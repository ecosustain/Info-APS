import os

import markdown
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class AutomacaoView(View):
    def get(self, request):
        return render(request, "automacao.html")
