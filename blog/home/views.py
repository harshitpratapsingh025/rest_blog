from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializer
from .models import Blog
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator


class PublicBlogView(APIView):

    def get(self, request):

        try:
            blogs = Blog.objects.all().order_by("?")
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )

            page_number = request.GET.get("page", 1)
            page_size = request.GET.get("size", 2)
            paginator = Paginator(blogs, page_size)
            serializers = BlogSerializer(paginator.page(page_number), many=True)
            return Response({"data": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong or invalid page"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
            serializers = BlogSerializer(blogs, many=True)
            return Response({"data": serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            request.data._mutable = True
            data = request.data
            data["user"] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {"message": "Invalid data", "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {"message": "Blog created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        try:
            data = request.data
            blogs = Blog.objects.filter(uid=data.get("uid"))
            if not blogs.exists():
                return Response(
                    {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )

            if request.user != blogs[0].user:
                return Response(
                    {"message": "You are not authorized for this."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = BlogSerializer(blogs[0], data=data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {"message": "Invalid data", "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {"message": "Blog updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        try:
            data = request.data
            blogs = Blog.objects.filter(uid=data.get("uid"))
            if not blogs.exists():
                return Response(
                    {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
                )

            if request.user != blogs[0].user:
                return Response(
                    {"message": "You are not authorized for this."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            blogs[0].delete()
            return Response(
                {"message": "Blog deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
