from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.

def opportunities(request):
    return render(request, "listopportunities.html")

def createOpportunity(request):
    return render(request, "create.html")
