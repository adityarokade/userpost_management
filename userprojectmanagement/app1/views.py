


from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    APIView,
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
# from .models import *
from app1.models import *

from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.decorators import method_decorator
from django.db import connections
from datetime import datetime, timedelta, date




@method_decorator(csrf_exempt, name="dispatch")
class login(APIView):
    def post(self, request):
        context = {}
        username = request.data.get("username")
        password = request.data.get("password")
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            context['data'] = {
                "message": "Login Successful!!!",
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": access_token,
                "id": user.id,
                "refresh": str(refresh),
                "login_status": 1,
            }
            
        else:
            context['data'] = {"message": "invalid credentials", "login_status": 0}
        return Response(context, status=status.HTTP_200_OK)
    

@method_decorator(csrf_exempt, name="dispatch")
class logout(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout Successful!"}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )
        




class Post_Managament(APIView):
    def post(self, request):
        context = {}
        data = json.loads(request.body)
        try:
            posts = Post()
            posts.title = data.get("title")
            posts.body = data.get("body")
            posts.author = request.user
            posts.save()
    
            context['message'] =  f' name : {posts.title} Created successfully...'
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context['error'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        context = {}

        try:
            posts = pd.DataFrame(Post.objects.all().values())
            context['posts'] = posts.to_dict(orient='records')
            # context['message'] =  f' name : {posts.title} Created successfully...'
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context['error'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        

class postslist(APIView):
    def get(self,request):
        context = {}

        try:
            posts = pd.DataFrame(Post.objects.all().values())
            context['posts'] = posts.to_dict(orient='records')
            # context['message'] =  f' name : {posts.title} Created successfully...'
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context['error'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        

class postread(APIView):
    def get(self,request,id):
        context = {}

        try:
            posts = pd.DataFrame(Post.objects.filter(id = id).values())
            context['posts'] = posts.to_dict(orient='records')
            # context['message'] =  f' name : {posts.title} Created successfully...'
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context['error'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,id):
        context = {}
        data = json.loads(request.body)
        try:
            posts = Post.objects.get(id = id)
            if posts.author.id != request.user.id:
                context['message'] =  f' you are not having access to update this posts.'
            # posts.author = data.get('author',posts.author)
            old_post = posts.title
            posts.title = data.get('title', posts.title)
            posts.body = data.get('body',posts.body)
            posts.save()
            
            context['message'] =  f' name :{old_post}--> {posts.title} updated successfully...'
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context['error'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    
