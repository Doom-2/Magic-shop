import json
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, User, Location
from ads.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, \
    LocationSerializer
from magic_shop.settings import TOTAL_ON_PAGE


def index(request):
    return HttpResponse('{"status": "ok"}', status=200)


''' #################### Ads #################### '''


# Get all ads
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        object_list = self.object_list.select_related("author", "category").order_by("-price")

        cat_id = request.GET.getlist("cat", None)
        if cat_id:
            object_list = object_list.filter(
                category_id__in=cat_id
            )

        ad_part_name = request.GET.get("text", None)
        if ad_part_name:
            object_list = object_list.filter(
                name__contains=ad_part_name
            )

        location_name = request.GET.get("location", None)
        if location_name:
            object_list = object_list.filter(
                author__locations__name__icontains=location_name
            )

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from and not price_to:
            object_list = object_list.filter(
                price__gte=price_from
            )
        elif not price_from and price_to:
            object_list = object_list.filter(
                price__lte=price_to
            )
        elif price_from and price_to:
            object_list = object_list.filter(
                Q(price__gte=price_from) & Q(price__lte=price_to)
            )

        paginator = Paginator(object_list, TOTAL_ON_PAGE)
        page_number = int(request.GET.get("page", 1))
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author.id,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category.id,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": ads,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }
        return JsonResponse(response, safe=False)


# Get a single ad
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category.id,
        })


# Create a new ad
@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            author_id=ad_data["author_id"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            image=ad_data["image"],
            category_id=ad_data["category_id"]
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category.id,
            "image": ad.image.url if ad.image else None
        })


# Update an existing ad
@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        if "name" in ad_data.keys():
            self.object.name = ad_data["name"]
        if "author_id" in ad_data.keys():
            self.object.author_id = ad_data["author_id"]
        if "price" in ad_data.keys():
            self.object.price = ad_data["price"]
        if "description" in ad_data.keys():
            self.object.description = ad_data["description"]
        if "category_id" in ad_data.keys():
            self.object.category_id = ad_data["category_id"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "image": self.object.image.url if self.object.image else None
        })


# Delete an existing ad
@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=204)


# Add or replace an image in the add
@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "image": self.object.image.url if self.object.image else None
        })


''' #################### Categories #################### '''


# Get all categories
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        object_list = self.object_list.order_by("name")

        response = []
        for category in object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)


# Get a single category
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


# Create a new category
@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)

        cat = Category.objects.create(
            name=cat_data["name"]
        )

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


# Update an existing category
@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)

        if "name" in cat_data.keys():
            self.object.name = cat_data["name"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


# Delete an existing category
@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=204)


''' #################### Users #################### '''


# Get all users
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Get a single user
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# Create a new user
# @method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# Update an existing user
# @method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


# Delete an existing user
# @method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


''' #################### Locations #################### '''


# Get all locations
class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
