from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'), # JWT based login
    path('l/', views.login,name='login'), # JWT based login
    path('status/',views.is_loggedin,name="is_loggedin"),
    path('profile/',views.profile,name="is_loggedin"),
]
