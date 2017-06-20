from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def  get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model) :

    STATUS_CHOICE = (('draft', 'Draft'), ('published', 'Published'), )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    objects = models.Manager()
    Published = PublishedManager()

    tags = TaggableManager()

    class Meta :
        ordering = ['-published']

    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse('mycoolwebsite:post_detail', args=[self.published.year, self.published.strftime('%m'),self.published.strftime('%d'),self.slug
                                                          ])



class comment(models.Model) :
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta :
        ordering = ('created',)

    def __str__(self):
        return 'comment by {} on {}'.format(self.name, self.post)
