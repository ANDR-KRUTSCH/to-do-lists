from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from rest_framework import serializers

from lists.forms import ExistingListItemForm
from lists.models import List, Item

# def list(request: HttpRequest, list_id: int) -> JsonResponse:
#     list_ = List.objects.get(pk=list_id)

#     if request.method == 'GET':    
#         items = [dict(id=item.pk, text=item.text) for item in list_.item_set.all()]
        
#         result = dict()
#         for id, item in enumerate(items, 1):
#             result[id] = item

#         return JsonResponse(data=result, content_type='application/json')
#     elif request.method == 'POST':
#         form = ExistingListItemForm(for_list=list_, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=201)
#         return JsonResponse(data=form.errors, content_type='application/json')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('text',)

@require_GET
def get_items(request: HttpRequest, list_pk: int) -> JsonResponse:
    list_ = List.objects.get(pk=list_pk)

    items = list_.item_set.all()

    serializer = ItemSerializer(instance=items, many=True)

    return JsonResponse(data=serializer.data, safe=False, content_type='application/json')

@require_POST
def post_item(request: HttpRequest, list_pk: int) -> JsonResponse:
    list_ = List.objects.get(pk=list_pk)

    form = ExistingListItemForm(for_list=list_, data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse(status=201)
    return JsonResponse(data=form.errors, content_type='application/json')