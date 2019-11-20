from rest_framework import status
from django.test import TestCase, Client
from .models import Movie, Comment
from .serializers import MovieSerializer, CommentSerializer

client = Client()

terminator = {
    "id": 1,
    "Title": "Terminator",
    "Year": "1991",
    "Rated": "N/A",
    "Released": "N/A",
    "Runtime": "39 min",
    "Genre": "Short, Action, Sci-Fi",
    "Director": "Ben Hernandez",
    "Writer": "James Cameron (characters), James Cameron (concept), Ben Hernandez (screenplay)",
    "Actors": "Loris Basso, James Callahan, Debbie Medows, Michelle Kovach",
    "Plot": "A cyborg comes from the future, to kill a girl named Sarah Lee.",
    "Language": "English",
    "Country": "USA",
    "Awards": "N/A",
    "Poster": "N/A",
    "Ratings": "[{'Source': 'Internet Movie Database', 'Value': '6.0/10'}]",
    "Metascore": "N/A",
    "imdbRating": "6.0",
    "imdbVotes": "24",
    "imdbID": "tt5817168",
    "Type": "movie",
    "DVD": "N/A",
    "BoxOffice": "N/A",
    "Production": "N/A",
    "Website": "N/A",
    "Response": "True"
}

kevin = {
    'id': 2,
    "Title": "Home Alone",
    "Year": "1990",
    "Rated": "PG",
    "Released": "16 Nov 1990",
    "Runtime": "103 min",
    "Genre": "Comedy, Family",
    "Director": "Chris Columbus",
    "Writer": "John Hughes",
    "Actors": "Macaulay Culkin, Joe Pesci, Daniel Stern, John Heard",
    "Plot": "An eight-year-old troublemaker must protect his house from a pair of burglars when he is accidentally left home alone by his family during Christmas vacation.",
    "Language": "English",
    "Country": "USA",
    "Awards": "Nominated for 2 Oscars. Another 10 wins & 4 nominations.",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMzFkM2YwOTQtYzk2Mi00N2VlLWE3NTItN2YwNDg1YmY0ZDNmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
    "Ratings": "[{'Source': 'Internet Movie Database', 'Value': '7.6/10'}, {'Source': 'Rotten Tomatoes', 'Value': '65%'}, {'Source': 'Metacritic', 'Value': '63/100'}]",
    "Metascore": "63",
    "imdbRating": "7.6",
    "imdbVotes": "414,746",
    "imdbID": "tt0099785",
    "Type": "movie",
    "DVD": "05 Oct 1999",
    "BoxOffice": "N/A",
    "Production": "Twentieth Century Fox",
    "Website": "N/A",
    "Response": "True"
}


class GetMoviesTest(TestCase):
    def setUp(self):
        Movie.objects.create(**terminator)
        Movie.objects.create(**kevin)

    def test_get_movies(self):
        response = client.get('/movies/')
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateMovieTest(TestCase):
    def test_create_movie(self):
        response = client.post('/movies/', data={'Title': 'Terminator'})
        self.assertEqual(response.data, terminator)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        movies = Movie.objects.all()
        self.assertEqual(len(movies), 1)

        response_double = client.post('/movies/', data={'Title': 'Terminator'})
        self.assertEqual(response_double.data['id'], response.data['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/movies/', data={'Title': 'Home Alone'})
        self.assertEqual(response.data, kevin)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post('/movies/', data={})
        self.assertEqual(response.data, {'Title': 'Field is required'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/movies/', data={'Title': 'asdf'})
        self.assertEqual(response.data, {'Response': 'False', 'Error': 'Movie not found!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateCommentTest(TestCase):
    def setUp(self):
        Movie.objects.create(**terminator)
        Movie.objects.create(**kevin)

    def test_create_comment(self):
        response = client.post('/comments/', {'movie_id': 1, 'message': 'test'})
        self.assertEqual(response.data['movie_id'], 1)
        self.assertEqual(response.data['message'], 'test')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)


class GetCommentsTest(TestCase):
    def setUp(self):
        Movie.objects.create(**terminator)
        Movie.objects.create(**kevin)
        Comment.objects.create(movie_id=Movie.objects.get(id=1), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=1), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')

    def test_get_comments(self):
        response = client.get('/comments/')
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 5)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get('/comments/?movie_id=1')
        comments = Comment.objects.filter(movie_id=1)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetTopMoviesTest(TestCase):
    def setUp(self):
        Movie.objects.create(**terminator)
        Movie.objects.create(**kevin)
        Comment.objects.create(movie_id=Movie.objects.get(id=1), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=1), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')
        Comment.objects.create(movie_id=Movie.objects.get(id=2), message='test')

    def test_get_top_movies(self):
        response = client.get('/top/?date_from=2019-01-01&date_to=2020-01-01')

        self.assertEqual(response.data, [
            {
                'movie_id': 1,
                'rank': 2,
                'total_comments': 2
            },
            {
                'movie_id': 2,
                'rank': 1,
                'total_comments': 3
            }
        ])

        response = client.get('/top/?date_from=2019-01-01&date_to=2019-01-01')

        self.assertEqual(response.data, [
            {
                'movie_id': 1,
                'rank': 1,
                'total_comments': 0
            },
            {
                'movie_id': 2,
                'rank': 1,
                'total_comments': 0
            }
        ])

        response = client.get('/top/')

        self.assertEqual(response.data, {'error': 'You must specify date_from and date_to query parameters.'})
