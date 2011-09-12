from django.db import models

class Term(models.Model):
    """A college term"""
    start = models.DateField(unique=True)
    end = models.DateField(unique=True)
    
    class Meta:
        ordering = ['start']

    def __unicode__(self):
        return u"Term"
    
    def get_display_name(self):
        if self.start.month > 6:
            season = 'Fall'
        else:
            season = 'Spring'
        return '{0} {1}'.format(season, self.start.year)

# CourseGroup

# Department

# Program

# Area

# Professor

# Course

# Section

# Textbook

# Review
