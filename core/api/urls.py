from django.urls import path

from .views import (
    SendOTPView, 
    VerifyOTPView, 
    ProjectCreateView, 
    ApprovedProjectListView,
    MyProjectListView,
    ProjectFilterView
)


urlpatterns = [
    path(
        'auth/send-otp/', 
        SendOTPView.as_view(),
        name='send-otp'
    ),
    path(
        'auth/verify-otp/',
        VerifyOTPView.as_view(),
        name='verify-otp'
    ),
    path(
        'items/',
        ProjectCreateView.as_view(),
        name = 'proj-create'
    ),
    path(
        'items/approved/',
        ApprovedProjectListView.as_view(),
        name = 'proj-approved'
    ),
    path(
        'items/my/',
        MyProjectListView.as_view(),
        name='proj-my'
    ),
    path(
        'items/filter/',
        ProjectFilterView.as_view(),
        name='proj-filters'
    ),
]
