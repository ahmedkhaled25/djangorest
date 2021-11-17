from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'mobile', 'profile_image', 'password', 'password_confirm')
        # extra_kwargs = {'password' : }

    def save(self, **kwargs):

        if self.validated_data.get('password') != self.validated_data.get('password_confirm'):
            raise serializers.ValidationError(
                {
                    'password': "Password doesn't match"
                }
            )
        user = User(email=self.validated_data.get('email'), username=self.validated_data.get('username'), mobile=self.validated_data.get('mobile'))
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user
