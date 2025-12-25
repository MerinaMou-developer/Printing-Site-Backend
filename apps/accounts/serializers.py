"""
User Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

User = get_user_model()


class EmailOnlyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Authenticate users strictly with email + password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace the default username field with email to control validation errors
        self.fields['email'] = serializers.EmailField()
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed('No active account found with the provided email.') from exc

        if not user.is_active:
            raise AuthenticationFailed('No active account found with the provided email.')

        credentials = {
            self.username_field: getattr(user, user.USERNAME_FIELD),
            'password': password,
        }

        return super().validate(credentials)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'address', 'city', 
            'state', 'country', 'company_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }
    
    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def validate_username(self, value):
        """Username is optional and can be duplicate"""
        # Username can be duplicate - no validation needed
        return value or None
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # Auto-generate username from email if not provided (can be duplicate)
        username = validated_data.get('username', '').strip()
        if not username:
            email = validated_data.get('email', '')
            # Use email prefix as username (can be duplicate, that's fine)
            base_username = email.split('@')[0]
            # Clean username (remove special chars, limit length)
            base_username = ''.join(c for c in base_username if c.isalnum() or c in ['_', '-'])[:150]
            validated_data['username'] = base_username or 'user'
        else:
            validated_data['username'] = username
        
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'city', 'state', 'country', 'company_name',
            'date_joined', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'username', 'date_joined', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'address', 
            'city', 'state', 'country', 'company_name'
        )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

