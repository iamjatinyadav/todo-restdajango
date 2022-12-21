from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import *
from .serializers import *
from rest_framework import permissions


class TodoItemsView(viewsets.ModelViewSet):
    queryset = TodoItems.objects.all()
    serializer_class = TodoItemsSerializers
    permission_classes = [permissions.IsAuthenticated]
    # search with 0,1 and 2
    search_fields = (
        '^status',
    )

    def get_serializer_class(self):
        if self.action == 'update':
            return TodoItemsWriteSerializers
        elif self.action == 'create':
            return TodoItemsWriteSerializers
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return TodoItems.objects.filter(user=user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

