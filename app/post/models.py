from django.db.models import Avg
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    text = models.TextField()
    date_publish = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username

    def total_mean_score(self):
        mean = MeanScore.objects.filter(post=self).aggregate(avg=Avg('score'))
        return mean


class MeanScore(models.Model):
    score = models.CharField(max_length=250, choices=((1,1), (2,2), (3,3), (4,4), (5,5)), default=0)
    post= models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=score)

    def __str__(self):
        return self.score


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_autor = models.CharField(max_length=20, blank=True)
    text = models.CharField(max_length=255)
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment_autor

