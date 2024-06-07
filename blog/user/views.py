from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResigterSerializer, LoginSerializer
from rest_framework import status


class RegisterView(APIView):

    def post(self, request):
        try:
            serializer = ResigterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "Something went wrong."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response(
                {"data": {}, "message": "Registration successfull."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)
            return Response(
                {"data": {}, "message": "Something went wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):

    def post(self, request):

        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "Invalid user inputs."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response = serializer.get_tokens_for_user(data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"data": {}, "message": "Something went wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )
