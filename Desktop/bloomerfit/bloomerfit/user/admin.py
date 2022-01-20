from django.contrib import admin
from .models import User, StatsLogin, Contact
# Register your models here.

admin.site.register(User),
admin.site.register(StatsLogin)
admin.site.register(Contact)