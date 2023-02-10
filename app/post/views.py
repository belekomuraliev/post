from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
import telebot
from .models import Author, Post, Comment, MeanScore
from .serializers import AuthorSerializer, PostSerializer, PostUpdateSerializer, CommentSerializer, MeanScoreSerializer

bot = telebot.TeleBot('5346721464:AAE-3hUao1oC03pUdacSIcf-sU1HryxjfUg', parse_mode=None)


class AuthorView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication, ]


class PostViewSet(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        obj = serializer.save(
            author=self.request.user.author,
        )
        bot.send_message(self.request.user.author.telegram_chat_id, f" Пост ' {obj.text} ' был успешно добавлен")


class PostUpdateRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))


class MeanScoreCreateAPIView(generics.ListCreateAPIView):
    queryset = MeanScore.objects.all()
    serializer_class = MeanScoreSerializer
    pagination_class = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get('post_id'),
        )


class MeanScoreDetailRetUpDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeanScore.objects.all()
    serializer_class = MeanScoreSerializer
    pagination_class = [IsAdminUser, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs.get('post_id'),
         )


class CommentRetrieveDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser, ]

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))

