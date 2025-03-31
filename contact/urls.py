
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.contactHome,name='contacts'),
    path('search/', views.search,name='search'),
    path('<int:contact_id>/', views.contactDetails,name='contact'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)