from django.db import models
from user.models import Profile
import uuid

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="blog_posts"
    )
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to="posts/", default="default/post.jpg")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="blog_posts"
    )
    tags = models.ManyToManyField("Tag", related_name="blog_posts")
    likes = models.ManyToManyField(Profile, related_name="liked_posts")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # return the likes count
    @property
    def get_likes_count(self):
        return self.likes.count()

    def __str__(self) -> str:
        return self.title[0:8]

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["-created_at"]


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message[0:6]

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
