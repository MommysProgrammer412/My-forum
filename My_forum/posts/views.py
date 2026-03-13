from django.shortcuts import render

def index(request):
    '''функция для запуска каркаса'''
    return render(request, 'base.html')