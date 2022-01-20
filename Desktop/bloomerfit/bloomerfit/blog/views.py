from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.core.paginator import (
   Paginator, EmptyPage,
   PageNotAnInteger
)
#https://docs.github.com/en/get-started/quickstart/hello-world


def blog_index(request):
    object_list = Post.objects.all().order_by('-created_on')
    paginator = Paginator(object_list, 6) # 6 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        "posts": posts,
        "page":page
    }
    return render(request, "blog/blog_index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog/blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    object_list = Post.objects.all().exclude(id=post.id)

    form = CommentForm()
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()
            

    comments = Comment.objects.filter(post=post)
    num_of_comments = len(comments)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "object_list":object_list,
        "num_of_comments":num_of_comments
    }
    return render(request, "blog/blog_detail.html", context)
