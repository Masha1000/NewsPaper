from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        all_post = Post.objects.filter(author=self.id)
        rating_post = sum([a.post_rating for a in all_post])
        rating_comment = sum([a.comment_rating for a in Comment.objects.filter(author=self.author)])
        rating_comment_post = sum([a.comment_rating for a in Comment.objects.filter(post__in=all_post)])

        self.author_rating = rating_post*3 + rating_comment_post + rating_comment
        self.save()

class Category(models.Model):
    categories = models.CharField(max_length = 100, unique = True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    News = 'NW'
    Article = 'AR'
    POST_TYPE = [
        (News, 'Новость'),
        (Article, 'Статья')
    ]

    type = models.CharField(max_length=2, choices=POST_TYPE, default='News')
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length = 255)
    text = models.TextField()
    post_rating = models.IntegerField(default = 0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        len_text = 124 if len(self.text) > 124 else len(self.text)
        return f'{self.text[:len_text]}...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default = 0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()