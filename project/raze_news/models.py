from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        author_all_post_rating = self.post_set.all().aggregate(post_rating=Sum('post_rating'))
        author_all_comment_rating = self.user.comment_set.all().aggregate(comment_rating=Sum('comment_rating'))

        all_comment_rating = Comment.objects.filter(post__author=self.id)
        return author_all_post_rating * 3 + author_all_comment_rating + all_comment_rating


sport = 'SP'
politics = "PL"
education = "ED"
culture = "CU"

CATEGORIES = [
    (sport, 'Спорт'),
    (politics, 'Политика'),
    (education, 'Образование'),
    (culture, 'Культура')
]


class Category(models.Model):
    name_category = models.CharField(max_length=2, choices=CATEGORIES, unique=True)


article = "A"
news = "N"
KIND = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Post(models.Model):
    title = models.CharField(max_length=255)
    time_in = models.DateTimeField(auto_now_add=True)
    post_kind = models.CharField(max_length=2, choices=KIND, default=news)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory')
    post_rating = models.FloatField(default=0.0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.dislikes -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
