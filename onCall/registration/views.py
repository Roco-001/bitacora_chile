from django.shortcuts import render, redirect
from django.contrib.auth import  logout #add this
from django.contrib import messages
# Create your views here.

def logout_request(request):
	logout(request)
	messages.info(request, "Has terminado tu sesión satisfactoriamente.")
	return redirect("bitacora:home")