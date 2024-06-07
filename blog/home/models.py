from django.db import models
import uuid
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog")
    title = models.CharField(max_length=500)
    description = models.TextField()
    main_image = models.ImageField(upload_to="images")

    def __str__(self) -> str:
        return self.title
