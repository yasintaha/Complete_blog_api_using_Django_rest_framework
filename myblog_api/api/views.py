from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.serializers import PostSerializer,CommentSerializer,SignupSerializer,LoginSerializer,PostSerializer1
from api.models import PostModel,CommentModel
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class SignupView(APIView):
    serializer_class = SignupSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                content = {'message':'user already exist'}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
            else:
                user_save = User(username=username,first_name=first_name,last_name=last_name,email=email)
                user_save.set_password(password)
                user_save.save()
                content = {'message':'user registered successfully'}
                return Response(content,status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                print(token)
                content = {'message':'login successfully','token':str(token)}
                return Response(content,status=status.HTTP_200_OK)            
            else:
                content = {'message':'unable to login'}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer1

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user 
            print(user)    
            title = serializer.data['title']
            text = serializer.data['text']

            try:
                user_a = User.objects.get(username=user) 
                               
            except User.DoesNotExist:
                print("----")
            print("detailed",user_a)
            post = PostModel()
            post.author = user_a
            post.title = title
            post.text = text
            post.save()
            content = {'message':'post created successfullly'}
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            content = {'message':'unbale to create'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

class PostDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer 

class PostListView(generics.ListAPIView):
    queryset = PostModel.objects.all().order_by('-published_date')
    serializer_class = PostSerializer

class PostPublish(APIView):
    def get(self,request,pk):
        post = get_object_or_404(PostModel,pk=pk)
        if post:
            post.publish()
            content = {'message':'post published'}
            return Response(content,status=status.HTTP_201_CREATED)
        
class add_comment_to_post(APIView):
    serializer_class = CommentSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {'message':'comment created'}
            return Response(content,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

class comment_approve(APIView):
    def get(self,request,pk):
        comment = get_object_or_404(CommentModel,pk=pk)
        comment.approve()
        content = {'message': 'comment is approved' }
        return Response(content,status=status.HTTP_201_CREATED)

class comment_remove(APIView):
    def get(self,request,pk):
        comment = get_object_or_404(CommentModel,pk=pk)
        content = {'message': 'comment deleted' }
        comment.delete()
        return Response(content,status=status.HTTP_204_NO_CONTENT)

class commentList(generics.ListAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer