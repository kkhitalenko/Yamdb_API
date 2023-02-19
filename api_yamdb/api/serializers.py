from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class SignupSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Регистрация пользователя с именем "me" невозможна'
            )
        if User.objects.filter(email=data['email']).exists:
            raise serializers.ValidationError(
                'Почта уже зарегистрирована'
            )
        return data


class CheckConfCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'confirmation_code',)
        model = User
