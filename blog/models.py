from autoslug import AutoSlugField
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.


class Excerpt(models.Model):
    excerpt = models.CharField(max_length=40)

    def __str__(self):
        return self.excerpt


class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, default="/media/images/900x300.png")
    slug = AutoSlugField(populate_from='title', unique=True, unique_with='title', editable=False,
                         help_text="Slug will be generated automatically from the title of the post")
    time = models.DateTimeField(auto_now_add=True)
    excerpt_type = models.ForeignKey(Excerpt, on_delete=models.CASCADE, null=True, blank=True)
    context = models.CharField(max_length=20, null=True, blank=True)
    tags = TaggableManager(blank=True)
    time_to_read = models.IntegerField(default=12)
    # tag = models.CharField(max_length=100, null=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/900x300.png"

    @property
    def get_month_name(self):
        if self.time.month == 1:
            return 'January'
        elif self.time.month == 2:
            return 'February'
        elif self.time.month == 3:
            return 'March'
        elif self.time.month == 4:
            return 'April'
        elif self.time.month == 5:
            return 'May'
        elif self.time.month == 6:
            return 'June'
        elif self.time.month == 7:
            return 'July'
        elif self.time.month == 8:
            return 'August'
        elif self.time.month == 9:
            return 'September'
        elif self.time.month == 10:
            return 'October'
        elif self.time.month == 10:
            return 'November'
        elif self.time.month == 12:
            return 'December'

    def __str__(self):
        return self.title + ' by ' + self.user.username

    def get_absolute_url(self):
        return reverse("posts:posts", args=[str(self.slug)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    about = models.TextField(default="No information about this user")
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    desc = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(null=True, default="No Information About This User")
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="replies")
    time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.comment[0:12] + '... ' + " by " + self.user.username

