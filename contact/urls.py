
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.contactHome,name='contacts'),
    path('search/', views.search,name='search'),
    path('contact/<int:contact_id>/detail/', views.contactDetails,name='contact'),
    path('contact/create/', views.create,name='create'),
    path('contact/<int:contact_id>/update/', views.update,name='update'),
    path('contact/<int:contact_id>/delete/', views.delete,name='delete'),

    path('user/register/', views.register,name='register'),
    path('user/login/', views.login_view,name='login'),
    path('user/logout/', views.logout_view,name='logout'),
    path('user/update/', views.user_update,name='update'),


]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)