from django.contrib import admin
from aspc.sagelist.models import BookSale

class BookSaleAdmin(admin.ModelAdmin):
    list_display = ("title",  "authors", "price", "condition", "condition", 
      "edition", "seller", "buyer")

admin.site.register(BookSale, BookSaleAdmin)
