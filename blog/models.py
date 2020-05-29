from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.dispatch import receiver
import os


class Post(models.Model):
    class_choice = (
        ('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Fourth', 'Fourth'),
        ('Fifth', 'Fifth'),('Sixth', 'Sixth'), ('Seventh', 'Seventh'), ('Eighth', 'Eighth'),
        ('Nineth', 'Nineth'),('Tenth', 'Thenth'), ('Eleventh', 'Eleventh'), ('Twelveth', 'Twelveth'), ('All', 'All')
    )
    class_name = models.CharField(max_length=10, choices=class_choice, default= 'all')
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'blog_img/%d%m%Y', default='blogimg.jpg',blank=True)



    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)