from rest_framework import serializers
from app.models import Post

class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'score', 'url', 'posted_at']
