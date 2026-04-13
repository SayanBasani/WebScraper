from rest_framework import serializers
from django.contrib.auth.models import User,Group

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # roles = serializers.SlugRelatedField( many=True, slug_field="name", queryset=Group.objects.all(), required=False )
    
    class Meta:
        model = User
        # fields = ["username", "first_name", "last_name", "email", "password", "roles"]
        exclude = ["id","last_login","is_superuser","is_staff","is_active","date_joined","user_permissions"] 
        extra_kwargs = {"username": {"required": False},"email": {"required": True},"roles": {"required": False}}

    def create(self, validated_data):
        # roles = validated_data.pop("roles", [])
        password = validated_data.pop("password", None)
        if not validated_data.get("username") and validated_data.get("email"):
            validated_data["username"] = validated_data["email"]
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def validate(self, data):
        # Set username = email if username not provided
        if not data.get("username"):
            data["username"] = data["email"]
        return data


