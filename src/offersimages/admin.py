from django.contrib import admin

# Register your models here.
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ["title"]

    class Meta:
        model = Offer
admin.site.register(Offer,OfferAdmin)