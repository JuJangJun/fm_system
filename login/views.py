from django.shortcuts import render
# from access.views import getDatas


# Create your views here.
def show(request):
    return render(request, "login/index.html")
