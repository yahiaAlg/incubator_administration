from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProjectMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_member')
    project = models.ForeignKey('administration.Project', on_delete=models.CASCADE, related_name='members')
    join_date = models.DateField(auto_now_add=True)
    skills = models.TextField(blank=True)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"

class ProjectLeader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_leader')
    projects = models.ManyToManyField('administration.Project', related_name='leaders')
    date_assigned = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Leader: {self.user.username}"
