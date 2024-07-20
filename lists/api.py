from django.http import HttpRequest, HttpResponse, JsonResponse

from lists.forms import ExistingListItemForm
from lists.models import List

def list(request: HttpRequest, list_id: int) -> JsonResponse:
    list_ = List.objects.get(pk=list_id)

    if request.method == 'GET':    
        items = [dict(id=item.pk, text=item.text) for item in list_.item_set.all()]
        
        result = dict()
        for id, item in enumerate(items, 1):
            result[id] = item

        return JsonResponse(data=result, content_type='application/json')
    elif request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return JsonResponse(data=form.errors, content_type='application/json')