from rest_framework import serializers
from .models import Post
from user.models import Profile


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields= ["id","name","username",'email','avatar']
    


class PostSerializer(serializers.ModelSerializer):
    author=AuthorSerializers(read_only=True)
    category=serializers.CharField()
    tags=serializers.ListSerializer(child=serializers.CharField())
    class Meta:
        model=Post
        fields= ["id","author","title",'image','body','category','tags','likes','created_at','updated_at']
    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        return super().create(validated_data)
    
    