from django.contrib import admin

# Register your models here.

from .models import Bill, Rejected, User, Reexp, Appreciation, Termination, Offer, Intern

admin.site.register(Bill)
admin.site.register(User)
admin.site.register(Rejected)
admin.site.register(Reexp)
admin.site.register(Appreciation)
admin.site.register(Termination)
admin.site.register(Offer)
admin.site.register(Intern)