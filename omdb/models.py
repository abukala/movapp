from django.db import models


class Movie(models.Model):
    Title = models.TextField()
    Year = models.TextField()
    Rated = models.TextField()
    Released = models.TextField()
    Runtime = models.TextField()
    Genre = models.TextField()
    Director = models.TextField()
    Writer = models.TextField()
    Actors = models.TextField()
    Plot = models.TextField()
    Language = models.TextField()
    Country = models.TextField()
    Awards = models.TextField()
    Poster = models.TextField()
    Ratings = models.TextField()
    Metascore = models.TextField()
    imdbRating = models.TextField()
    imdbVotes = models.TextField()
    imdbID = models.TextField()
    Type = models.TextField()
    DVD = models.TextField()
    BoxOffice = models.TextField()
    Production = models.TextField()
    Website = models.TextField()
    Response = models.TextField()


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

