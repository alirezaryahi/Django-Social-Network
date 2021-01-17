from django.db import models
from profiles.models import Profile
from django.core.validators import FileExtensionValidator


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post/', blank=True, validators=[FileExtensionValidator(['png', 'jpg'])])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    licked = models.ManyToManyField(Profile, related_name='liked', blank=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.licked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-create',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


# class Like(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     update = models.DateTimeField(auto_now=True)
#     create = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user
