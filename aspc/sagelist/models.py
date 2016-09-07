from django.db import models
from django.contrib.auth.models import User
from aspc.activityfeed.signals import new_activity, delete_activity
from aspc.courses.models import Course
from amazon.api import AmazonAPI
import datetime
from aspc.settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG
import json

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

class BookSale(models.Model):
    CONDITIONS = (
        (0, "like new"),
        (1, "very good"),
        (2, "good"),
        (3, "usable"),
    )

    # See http://www.pomona.edu/administration/sustainability/programs/recoop.aspx
    # Record these so ReCoop listings can be disabled on these days
    RECOOP_SALE_DATES = [
        datetime.date(2014, 8, 31),
        datetime.date(2014, 9, 1),
        datetime.date(2014, 9, 2),
        datetime.date(2014, 9, 3),
        datetime.date(2014, 9, 4)
    ]

    """Model representing a sale of a textbook"""
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, verbose_name="Author(s)")
    course = models.ForeignKey(Course, blank=True, null=True)
    isbn = models.CharField(max_length=20, null=True, blank=True, verbose_name="ISBN")
    edition = models.CharField(max_length=30, null=True, blank=True)
    condition = models.IntegerField(choices=CONDITIONS)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_recoop = models.BooleanField(default=False)
    recoop_id = models.IntegerField(unique=True, null=True)

    seller = models.ForeignKey(User, related_name="book_sales_set")
    buyer = models.ForeignKey(User, null=True, blank=True, related_name="book_purchases_set")

    posted = models.DateTimeField(auto_now_add=True)

    amazon_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['posted']

    def __unicode__(self):
        return u"BookSale: {0} by {1} ({2})".format(self.title, self.authors, self.seller.username)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(BookSale, self).save(*args, **kwargs)
        if created and not self.is_recoop:
            new_activity.send(sender=self, category="sagelist", date=self.posted)

    def update_amazon_info(self):
        if not self.isbn:
            return
        products = amazon.search_n(1,Keywords=self.isbn.replace('-',''), SearchIndex='Books')
        if not len(products):
            return
        amazon_info = {}
        amazon_info['price'] = products[0].price_and_currency[0]
        amazon_info['image_url'] = products[0].large_image_url
        amazon_info['url'] = products[0].offer_url
        amazon_info['description'] = products[0].editorial_review
        self.title = products[0].title
        self.authors = products[0].author
        if not self.edition:
            self.edition = products[0].edition
        self.amazon_info = json.dumps(amazon_info)
        self.save()

    def get_amazon_attribute(self, attribute):
        if not self.amazon_info:
            return None
        amazon_info = json.loads(self.amazon_info)
        return amazon_info.get(attribute)

    def amazon_price(self):
        return self.get_amazon_attribute('price')

    def url(self):
        return self.get_amazon_attribute('url')

    def image_url(self):
        return self.get_amazon_attribute('image_url')

    def description(self):
        return self.get_amazon_attribute('description')

    def money_saved(self):
        if not self.amazon_price() or self.price > self.amazon_price():
            return 0
        return self.amazon_price() - float(self.price)

    def delete(self, *args, **kwargs):
        delete_activity.send(sender=self)
        super(BookSale, self).delete(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('sagelist_detail', [self.id])

    @property
    def is_frozen(self):
        return self.is_recoop and datetime.date.today() in self.RECOOP_SALE_DATES