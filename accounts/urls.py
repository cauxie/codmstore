# urls.py (main project urls.py)
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('shop/', views.shop, name='shop'),
    path('battle/', views.battle_view, name='battle'),
    path('request/', views.request_page, name='request'),
   
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-of-service/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # ... other paths
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)