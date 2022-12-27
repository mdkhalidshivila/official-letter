from django.contrib import admin

# Register your models here.

from .models import Bill, Rejected, User, Reexp, Appreciation

admin.site.register(Bill)
admin.site.register(User)
admin.site.register(Rejected)
admin.site.register(Reexp)
admin.site.register(Appreciation)