from django.contrib.auth.models import AbstractUser
from django.db import models


class DeliveryCenter(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location


class Member(AbstractUser):
    delivery_center = models.ForeignKey(DeliveryCenter, on_delete=models.CASCADE, related_name='members')
    password = models.CharField(max_length=255)


class Position(models.Model):
    position = models.CharField(max_length=255)
    member = models.ManyToManyField(Member, db_constraint=False, related_name='positions')
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.position


class Project(models.Model):
    title = models.CharField(max_length=255)
    position = models.ManyToManyField(Position, db_constraint=False, related_name='projects')
    # technologies = models.ManyToManyField(Technology, db_constraint=False, related_name='projects')

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=255)
    project = models.ManyToManyField(Project, db_constraint=False, related_name='technologies')

    def __str__(self):
        return self.title
