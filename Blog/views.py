from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import (
   Paginator, EmptyPage,
   PageNotAnInteger
)
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_list(request,tag_slug=None):
   posts = Post.published.all()
   tag=None
   if tag_slug:
       tag=get_object_or_404(Tag,slug=tag_slug)
       posts=posts.filter(tags__in=[tag])
   paginator = Paginator(posts, 2) # 2 posts in each page
   page = request.GET.get('page')
   try:
       posts = paginator.page(page)
   except PageNotAnInteger:
       # If page is not an integer deliver the first page
       posts = paginator.page(1)
   except EmptyPage:
       # If page is out of range deliver last page of results
       posts = paginator.page(paginator.num_pages)
   return render(request,
                 'blog/post_list.html',
                 {'page': page,
                  'posts': posts})


   return render(request,
                 'blog/post_list.html',
                 {'posts': posts,'tag':tag})

from .forms import CommentForm

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,slug=post,
                                  status='published',
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)
    posts_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.objects.filter(tags__in=posts_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()

    return render(request,
                 'blog/post_detail.html',
                 {'post': post,'form':form,'csubmit':csubmit,'comments':comments,'similar_posts':similar_posts})

from django.core.mail import send_mail
from .forms import EmailSendForm

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent= False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=post.get_absolute_url
            send_mail=("send","message","pythonlanguage323@gmail.com",[cd['to']])
            sent= True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})

def add_post_view(request):
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            print("Successfully Added")
        return post_list(request)
    return render(request,'Blog/addpost.html',{'form':form})
