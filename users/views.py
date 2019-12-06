
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import requests, json
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView

# Create your views here.
class UserView(View):
    pass