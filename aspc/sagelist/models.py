from django.db import models
from django.contrib.auth.models import User

class BookSale(models.Model):
    CONDITIONS = (
        (0, "like new"),
        (1, "very good"),
        (2, "good"),
        (3, "usable"),
    )
    """Model representing a sale of a textbook"""
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, verbose_name="Author(s)")
    isbn = models.CharField(max_length=20, null=True, blank=True, verbose_name="ISBN")
    edition = models.CharField(max_length=20, null=True, blank=True)
    condition = models.IntegerField(choices=CONDITIONS)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    seller = models.ForeignKey(User, related_name="book_sales_set")
    buyer = models.ForeignKey(User, null=True, blank=True, related_name="book_purchases_set")
    
    posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['posted']

    def __unicode__(self):
        return u"BookSale: {0} by {1} ({2})".format(self.title, self.authors, self.seller.username)

    @models.permalink
    def get_absolute_url(self):
        return ('sagelist_detail', [self.id])