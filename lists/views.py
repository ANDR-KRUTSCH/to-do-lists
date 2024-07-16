from django.shortcuts import render, redirect
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm
from django.http import HttpRequest, HttpResponse

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request: HttpRequest, list_id) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})
    
def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    return render(request, 'my_lists.html')