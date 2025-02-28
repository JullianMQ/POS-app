from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializer import UserSerializer


# Create your views here.
@api_view(['GET'])
def get_users(req):
    users = User.objects.all()
    serializedUsers = UserSerializer(users, many=True).data
    return Response(serializedUsers)


@api_view(['POST'])
def create_user(req):
    data = req.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET'])
def delete_user(req, key):
    try:
        user = User.objects.get(pk=key)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif req.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
