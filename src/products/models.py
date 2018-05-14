from django.db.models import Q
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from technofresh.utils import unique_slug_generator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True,active= True)
	def search(self, query):
		lookups = (Q(title__icontains=query) | 
			Q(description__icontains=query) |
			Q(tag__title__icontains=query))
		return self.filter(lookups).distinct()

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model,using=self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self):
		return self.get_queryset().featured()
		
	def get_by_id(self,id):
		qs = self.get_queryset().filter(id=id)
		if qs.count == 1:
			return qs.first()
		return None 
	def search(self, query):
		return self.get_queryset().active().search(query)
	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories__in=instance.categories.all())
		products_two = self.get_queryset().filter(default=instance.default)
		qs = (products_one | products_two).exclude(id=instance.id).distinct()
		return qs

class Product(models.Model):
	title       =  models.CharField(max_length=120)
	description =  models.TextField(blank=True, null=True)
	slug 	 	=  models.SlugField(max_length=200,blank=True,unique=True)
	price 		=  models.DecimalField(decimal_places=2, max_digits=20)
	active 		=  models.BooleanField(default=True)
	categories  =  models.ManyToManyField('Category', blank=True)
	default     =  models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
	featured    =  models.BooleanField(default= False)
	objects     = ProductManager()

	class Meta:
		ordering = ["-title"]

	def __str__(self): #def __str__(self):
		return self.title 

	def get_absolute_url(self):
		return reverse("products:detail", kwargs={"slug": self.slug})


	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		return img #None




class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True) #refer none == unlimited amount

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_html_price(self):
		if self.sale_price is not None:
			html_text = "<span class='sale-price'> ₹ %s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
		else:
			html_text = "<span class='price'> %s</span>" %(self.price)
		return mark_safe(html_text)

	def get_absolute_url(self):
		return self.product.get_absolute_url()

	#def add_to_cart(self):
		#return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

	#def remove_from_cart(self):
		#return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

	def get_title(self):
		return "%s - %s" %(self.product.title, self.title)



def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price
		new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)

def product_pre_save_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug =  unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender=Product)

def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to)

	image_thumbnail = ImageSpecField(source='image',
								processors=[ResizeToFill(100,50)],
								format="JPEG",
								options={'quality':70})

	def __str__(self):
		return self.product.title

# Product Category

def image_upload_to_category(instance, filename):
	title = instance.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "categories/%s/category/%s" %(slug, new_filename)



class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug })



def image_upload_to_featured(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "products/%s/featured/%s" %(slug, new_filename)




class ProductFeatured(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to_featured)
	title = models.CharField(max_length=120, null=True, blank=True)
	text = models.CharField(max_length=220, null=True, blank=True)
	text_right = models.BooleanField(default=False)
	text_css_color = models.CharField(max_length=6, null=True, blank=True)
	show_price = models.BooleanField(default=False)
	#make_image_background = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.product.title





