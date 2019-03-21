from rest_framework import serializers
from api.models import PostModel,CommentModel

class PostSerializer(serializers.ModelSerializer):
    class Meta():
        model = PostModel
        fields = ('id','author','title','text')
    
class PostSerializer1(serializers.Serializer):
    title = serializers.CharField(max_length=243)
    text = serializers.CharField(max_length=243)


class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model = CommentModel
        fields = ('id','post','author','text')    

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=243,required=True)
    first_name = serializers.CharField(max_length=243,required=False)
    last_name = serializers.CharField(max_length=243)
    email = serializers.EmailField(max_length=243)
    password = serializers.CharField(max_length=243,required=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=243)
    password = serializers.CharField(max_length=243)