from django.contrib import admin

# Register your models here.


from .models import Product, Variation, ProductImage, Category, ProductFeatured

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	max_num = 10

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0
	max_num = 10

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug']
	prepopulated_fields = {'slug': ('title',)}
	
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price','active','slug','featured']
	prepopulated_fields = {'slug':('title',),}
	list_editable = ['price', 'active','featured']
	inlines = [
		ProductImageInline,
		VariationInline,
	]
	ordering = ['title',]
	search_fields = ['title']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)



#admin.site.register(Variation)

admin.site.register(ProductImage)



admin.site.register(ProductFeatured)