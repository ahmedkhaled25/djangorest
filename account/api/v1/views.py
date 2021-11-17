from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from.serializers import UserSerializer
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([])
def signup(request):
    data = {'data': '', 'status': ''}

    user_serialized = UserSerializer(data=request.data)

    if user_serialized.is_valid():
        user_serialized.save()
        data['data'] = {
            'user': user_serialized.data,
            'token': Token.objects.get(user__username=user_serialized.data.get('username')).key,
             'message': 'Created'
        }
        data['status'] = status.HTTP_201_CREATED
    else:
        data['data'] = user_serialized.errors
        data['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def logout(request):
    data = {'data': 'logging out', 'status': status.HTTP_200_OK}
    tno = str(request.auth)

    tok = Token.objects.get(key=tno)
    tok.delete()

    return Response(**data)
