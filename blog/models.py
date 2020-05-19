from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    class_choice = (
        ('First', 'first'), ('Second', 'second'), ('Third', 'third'), ('Fourth', 'fourth'),
        ('Fifth', 'fifth'),('Sixth', 'sixth'), ('Seventh', 'seventh'), ('Eighth', 'eighth'),
        ('Nineth', 'nineth'),('Tenth', 'thenth'), ('Eleventh', 'eleventh'), ('Twelveth', 'twelveth'), ('all', 'all')
    )
    class_name = models.CharField(max_length=10, choices=class_choice, default= 'all')
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})