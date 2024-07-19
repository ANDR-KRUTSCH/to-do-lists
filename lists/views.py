from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import View, FormView, DetailView

from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()

# Create your views here.
class HomePage(FormView):
    form_class = ItemForm
    template_name = 'home.html'

# def home_page(request: HttpRequest) -> HttpResponse:
#     return render(request, 'home.html', {'form': ItemForm()})

class ViewList(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        list_ = get_object_or_404(klass=List, id=self.args[0])
        form = ExistingListItemForm(for_list=list_)
        if request.method == 'POST':
            form = ExistingListItemForm(for_list=list_, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(to=list_)
        return render(request=request, template_name='list.html', context={'list': list_, 'form': form})

# def view_list(request: HttpRequest, list_id: int) -> HttpResponse | HttpResponseRedirect:
#     list_ = List.objects.get(id=list_id)
#     form = ExistingListItemForm(for_list=list_)
#     if request.method == 'POST':
#         form = ExistingListItemForm(for_list=list_, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(to=list_)
#     return render(request=request, template_name='list.html', context={'list': list_, 'form': form})

class NewList(FormView):
    form_class = NewListForm
    template_name = 'home.html'

    def form_valid(self, form: NewListForm) -> HttpResponse:
        list_ = form.save(owner=self.request.user)
        return redirect(to=list_)
    
# def new_list(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
#     form = NewListForm(data=request.POST)
#     if form.is_valid():
#         list_ = form.save(owner=request.user)
#         return redirect(to=list_)
#     return render(request=request, template_name='home.html', context={'form': form})

class MyLists(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        email = self.args[0]
        owner = get_object_or_404(klass=User, email=email)
        return render(request=request, template_name='my_lists.html', context={'owner': owner})
  
# def my_lists(request: HttpRequest, email: str) -> HttpResponse:
#     owner = User.objects.get(email=email)
#     return render(request=request, template_name='my_lists.html', context={'owner': owner})

class ShareList(View, LoginRequiredMixin):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        list_ = get_object_or_404(klass=List, pk=self.args[0])
        email = request.POST.get('sharee')
        try:
            list_.shared_with.add(email=request.user.pk)
            list_.shared_with.add(email=email)
            return redirect(to=list_)
        except User.DoesNotExist:
            return HttpResponseBadRequest()


# @require_POST
# @login_required
# def share_list(request: HttpRequest, list_id: int) -> HttpResponseRedirect | HttpResponseBadRequest:
#     list_ = get_object_or_404(klass=List, pk=list_id)
#     email = request.POST.get('sharee')
#     try:
#         list_.shared_with.add(email=request.user.pk)
#         list_.shared_with.add(email=email)
#         return redirect(to=list_)
#     except User.DoesNotExist:
#         return HttpResponseBadRequest()