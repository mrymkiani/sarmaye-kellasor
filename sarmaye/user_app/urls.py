from django.urls import path
from .views import Login, Refresh, UserRegisteration, UserProfileView

urlpatterns = [
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('register/', UserRegisteration.as_view()),
    path('profile/', UserProfileView.as_view()),
]