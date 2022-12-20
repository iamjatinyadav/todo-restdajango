from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'},write_only=True, required=True )
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password field didn't match"})
        return attrs

    def create(self, vaildate_data):
        user = User.objects.create(email=vaildate_data['email'])
        user.set_password(vaildate_data['password'])
        # user.is_active = True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,style={'input_type': 'password'}, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self,instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return self


class TodoItemsSerializers(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = TodoItems
        fields = '__all__'


class TodoItemsWriteSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TodoItems
        fields = '__all__'
