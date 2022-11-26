from django.contrib import admin

from ads.models import Category, Location, User, Ad, Selection

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Selection)
