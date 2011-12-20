from django.contrib import admin
from aspc.eatshop.models import Business, Hours

class HoursInline(admin.TabularInline):
    model = Hours

class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "phone", "www", 
                    "has_discount", "flex", "claremont_cash")
    inlines = [HoursInline, ]

admin.site.register(Business, BusinessAdmin)
