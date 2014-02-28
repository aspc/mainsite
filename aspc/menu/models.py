from django.db import models

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

    class Meta:
        ordering = ('date', 'dining_hall', 'meal')
        verbose_name_plural = 'Menus'