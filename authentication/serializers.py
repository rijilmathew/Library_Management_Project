from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from authentication.models import CustomUser,UserProfile
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user']={
            'userId':user.id,
            'user_name':user.username,
            'email':user.email,
            'role':user.role,
            'is_superuser': user.is_superuser,

         
        }
        return token
    

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        
        # Ensure that only an admin can register staff users
        if role == 'staff' and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError("You do not have permission to register staff users.")
        
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.role = role
        user.save()
        return user
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_picture']
        



