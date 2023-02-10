from rest_framework import serializers

from .models import User, Author, Post, Comment, MeanScore


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ['user', ]

    def create(self, validated_data):
        try:
            new_user = User(username=validated_data['username'],)
            new_user.set_password(validated_data['password'])
            new_user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удается создать пользователя. {e}')
        else:
            new_author = Author.objects.create(
                user=new_user,
                telegram_chat_id=validated_data['telegram_chat_id'],
                email=validated_data['email'],
            )
            new_author.save()
            return new_author


class PostSerializer(serializers.ModelSerializer):
    mean_score = serializers.ReadOnlyField(source='total_mean_score')

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['author', ]

    def create(self, validated_data):
        post = Post.objects.create(
            author=validated_data['author'],
            text=validated_data['text'],
        )
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['author', ]


class MeanScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeanScore
        fields = '__all__'
        read_only_fields = ['post', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['post', ]


