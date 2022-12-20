from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("todos", TodoItemsView)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name="Register"),
    path('signin/', LoginView.as_view()),
    path('changePassword/', ChangePasswordView.as_view())
]

urlpatterns += router.urls