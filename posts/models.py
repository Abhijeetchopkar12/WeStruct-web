from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


# Add following field to User dynamically
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_picture = models.ImageField(default='user.png')


    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_Author_signal(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)
        instance.author.save()

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    rating = models.IntegerField(default=0)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    Date = models.DateTimeField(auto_now_add=True)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['-Date']

    def publish(self):
        self.Date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()



class Contact_us(models.Model):
    massage_id = models.AutoField(primary_key=True)
    nmae = models.CharField(max_length=100)
    email = models.CharField(max_length=50,default="")
    phone_number = models.CharField(max_length=50,default="")
    subject = models.CharField(max_length=100,default="")
    massage = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.nmae