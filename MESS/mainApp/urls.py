from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),

    path('subscribe/',views.addSubscriber,name='addSubscriber'),
    path('getSubs/',views.getSubs,name='getSubs'),
    path('delSubs/',views.delSubs,name='delSubs'),




]