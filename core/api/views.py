from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.cache import cache
from django.contrib.auth.models import User 

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Project
from .serializers import (
    SendOTPSerializer, 
    VerifyOTPSerializer,
    ProjectSerializer
)

from .utils import generate_otp_code
from .tasks import send_mail
from .paginations import StandardResultsSetPagination
from .filters import ManualFilter


class SendOTPView(APIView):
    throttle_scope = "otp_limit"

    @swagger_auto_schema(request_body=SendOTPSerializer)
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            rate_key = f"otp_rate_{email}"
            if cache.get(rate_key):
                return Response(
                    {"error": "Please wait before requesting another OTP for this email."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            cache_key = f"otp_{email}"
            if cache.get(cache_key):
                return Response(
                    {"error": "OTP already sent. Please wait."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            otp_code = generate_otp_code()
            
            send_mail.delay(
                "Login",
                otp_code,
                recipient_list=[email],
            )

            cache.set(cache_key, otp_code, timeout=300)

            cache.set(rate_key, True, timeout=60)

            return Response(
                {"message": "OTP sent successfully"},
                status=status.HTTP_200_OK
            )
    
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
        

    

class VerifyOTPView(APIView):
    throttle_scope = "login_limit"

    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = serializer.validated_data["otp"]

            cache_key = f"otp_{email}"
            stored_otp = cache.get(cache_key)

            if otp_code != stored_otp:
                return Response(
                    {
                        "error": "Invalid or expired OTP!",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user, _ = User.objects.get_or_create(
                username=email, 
                defaults={"email": email}
                )
            
            token = RefreshToken.for_user(user)

            cache.delete(cache_key)

            data = {
                "user": user.pk,
                "refresh": str(token),
                "access_token": str(token.access_token),
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
class ProjectCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=ProjectSerializer)
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    

class ApprovedProjectListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        projects = Project.objects.filter(
            status=Project.APPROVED
        ).order_by(
            "-created_at"
        )

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProjectFilterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by status (pending, approved, rejected)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'created_at',
                openapi.IN_QUERY,
                description="Filter by date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'title',
                openapi.IN_QUERY,
                description="Search in title",
                type=openapi.TYPE_STRING
            ),
        ]
    )

    def get(self, request):
        projects = Project.objects.all().order_by("-created_at")
        
        projects = ManualFilter.apply_filter(projects, request.query_params)

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MyProjectListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ProjectSerializer(many=True)}
    )

    def get(self, request):
        projects = Project.objects.filter(created_by=request.user)

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    