from django.contrib import admin

from ads.models import Category, Location, User, Ad

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Ad)
