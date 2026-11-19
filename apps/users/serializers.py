from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, email):
        email = email.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return email

    def validate(self, attrs):
        attrs_without_password = attrs.copy()
        password = attrs_without_password.pop('password')
        user = User(**attrs_without_password)

        try:
            validate_password(password, user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'password': list(error.messages)})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)