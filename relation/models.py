from django.db import models


class DeliveryCenter(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location


class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    delivery_center = models.ForeignKey(DeliveryCenter, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return self.name


class Position(models.Model):
    position = models.CharField(max_length=255)
    member = models.ManyToManyField(Member, related_name='positions')

    def __str__(self):
        return self.position


class Project(models.Model):
    title = models.CharField(max_length=255)
    position = models.ManyToManyField(Position, related_name='projects')

    def __str__(self):
        return self.title


class Technology(models.Model):
    title = models.CharField(max_length=255)
    project = models.ManyToManyField(Project, related_name='technologies')

    def __str__(self):
        return self.title
