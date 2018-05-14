from django.shortcuts import render
from .models import Offer




def offers_list(request):
    queryset =Offer.objects.all()
    context = {
            "photos":queryset,      
    }
    return render(request,"offer.html",context)