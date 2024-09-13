import markdown
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
import os


class ErModelView(View):
    def get(self, request):
        #   # Caminho para o arquivo Markdown
        #   filepath = os.path.join(settings.BASE_DIR, 'README.md')
        #
        #   # Ler o conteúdo do arquivo
        #   with open(filepath, 'r') as file:
        #       text = file.read()
        #
        # # Converter Markdown para HTML
        #   html_content = markdown.markdown(text)
        #
        #   # Renderizar o template com o conteúdo HTML do Markdown
        #   context = {
        #       'markdown_content': html_content,
        #   }
        return render(request, 'er_model.html')
