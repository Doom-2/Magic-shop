import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ads.models import Ad, Category, User, Location, Selection
from ads.permissions import SelectionUpdateDeletePermission, AdUpdateDeletePermission
from ads.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, \
    LocationSerializer, SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer, \
    SelectionUpdateSerializer, SelectionDestroySerializer, AdUpdateSerializer
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
@api_view()
@permission_classes([IsAuthenticated])
def ad_detail_view(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

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


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [AdUpdateDeletePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    success_url = "/"

    def test_func(self):
        obj = self.get_object()
        print(obj.author)
        return obj.author == self.request.user

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
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# Update an existing user
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


# Delete an existing user
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


''' #################### Locations #################### '''


# Get all locations
class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


''' #################### Selections #################### '''


# Get all selections
class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


# Get a single selection
class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated]


# Create a new selection
class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


# Update an existing selection
class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [SelectionUpdateDeletePermission]


# Delete an existing selection
class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDestroySerializer
    permission_classes = [SelectionUpdateDeletePermission]
