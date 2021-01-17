from django.contrib import admin
from .models import Post, Comment


# Register your models here.

class Post_admin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create', 'update']
    search_fields = ['author']

    class Meta:
        model = Post


class Comment_admin(admin.ModelAdmin):
    list_display = ['user', 'post', 'create', 'update']
    search_fields = ['user']

    class Meta:
        model = Comment


# class Like_admin(admin.ModelAdmin):
#     list_display = ['user', 'post', 'like', 'create', 'update']
#     search_fields = ['user']
#     list_filter = ('like',)
#
#     class Meta:
#         model = Like


admin.site.register(Post, Post_admin)
admin.site.register(Comment, Comment_admin)
# admin.site.register(Like, Like_admin)
