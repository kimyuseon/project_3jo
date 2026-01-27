from django.shortcuts import render, redirect
from .models import Post, Comment
from django.urls import reverse


def index(request):
    return render(request, "index.html")

#전체목록보기
def post_list(request):
    my_posts = Post.objects.all().order_by('-created_at') #모든 레코드 조회 후 최신순으로 정렬
    my_context = {"posts":my_posts}

    return render(request, "community/post_list.html", context=my_context)

#특정 글 보기
#만약 로그인한 사용자만 댓글을 달게 하고싶다면 @login_required 데코레이션 추가한다.
#위에 from django.contrib.auth.decorators import login_required도 추가 같이 해줘야한다.
def post_detail(request, post_id):
    my_post = Post.objects.get(id=post_id)

    if request.method == "POST":
        my_comment_content = request.POST["comment"]
        Comment.objects.create(post=my_post, content = my_comment_content, author=request.user)

        return redirect("community:post_detail", post_id=post_id)
    
    my_comments = my_post.comment_set.all()
    my_context = {"post":my_post, "comments": my_comments}
    
    return render(request, "community/post_detail.html", context=my_context)


#글 작성하기
def post_add(request):
    #게시글 제목, 내용 가져오기
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        #이미지 파일 가져오기
        thumbnail = request.FILES["thumbnail"]

        #새로운 레시피 저장하기
        my_post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            thumbnail=thumbnail,
        )
        #저장하고 나면 상세페이지로 이동하기
        return redirect(reverse("community:post_detail", args=[my_post.id]))
    return render(request, "community/post_add.html")

#글 수정 
# def post_edit(request, post_id):
#     #수정할 기존 글 가져오기
#     my_post = Post.objects.get(id=post_id)

#     if request.method == "POST":
#         #새로 입력한 내용
#         my_post.title = request.POST["title"]
#         my_post.content = request.POST["content"]
#         #사진을 새로 올렸을 때 교체
#         if request.FILES.get("thumbnail"):
#             my_post.thumbnail = request.FILES["thumbnail"]
#         #변경 사항을 저장합니다.
#         my_post.save()
#         #수정 후 상세페이지 이동
#         return redirect(reverse("community:post_detail", args=[my_post.id]))

    
#     return render(request, "community/post_edit.html", {"post": my_post})

def post_edit(request, post_id):
    #수정을 진행할 기존 글 찾아오기
    my_post = Post.objects.get(id=post_id)

    if request.method == "POST":
        my_post.title = request.POST.get("title", my_post.title)
        my_post.content = request.POST.get("content", my_post.content)
        
        #사진을 새로 올렸을 때 교체
        if request.FILES.get("thumbnail"):
            my_post.thumbnail = request.FILES["thumbnail"]
            
        #변경사항 저장
        my_post.save()

        #수정 후 상세페이지로 이동
        return redirect("community:post_detail", post_id=my_post.id)

    # get요청시 수정 페이지로 이동
    return render(request, "community/post_edit.html", {"post": my_post})


#글 삭제
def post_delete(request, post_id):
    #삭제할 글을 가져오기
    my_post = Post.objects.get(id=post_id)
    #삭제하기
    my_post.delete()
    #삭제 후 목록으로 이동
    return redirect("community:post_list")

def login_view(request): 
    if request.method == 'POST':
        return render(request, 'community/login.html')
    else:
        return render(request, 'community/login.html')