from django.contrib import admin
from django.conf.urls import patterns
from django.contrib.auth.models import User
from django.shortcuts import render
from aspc.housing.models import Room, Review
from aspc.courses.models import CourseReview
import random


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'create_ts', ]
    exclude = ('room',)

    def get_urls(self):
        urls = super(ReviewAdmin, self).get_urls()
        extra_urls = patterns('',
            (r'^raffle/$', self.admin_site.admin_view(self.raffle_view))
        )
        return extra_urls + urls

    def raffle_view(self, request):
        from aspc.housing.forms import RaffleForm
        context = {}
        if request.GET:
            form = RaffleForm(request.GET)
            if form.is_valid():
                start = form.cleaned_data["start_date"]
                end = form.cleaned_data["end_date"]
                num = form.cleaned_data["num_winners"]
                reviews = list(Review.objects.filter(create_ts__range=[start, end])) + \
                    list(CourseReview.objects.filter(created_date__range=[start, end]))
                winner_reviews = random.sample(reviews, num)
                context.update({'winner_reviews': winner_reviews})
        else:
            form = RaffleForm()
        context.update({'form': form})
        return render(request, 'housing/raffle.html', context)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'floor', 'size', 'occupancy', 'reserved', 'suite']
    ordering = ['floor']


admin.site.register(Room, RoomAdmin)
admin.site.register(Review, ReviewAdmin)