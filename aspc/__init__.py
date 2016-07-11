# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from __future__ import absolute_import

# Set header for admin page
from django.contrib import admin
admin.site.site_header = admin.site.site_title = 'ASPC Admin Interface'