from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")

# 전체 목록 보기
def post_list(request):
    my_posts = Post.objects.all().order_by('-created_at') 
    my_context = {"posts": my_posts}
    return render(request, "community/post_list.html", context=my_context)

#글보기
def post_detail(request, post_id):
    # Post.objects.get(id=post_id) 대신 get_object_or_404 사용
    my_post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('user:login')
        
        my_comment_content = request.POST.get("comment")
        if my_comment_content: 
            Comment.objects.create(
                post=my_post, 
                content=my_comment_content, 
                author=request.user
            )
        return redirect("community:post_detail", post_id=post_id)
    
    my_comments = my_post.comment_set.all()
    my_context = {
        "post": my_post, 
        "comments": my_comments
    }
    return render(request, "community/post_detail.html", context=my_context)

# 글 작성
@login_required
def post_add(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        thumbnail = request.FILES.get("thumbnail")

        my_post = Post.objects.create(
            author=request.user, 
            title=title,
            content=content,
            thumbnail=thumbnail,
        )
        return redirect("community:post_detail", post_id=my_post.id)
    return render(request, "community/post_add.html")

# 수정
@login_required
def post_edit(request, post_id):
    my_post = get_object_or_404(Post, id=post_id)

    if my_post.author != request.user:
        return redirect("community:post_detail", post_id=post_id)

    if request.method == "POST":
        my_post.title = request.POST.get("title", my_post.title)
        my_post.content = request.POST.get("content", my_post.content)
        if request.FILES.get("thumbnail"):
            my_post.thumbnail = request.FILES["thumbnail"]
        my_post.save()
        return redirect("community:post_detail", post_id=my_post.id)

    return render(request, "community/post_edit.html", {"post": my_post})

# 글 삭제
@login_required
def post_delete(request, post_id):
    my_post = get_object_or_404(Post, id=post_id)
    
    if my_post.author == request.user:
        my_post.delete()
    
    return redirect("community:post_list")

def login_view(request): 
    return render(request, 'community/login.html')

#좋아요 기능
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)    
        
    return redirect('community:post_detail', post_id=post_id)