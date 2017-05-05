from django.contrib.auth.models import AbstractUser
from django.db import models


class DeliveryCenter(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location


class Technology(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Member(AbstractUser):
    delivery_center = models.ForeignKey(DeliveryCenter, on_delete=models.CASCADE, related_name='members')
    password = models.CharField(max_length=255)


class Position(models.Model):
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.position


class Project(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(Member, through='Relation', through_fields=('project', 'member'))
    technologies = models.ManyToManyField(Technology, db_constraint=False, related_name='projects')

    def __str__(self):
        return self.title


class Relation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="relation")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="relation")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="relation")
