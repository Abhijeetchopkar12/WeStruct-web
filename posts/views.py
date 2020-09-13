from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm, PostForm, UserUpdate, ProfileUpdate, ContactForm
from .models import Post, Author, PostView, User, Contact
from marketing.forms import EmailSignupForm
from marketing.models import Signup
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.views import generic
from actions.utils import create_action
from django.core.mail import send_mail, BadHeaderError



form = EmailSignupForm()

class UserListView(generic.ListView):
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()

class UserDetail(generic.DetailView):
    context_object_name = "person"
    model = User
    template_name = 'user_detail.html'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        
        try:
            context['profile'] = Author.objects.filter(user=User.objects.get(pk=pk))
            context['queryset'] = Post.objects.filter(author=Author.objects.get(pk=pk))
        except ObjectDoesNotExist:
            pass
        return context


class UserFollow(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        celeb = get_object_or_404(User, pk=pk)
        url_ = '/'

        if self.request.user.is_authenticated:
            if self.request.user in celeb.followers.all():
                Contact.objects.filter(user_from=self.request.user,
                                       user_to=celeb).delete()
            else:
                Contact.objects.get_or_create(user_from=self.request.user,
                                              user_to=celeb)
                create_action(self.request.user, 'is now following', celeb)
        return url_

@login_required
def profile(request, username):
    if username == request.user:
        if request.method == 'POST':
            u_form = UserUpdate(request.POST, instance= request.user)
            p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.author)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,f'Your Profile has been updated!')
        else:
            u_form = UserUpdate(instance=request.user)
            p_form = ProfileUpdate(instance=request.user.author)

        post_form = PostForm()
        person = User.objects.get(username = username)
        context = {
            'u_form':u_form,
            'p_form':p_form,
            'post_form':post_form,
            'person':person
            }
    else:
        if request.method == 'POST':
            u_form = UserUpdate(request.POST, instance= request.user)
            p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.author)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,f'Your Profile has been updated!')
        else:
            u_form = UserUpdate(instance=request.user)
            p_form = ProfileUpdate(instance=request.user.author)

        person = User.objects.get(username = username)
        # already_a_follower=0
        # for followers in person.follower_set.all():
        #     if (followers.follower_user ==  request.user.username):
        #         already_a_follower=1
        #             break;
                    
        #     if already_a_follower==1:
            #     context = {'person':person,}
            # else:
            #     context = {'person':person, 'f':1,}
        context = {
            'u_form':u_form,
            'p_form':p_form,
            'person':person
            }
        
    return render(request, 'profile.html', context)

def contactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        form.save()
        messages.success(request,f'Your message was successfully send')
    else:    
        form = ContactForm()
    return render(request, "contact.html", {'form': form})

# @login_required
# def profile_update(request):
#     if request.method == 'POST':
#         u_form = UserUpdate(request.POST, instance= request.user)
#         p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.author)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#         return redirect('profile')
#     else:
#         u_form = UserUpdate(instance=request.user)
#         p_form = ProfileUpdate(instance=request.user.author)
#     return render(request, 'profile_update.html', {'u_form':u_form, 'p_form':p_form})

def get_user(username):
    qs = User.objects.filter(username=username)
    if qs.exists():
        return qs[0]
    return None

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")

# def home(request, username = None):

#     if username:
#         author = User.objects.get(username=username)
#         posts = Post.objects.filter(author=author)
#     else:
#         posts = Post.objects.all()

#     posts = posts.order_by('-Date')
#     context = {'posts': posts,}
#     return render(request, 'index.html', context)

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'posts': posts,
        'object_list': featured,
        'latest': latest,
        'form': form
    }
    return render(request, 'index.html', context)



class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context
   

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.instance.user_author = get_author(self.request.user)
        form.save()

        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

    # def form_valid(self, form):
    #     form.instance.user_author = self.request.user
    #     return super(PostCreateView, self).form_valid(form) 


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:4]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

def post_list(request):
    weeek_ago = datetime.date.today() - datetime.timedelta(days=7)
    trending = Post.objects.filter(Date__get = weeek_ago).order_by('-rating')
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:4]
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
        'trending': trending[:5],
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self, **kwargs):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


def post_detail(request, id):
    weeek_ago = datetime.date.today() - datetime.timedelta(days=7)
    trending = Post.objects.filter(Date__get=weeek_ago).order_by(-rating)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'trending':trending,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()

        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    user = get_user(request.user)

    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form_user.instance.user = user
            form.save()
            form_user.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form,
        'form_user':form_user
    }
    return render(request, "post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()

        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)    
    author = get_author(request.user)
    user = get_user(request.user)

    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form_user.instance.user = user
            form.save()
            form_user.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form,
        'form_user':form_user
    }
    return render(request, "post_create.html", context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
