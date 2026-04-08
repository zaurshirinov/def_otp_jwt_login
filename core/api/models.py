from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_LIST = [
        (PENDING, "PENDING"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED")
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.CharField()
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="projects"
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_LIST,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
