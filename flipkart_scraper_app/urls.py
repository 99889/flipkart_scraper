from django.urls import path
from .views import UserLogin, ScrapedDataAPI

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('scrape/', ScrapedDataAPI.as_view(), name='scrape-data'),
]
