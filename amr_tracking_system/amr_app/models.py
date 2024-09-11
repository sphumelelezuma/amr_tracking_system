from django.db import models
from PIL import Image 
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# amr_app/models.py

from django.db import models


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default-profile.jpg')

    def __str__(self):
        return self.user.username

class Pathogen(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ResistanceData(models.Model):
    pathogen = models.ForeignKey(Pathogen, on_delete=models.CASCADE)
    resistance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_collected = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the built-in User model

    def __str__(self):
        return f"{self.pathogen.name} - {self.location.name} ({self.date_collected})"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    document = models.FileField(upload_to='post_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)

            # Resize the image to a specific size (e.g., 500x500)
            output_size = (1080, 1920)
            img = img.resize(output_size, Image.Resampling.LANCZOS)

            # Save it back to the image file
            img.save(self.image.path)

    def __str__(self):
        return self.content[:50]  # Display the first 50 characters of the post content

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    HEART = 'heart'

    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
        (HEART, 'Heart'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE, null=True, blank=True)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

