from django.db import models
from rest_framework import serializers

class FrankManager(models.Manager):
    def get_queryset(self):
        return super(FrankManager, self).get_queryset().filter(dining_hall='frank')

class FraryManager(models.Manager):
    def get_queryset(self):
        return super(FraryManager, self).get_queryset().filter(dining_hall='frary')

class OldenborgManager(models.Manager):
    def get_queryset(self):
        return super(OldenborgManager, self).get_queryset().filter(dining_hall='oldenborg')

class ScrippsManager(models.Manager):
    def get_queryset(self):
        return super(ScrippsManager, self).get_queryset().filter(dining_hall='scripps')

class MuddManager(models.Manager):
    def get_queryset(self):
        return super(MuddManager, self).get_queryset().filter(dining_hall='mudd')

class CmcManager(models.Manager):
    def get_queryset(self):
        return super(CmcManager, self).get_queryset().filter(dining_hall='cmc')

class PitzerManager(models.Manager):
    def get_queryset(self):
        return super(PitzerManager, self).get_queryset().filter(dining_hall='pitzer')

class Menu(models.Model):
    CHARFIELD_MAX_LENGTH = 255
    DINING_HALLS = (
        ('frank', 'Frank'),
        ('frary', 'Frary'),
        ('oldenborg', 'Oldenborg'),
        ('scripps', 'Scripps'),
        ('mudd', 'Mudd'),
        ('cmc', 'CMC'),
        ('pitzer', 'Pitzer')
    )
    MEALS = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('brunch', 'Brunch')
    )
    DAYS = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday')
    )

    dining_hall = models.CharField(max_length=CHARFIELD_MAX_LENGTH, choices=DINING_HALLS)
    meal = models.CharField(max_length=CHARFIELD_MAX_LENGTH, choices=MEALS)
    day = models.CharField(max_length=CHARFIELD_MAX_LENGTH, choices=DAYS)
    food_items = models.TextField()

    objects = models.Manager()
    frank_meals = FrankManager()
    frary_meals = FraryManager()
    oldenborg_meals = OldenborgManager()
    scripps_meals = ScrippsManager()
    mudd_meals = MuddManager()
    cmc_meals = CmcManager()
    pitzer_meals = PitzerManager()

    class Meta:
        ordering = ('day', 'dining_hall', 'meal')
        verbose_name_plural = 'Menus'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'dining_hall', 'day', 'meal', 'food_items')