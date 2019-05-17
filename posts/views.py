from unidecode import unidecode
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse
import random
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, Comment


def slugify(slug):
    slug = slug.replace(' ', '-')
    return slug


def generate_id():
    id = random.randint(0000000, 9999999)
    return id


def index(request):
    posts = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-date')[:3]
    context = {
        "posts": posts,
        "latest": latest
    }
    return render(request, 'index.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'subcontent', 'slug', 'content', 'image', 'featured']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'subcontent', 'categories', 'content', 'image', 'featured']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = unidecode(form.instance.title)
        form.instance.slug = slugify(form.instance.slug)
        form.instance.post_id = generate_id()
        return super().form_valid(form)


def post(request, slug, post_id):
    post = get_object_or_404(Post, slug=str(slug), post_id=str(post_id))
    latest = Post.objects.order_by('-date')[:3]
    comments = post.get_comments
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    # create replay comment object
                    reply_comment = form.save(commit=False)
                    # assign parent_obj to replay comment
                    reply_comment.parent = parent_obj
            form.instance.post = post
            form.instance.user = request.user
            form.save()
            return redirect(reverse("post", kwargs={
                'slug': post.slug,
                'post_id': post.post_id,
            }))
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'latest': latest

    }
    return render(request, 'post.html', context)


def like(request, slug, post_id, comment_id):
    post = get_object_or_404(Post, slug=str(slug), post_id=str(post_id))
    comment = get_object_or_404(Comment, id=int(comment_id))
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    elif user in comment.dislikes.all():
        comment.dislikes.remove(user)
        comment.likes.add(user)
    else:
        comment.likes.add(user)

    return redirect(reverse("post", kwargs={
        'slug': post.slug,
        'post_id': post.post_id,
    }))


def dislike(request, slug, post_id, comment_id):
    post = get_object_or_404(Post, slug=str(slug), post_id=str(post_id))
    comment = get_object_or_404(Comment, id=int(comment_id))
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)

    elif user in comment.likes.all():
        comment.likes.remove(user)
        comment.dislikes.add(user)
    else:
        comment.dislikes.add(user)

    return redirect(reverse("post", kwargs={
        'slug': post.slug,
        'post_id': post.post_id,
    }))


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query) |
            Q(subcontent__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'results.html', context)


def news(request):
    latest = Post.objects.order_by('-date')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'latest': latest,
        'page_request_var': page_request_var,
    }
    return render(request, 'blog.html', context)

def about(request):
    return render(request, 'about.html')
