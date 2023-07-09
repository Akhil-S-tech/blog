from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics,status
from .permissions import IsAuthor
from rest_framework.permissions import IsAuthenticated


from .serializers import PostSerializer
from .models import Post



class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]

class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg='post_id'

    def retrieve(self, request, *args, **kwargs):

        instance=self.get_object()
        serializer=self.get_serializer(instance)
        related_post=Post.objects.filter(tags__in=instance.tags.all()).exclude(id=instance.id)[:4]
        data=serializer.data
        data['related_post']=PostSerializer(related_post,many=True).data
        return Response(data,status=status.HTTP_200_OK)

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({ "success": True, "message": "updated post" })
        else:
            # print(serializer.errors)
            return Response({ "success": False, "message": "error updating post" })
        
class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg='post_id'
    permission_classes=[IsAuthenticated,IsAuthor]

    
    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         pk = kwargs.get("pk")
    #         post = Post.objects.get(id=pk)
    #         if post.user.id == request.user.id:
    #             self.perform_destroy(post)
    #             return Response({ "success": True, "message": "post deleted" })
    #         else:
    #             return Response({ "success": False, "message": "not enough permissions" })
    #     except ObjectDoesNotExist:
    #         return Response({ "success": False, "message": "post does not exist" })
