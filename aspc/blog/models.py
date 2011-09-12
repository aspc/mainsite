from django.db import models

class Post(models.Model):
    """A blog post (attached to a senator via Appointment)"""
    
    author = models.ForeignKey('senate.Appointment')
    title = models.CharField(max_length=80)
    body = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    
    class Meta:
        ordering = ['posted']

    def __unicode__(self):
        return u"{0} by {1} ({2}) on {3}".format(
            self.title,
            self.author.user.get_full_name(),
            self.author.position.title,
            self.posted,
        )

    @models.permalink
    def get_absolute_url(self):
        return ('Post', [self.id])