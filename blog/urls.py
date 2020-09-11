from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from posts import views as user_views
from blog import settings
from marketing.views import email_list_signup
from posts import views
from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('upload/', include('post.urls')),
    path('', IndexView.as_view(), name='home'),
    # path('<str:user>', home, name='user_posts'),
    # url(r'^(?P<username>\w+)/$', views.profile_page, name='user_profile'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # path('create/', post_create, name='post-create'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('contact/', contactView, name='contact'),
    # path('profile/', views.profile, name='profile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url('userdetail/(?P<pk>[0-9]+)/', views.UserDetail.as_view(), name='userdetail'),
    url('user/follow/(?P<pk>[0-9]+)/', views.UserFollow.as_view(), name='user_follow'),
    url(r'^profile/(?P<username>\w+)/$',user_views.profile,name='profile'),
    url(r'^accounts/signup/home/profile/(?P<username>\w+)/$',user_views.profile,name='signup_profile'),
    url('users/', views.UserListView.as_view(), name='users_list')


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
