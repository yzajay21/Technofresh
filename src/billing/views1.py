from django.shortcuts import render

# Create your views here.
PAYU_PUB_KEY
def payment_method_view(request):
	if request.method == "POST":
		print(rquest.POST)
	return render(request,'billing/payment_method.html',{})
