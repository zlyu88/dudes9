from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Technology(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title


class Member(AbstractUser):
    location_choices = (('lviv', 'lviv'), ('kyiv', 'kyiv'))
    delivery_center = models.CharField(max_length=10, choices=location_choices, default='lviv')
    password = models.CharField(max_length=255)

    @staticmethod
    def only_members():
        return Member.objects.filter(is_staff=0)

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(unique=True, max_length=255)
    members = models.ManyToManyField(Member, through='Relation', through_fields=('project', 'member'))
    technologies = models.ManyToManyField(Technology, db_constraint=False, related_name='projects')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)

    def active_relations(self):
        return Relation.objects.filter(project_id=self.id, date_left=None)

    def na_relations(self):
        return Relation.objects.all().exclude(project_id=self.id, date_left=None)

    def positions(self):
        return Relation.objects.filter(project_id=self.id, date_left=None).values('position').distinct()

    def __str__(self):
        return self.title


class Relation(models.Model):
    position_choices = (('developer', 'developer'), ('qa', 'qa'), ('hr', 'hr'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="relation")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="relation")
    position = models.CharField(max_length=10, choices=position_choices, default='developer')
    date_joined = models.DateTimeField(default=timezone.now)
    date_left = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('project', 'member', 'position')

    def __str__(self):
        return self.position
