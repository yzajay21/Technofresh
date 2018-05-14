from django.db import models

# Create your models here.
from billing.models import BillingProfile


ADDRESS_TYPES = (
	('billing','Billing'),
	('shipping','Shipping'),
)
class Address(models.Model):
	billing_profile		= models.ForeignKey(BillingProfile)
	address_type		= models.CharField(max_length=200,choices=ADDRESS_TYPES)
	address_line_1		= models.CharField(max_length=200)
	address_line_2		= models.CharField(max_length=200,null=True,blank=True)
	city				= models.CharField(max_length=120)
	country				= models.CharField(max_length=120,default='India')
	state				= models.CharField(max_length=120,default='Maharashtra')
	mobile				= models.IntegerField(help_text="Your Mobile Number")
	postal_code			= models.CharField(max_length=120)


	def __str__(self):
		return str(self.billing_profile)
	def get_address(self):
		return "{line1}\n{line2}\n{mobile}\n{city}\n{state},{postal}\n{country}".format(
			line1 = self.address_line_1,
			line2 = self.address_line_2,
			mobile= self.mobile,
			city  = self.city,
			state = self.state,
			postal= self.postal_code,
			country=self.country
			)