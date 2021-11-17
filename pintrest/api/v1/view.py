from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer
from pintrest.models import Movie
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.authentication import TokenAuthentication


class UserCanDeleteMovie(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='can-Delete').existd():
            return True
        return False


@api_view(['GET'])
@permission_classes([IsAdminUser])
def hello(request):
    data = {'message': 'Hello from rest api'}
    return Response(data=data)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(instance=movies, many=True)

    return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([UserCanDeleteMovie])
def movie_create(request):
    serialized_movie = MovieSerializer(data=request.data)
    if serialized_movie.is_valid():
        serialized_movie.save()
    else:
        return Response(data=serialized_movie.errors, status=status.HTTP_400_BAD_REQUEST)

    # Manipulate response
    data = {
        'message': 'Success',
        'data': {'id': serialized_movie.data.get('id')}
    }

    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def movie_detail(request, pk):
    response = {}
    movie_obj = Movie.objects.filter(pk=pk)
    if movie_obj.exists():
        movie_obj = movie_obj.first()
        serialized_movie = MovieSerializer(instance=movie_obj)

        response['data'] = serialized_movie.data
        response['status'] = status.HTTP_200_OK
    else:
        response['data'] = {'message': 'failed Movie does not exist'}
        response['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(['DELETE'])
def movie_delete(request, pk):
    response = {}
    try:
        movie_obj = Movie.objects.get(pk=pk)
        movie_obj.delete()
        response['data'] = {'message': 'Successfully Deleted Movie'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'Error While Deleting Movie -- {} -- Target Movie {}'.format(str(e), pk)}
        response['status'] = status.HTTP_400_BAD_REQUEST

    print("Result -> ", response)
    return Response(**response)


@api_view(['PUT', 'PATCH'])
def movie_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serialized_movie = MovieSerializer(instance=movie, data=request.data)
    elif request.method == 'PATCH':
        serialized_movie = MovieSerializer(instance=movie, data=request.data, partial=True)

    if serialized_movie.is_valid():
        serialized_movie.save()
        return Response(data=serialized_movie.data, status=status.HTTP_200_OK)

    return Response(data=serialized_movie.errors, status=status.HTTP_400_BAD_REQUEST)