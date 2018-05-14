from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm,RegisterForm
from products.models import ProductFeatured, Product,Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from banner.models import Photo
from offersimages.models import Offer
def home_page(request):
    featured = ProductFeatured.objects.filter(active=True).order_by("?")
    photos    = Photo.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all().order_by("?")[:8]
    products2 = Product.objects.filter(featured=True).order_by("?")
    offers    = Offer.objects.all()

    paginator = Paginator(products2, 4)
    page 	  = request.GET.get('page')

    try :
    	items = paginator.page(page)
    except PageNotAnInteger:
    	items = paginator.page(1)
    except EmptyPage:
    	items = paginator.page(paginator.num_pages)

    index 	    = items.number - 1
    max_index   = len(paginator.page_range)
    start_index = index - 5 if index >=5 else 0
    end_index	= index + 5 if index <= max_index -5 else max_index
    page_range  = paginator.page_range[start_index:end_index]
    context = {
		#"title": title,
		#"form": form,
        "offers":offers,
        "photos":photos,
		"featured":featured,
		"products":products,
		"products2":products2,
		"items" 	:items,
		"page_range": page_range,
		"categories":categories
	}
    return render(request,"home.html",context)

def about(request):
	return render(request,"about.html",{})

