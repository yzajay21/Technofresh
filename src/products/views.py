from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from carts.models import Cart

from analytics.mixins import ObjectViewedMixin
from django_filters import FilterSet, CharFilter, NumberFilter
# Create your views here.

from .forms import VariationInventoryFormSet, ProductFilterForm
from .mixins import StaffRequiredMixin
from .models import Product, Variation, Category
import random

class ProductFeaturedListView(ListView):
	template_name ='products/product_list.html'

	def get_queryset(self,*args,**kwargs):
		request =self.request
		return Product.objects.featured()
	def get_context_data(self,*args,**kwargs):
		context = super(ProductFeaturedListView,self).get_context_data(*args,**kwargs)

		cart_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
	#queryset = Product.objects.all()
	template_name = "products/featured-detail.html"


	def get_queryset(self,*args,**kwargs):
		request =self.request
		return Product.objects.featured()

	def get_context_data(self,*args,**kwargs):
		context = super(ProductFeaturedDetailView,self).get_context_data(*args,**kwargs)

		cart_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	#def get_object(self,*args,**
class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/category_list1.html"




class CategoryDetailView(ObjectViewedMixin,DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()

		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products ).distinct()
		categories = Category.objects.all()
		context["products"] = products
		context ["categories"] = categories
		return context



class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				#if new_item.title:
				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				new_item.product = product
				new_item.save()
				
			messages.success(request, "Your inventory and pricing has been updated.")
			return redirect("products")
		raise Http404



class ProductFilter(FilterSet):
	title = CharFilter(name='title', lookup_type='icontains', distinct=True)
	category = CharFilter(name='categories__title', lookup_type='icontains', distinct=True)
	category_id = CharFilter(name='categories__id', lookup_type='icontains', distinct=True)
	min_price = NumberFilter(name='variation__price', lookup_type='gte', distinct=True) # (some_price__gte=somequery)
	max_price = NumberFilter(name='variation__price', lookup_type='lte', distinct=True)
	class Meta:
		model = Product
		fields = [
			'min_price',
			'max_price',
			'category',
			'title',
			'description',
		]


def product_list(request):
	qs = Product.objects.all()
	ordering = request.GET.get("ordering")
	if ordering:
		qs = Product.objects.all().order_by(ordering)
	f = ProductFilter(request.GET, queryset=qs)
	return render(request, "products/product_list.html", {"object_list": f })



	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context

class UserProductHistoryListView(LoginRequiredMixin,ListView):
	
	#template_name = "products/product_list.html"
	template_name = "products/user-history.html"

	def get_context_data(self,*args,**kwargs):
		context = super(UserProductHistoryListView,self).get_context_data(*args,**kwargs)

		cart_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self,*args,**kwargs):
		request = self.request
		views   = request.user.objectviewed_set.by_model(Product, model_queryset=False) 
		#viewed_ids	=[ x.object_id for x in views]
		return views


class ProductListView(ListView):
	#queryset = Product.objects.all()
	template_name = "products/product_list.html"

	def get_context_data(self,*args,**kwargs):
		context = super(ProductListView,self).get_context_data(*args,**kwargs)

		cart_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self,*args,**kwargs):
		request = self.request
		return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        instance = self.get_object()
        context['cart'] = cart_obj
        context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance




class ProductDetailView(DetailView):
	model = Product
	#template_name = "product.html"
	#template_name = "<appname>/<modelname>_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		#order_by("-title")
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
		return context


def product_detail_view(request,pk=None,*args,**kwargs):
	print(args)
	print(kwargs)
	
	#instance = get_object_or_404(Product,pk=pk)
	#try:
	#instance = Product.objects.get(id=pk)
	#except Product.DoesNotExist:
	#	print('no product here')
	#	raise Http404("Product doesn't exist")
	#except:
	#	print("huhhh?")
	#context = {
	#	'object' : instance
	#}
	#print(context)
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product doesn't exist")
	context = {
		'object' : instance
	}

	return render(request,"products/product_detail.html",context)