from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.
class PublishedManager(models.Manager):
   def get_queryset(self):
       # Displays only published post
       return super().get_queryset().filter(status='published')  # ========= New lines


class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug = models.SlugField(max_length = 264, null = True, blank = True,)
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects = models.Manager() # The default manager. ============== New line
    published = PublishedManager() # The custom manager. =========== New line
    tags=TaggableManager()

    class Meta:
        ordering=['-publish',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        args=[
           self.publish.year,
           self.publish.month,
           self.publish.day,
           self.slug,
           ]
        return reverse('blog:post_detail', args=args)

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return "Commented By {} on {}".form(self.name,self.post)
