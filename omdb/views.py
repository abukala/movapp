from rest_framework.decorators import api_view

from . import models, serializers
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import requests
import scipy.stats as ss


class MovieViewSet(ViewSet):
    def list(self, request):
        queryset = models.Movie.objects.all()
        year = request.query_params.get('Year', None)
        language = request.query_params.get('Language', None)
        if year:
            queryset = queryset.filter(Year=year)
        if language:
            queryset = queryset.filter(Language=language)

        serializer = serializers.MovieSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if 'Title' not in request.data:
            return Response({"Title": "Field is required"})

        response = requests.get('http://www.omdbapi.com/?apikey=7810b313&t=%s' % request.data['Title'])
        data = response.json()
        if 'Ratings' in data:
            data['Ratings'] = str(data['Ratings'])

        serializer = serializers.MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            queryset = models.Comment.objects.filter(movie_id=movie_id)
        else:
            queryset = models.Comment.objects.all()
        return queryset


@api_view(['GET'])
def top_movies(request):
    date_from = request.query_params.get('date_from', None)
    date_to = request.query_params.get('date_to', None)

    if not date_from or not date_to:
        return Response({'error': 'You must specify date_from and date_to query parameters.'})

    movies = models.Movie.objects.all()
    comments_count = [m.comments.filter(created_at__range=(date_from, date_to)).count() for m in movies]
    ranks = ss.rankdata([-1 * c for c in comments_count], method='dense')

    top_list = []
    for movie, count, rank in zip(movies, comments_count, ranks):
        top_list.append({
            'movie_id': movie.id,
            'rank': rank,
            'total_comments': count
        })
    return Response(top_list)
