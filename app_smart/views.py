from django.shortcuts import render
from django.http import HttpResponse

#Create you views here:
def abre_index(request):
    mensagem = "Hello world."
    return HttpResponse(mensagem)