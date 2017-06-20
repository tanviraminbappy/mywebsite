from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts() :
    return Post.Published.count()


@register.inclusion_tag('mycoolwebsite/base.html')
def show_latest_posts(count=3):
    latest_posts = Post.Published.order_by('-published')[:count]
    return {'latest_posts' : latest_posts}

