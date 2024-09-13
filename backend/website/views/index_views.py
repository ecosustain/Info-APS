import markdown
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
import os


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
