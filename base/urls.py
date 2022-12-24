from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register("todos", TodoItemsView)

urlpatterns = [
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('changePassword/', ChangePasswordView.as_view()),
]

urlpatterns += router.urls