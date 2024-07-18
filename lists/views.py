from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()

# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})
    
def new_list(request: HttpRequest) -> HttpResponseRedirect:
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})
    
def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

@require_POST
@login_required
def share_list(request: HttpRequest, list_id: int) -> HttpResponseRedirect:
    list_ = get_object_or_404(List, pk=list_id)
    email = request.POST.get('sharee')
    try:
        list_.shared_with.add(email=request.user.pk)
        list_.shared_with.add(email=email)
        return redirect(to=list_)
    except User.DoesNotExist:
        return HttpResponseBadRequest()