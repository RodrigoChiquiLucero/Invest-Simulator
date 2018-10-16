from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/password/', views.change_password, name='password'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change_avatar/', views.change_avatar, name='change_avatar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
