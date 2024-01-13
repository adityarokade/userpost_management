from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mst_UsrTbl
        fields = ('id', 'username', 'email',)  # Add other fields as needed



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author',)
        read_only_fields = ('author',)