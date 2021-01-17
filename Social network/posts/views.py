from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from posts.models import Post
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def post_comment_create_and_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    p_form = PostForm()
    c_form = CommentForm()
    post_added = False

    if 'p_button' in request.POST:
        p_form = PostForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostForm()
            post_added = True

    if 'c_button' in request.POST:
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentForm()
    context = {
        'posts': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }
    return render(request, 'main.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.licked.all():
            post_obj.licked.remove(profile)
        else:
            post_obj.licked.add(profile)
        # like, create = Like.objects.get_or_create(user=profile, post=post_id)
        # if not create:
        #     if like.like:
        #         like.like = False
        #     else:
        #         like.like = True
        # else:
        #     like.like = True
        #     post_obj.save()
            # like.save()
    return redirect('posts')


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'confirm-del.html'
    success_url = reverse_lazy('posts')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if obj.author.user != self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete the post')
        return obj


class PostUpdateView(UpdateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'update.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the author of the post in order to update the post')
            return super().form_invalid(form)
