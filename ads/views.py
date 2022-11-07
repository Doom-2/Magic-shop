import json
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from ads.models import Ad, Category


def index(request):
    return HttpResponse('{"status": "ok"}', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ad.objects.all()

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        destination_data = json.loads(request.body)

        ad = Ad()
        ad.name = destination_data["name"]
        ad.author = destination_data["author"]
        ad.price = destination_data["price"]
        ad.description = destination_data["description"]
        ad.address = destination_data["address"]
        ad.is_published = destination_data["is_published"]

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        destination_data = json.loads(request.body)

        category = Category()
        category.name = destination_data["name"]

        try:
            category.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        category.save()
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })
