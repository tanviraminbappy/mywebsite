from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count



def post_list(request, tag_slug=None):

    object_list = Post.Published.all()
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage :
        posts = paginator.page(paginator.num_pages)
    return render(request, 'mycoolwebsite/post/list.html', {'page': page, 'posts': posts})

# class PostListView(ListView):
#     queryset = Post.Published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'mycoolwebsite/post/list.html'

def post_detail(request, year, month, day, post) :
    post = get_object_or_404(Post, slug=post, status='published', published__year=year,published__month=month,published__day=day )

    comments = post.comments.filter(active=True)

    if request.method =='POST' :
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.Published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:4]




    return render(request, 'mycoolwebsite/post/detail.html', {'post': post, 'comments' : comments, 'comment_form' : comment_form, 'similar_posts': similar_posts} )


def post_share(request, post_id) :
    post = get_object_or_404(Post, id=post_id , status='published')
    sent = False
    if request.method == 'POST' :
        form = EmailPostForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommands you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n\'s comments : {}'.format(post.title, post_url, cd['comment'])
            to_emails = [settings.EMAIL_HOST_USER,cd['to'] ]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, to_emails )

            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'mycoolwebsite/post/share.html', {'post': post, 'form': form, 'sent': sent})
