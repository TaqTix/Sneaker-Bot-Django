from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index_view(request):
    return render(request, 'index.html')

'''def store_view(request):
    return render(request, 'store.html')'''

def doc_view(request):
    return render(request, 'docs.html') #need to create docs.html