from django.contrib import admin
from aspc.mentalhealth.models import (Insurance, Qualification, Specialty, Tag, Gender, Identity, SexualOrientation,
                                       Ethnicity, Therapist, MentalHealthReview)

admin.site.register(Insurance)
admin.site.register(Qualification)
admin.site.register(Specialty)
admin.site.register(Tag)
admin.site.register(Gender)
admin.site.register(Identity)
admin.site.register(SexualOrientation)
admin.site.register(Ethnicity)
admin.site.register(Therapist)
admin.site.register(MentalHealthReview)