from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

# Create your views here.
def home_page(request):
    form = ItemForm()
    return render(request, 'home.html', {'form': form})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST.get('text'), list=list_)
            return redirect(list_)
    form = ItemForm()
    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get('text'), list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})