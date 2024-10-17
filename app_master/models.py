from django.db import models


TOWN_CHOICES = [
    ('Southbury', 'Southbury'),
    ('Middlebury', 'Middlebury'),
    ('Woodbury', 'Woodbury')
]

AREA_CHOICES = [
    ('Park & Recreation', 'Park & Recreation'),
    ('School', 'School'),
    ('Library', 'Library'),
    ('Senior Center', 'Senior Center'),
    ('Shopping/Stores', 'Shopping/Stores'),
    # ('Police Dept', 'Police Dept'),
    # ('Fire Dept', 'Fire Dept'),
    # ('Medical', 'Medical'),
    # ('Tax Collector', 'Tax Collector'),
    # ('Restaurants', 'Restaurants'),
    ('Environment', 'Environment'),
    ('Others', 'Others')
]

IS_ACTIVE_CHOICES = [
    (False, 'No'),
    (True, 'Yes')
]

# --
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    disclaimer_seen = models.BooleanField(default=False)
# --

class ProfaneIdeas(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=24)
    idea = models.TextField()
    town = models.CharField(
        max_length=30,
        choices=TOWN_CHOICES,
        default='Southbury'
    )
    area = models.CharField(
        max_length=40,
        choices=AREA_CHOICES,
        default='Park & Recreation'
    )

    def __str__(self):
        return self.area

    class Meta:
        db_table = 'profaneIdeas'
        
        
        
class ideas(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=24)
    idea = models.TextField()
    idea_id = models.AutoField(primary_key=True, unique=True)
    town = models.CharField(
        max_length=30,
        choices=TOWN_CHOICES,
        default='Southbury'
    )
    area = models.CharField(
        max_length=40,
        choices=AREA_CHOICES,
        default='Park & Recreation'
    )

    def __str__(self):
        return self.area

    class Meta:
        db_table = 'ideas'


class iSummary(models.Model):
    summary_id = models.AutoField(primary_key=True, unique=True)
    Summary = models.TextField()
    date_summarized = models.DateField(auto_now_add=True)
    isActive = models.BooleanField("isActive?", default=False, choices=IS_ACTIVE_CHOICES)
    ideas = models.ManyToManyField(ideas, related_name='i_summaries', through='ideaSummary')
    town = models.CharField(
        max_length=30,
        choices=TOWN_CHOICES,
        default='Southbury'
    )
    area = models.CharField(
        max_length=40,
        choices=AREA_CHOICES,
        default='Park & Recreation'
    )

    def __str__(self):
        return self.area

    class Meta:
        db_table = 'iSummary'


class IdeaSummary(models.Model):
    idea = models.ForeignKey(ideas, on_delete=models.CASCADE)
    Summary = models.ForeignKey(iSummary, on_delete=models.CASCADE)
    town = models.CharField(
        max_length=30,
        choices=TOWN_CHOICES,
        default='Southbury'
    )
    area = models.CharField(
        max_length=40,
        choices=AREA_CHOICES,
        default='Park & Recreation'
    )

    def __str__(self):
        return self.area

    class Meta:
        db_table = 'ideaSummary'

class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    details = models.TextField()
    date = models.DateField(auto_now_add=True)
    town = models.CharField(
    max_length=30,
    choices=TOWN_CHOICES,
    default='Southbury'
    )
    def __str__(self):
        return self.details
    
    class Meta:
        db_table = 'feedback'