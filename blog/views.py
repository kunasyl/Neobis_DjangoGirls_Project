from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from . import models, forms


def post_list(request):
    posts = models.Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_new(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = forms.PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(forms.Post, pk=pk)
    if request.method == "POST":
        form = forms.PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = forms.PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})
