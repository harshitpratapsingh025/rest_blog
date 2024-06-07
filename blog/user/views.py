from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResigterSerializer
from rest_framework import status

class RegisterView(APIView):

    def post(self, request):

        try:
            serializer = ResigterSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                    'data': {},
                    'message': 'Registration successfull.'
                }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'Something went wrong.'
                }, status=status.HTTP_400_BAD_REQUEST)

