from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import register, profile

from django.contrib.auth import views as auth_views
from posts.views import PostCreateView, PostUpdateView, PostDeleteView,search, news, index,about,post,like,dislike

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('blog/', news, name='blog'),
    path('about/',about,name='about'),
    path('search/', search, name='search'),
    path('create/',PostCreateView.as_view(template_name='create.html'), name='create'),
    path('article/<slug>/<post_id>/update/', PostUpdateView.as_view(template_name='create.html'), name='update-post'),
    path('article/<slug>/<post_id>/delete/', PostDeleteView.as_view(template_name='post_confirm_delete.html'), name='delete-post'),
    path('article/<slug>/<int:post_id>/',post, name='post'),
    path('article/<slug>/<int:post_id>/like/<int:comment_id>/', like, name='like'),
    path('article/<slug>/<int:post_id>/dislike/<int:comment_id>/', dislike, name='dislike'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

