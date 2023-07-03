from rest_framework.response import Response
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status

from .serializers import BlogPostSerializer
from .models import Post

# List all posts
class BlogView(APIView):
    def get(self,request,format=None):
        post= Post.objects.all()
        serializer=BlogPostSerializer(post,many=True)
        return Response(serializer.data)

# Create a post     
class BlogCreate(APIView):
    def post(self, request, format=None):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Details of a post 
class BlogDetail(APIView):
    def get_object(self, pk):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)
    
# Update a Post 
class BlogUpdate(APIView):
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

 # delete a post         
class BlogDelete(APIView):
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
