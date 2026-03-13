from django.shortcuts import render

def search_view(request):
    return render(request, 'My_forum/search.html')
