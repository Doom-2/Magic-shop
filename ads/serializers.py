from datetime import date
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ads.models import Location, User, Ad, Selection
from .validators import DomainBlackList


''' #################### Locations #################### '''


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


''' #################### Users #################### '''


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    # age = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'locations', 'total_ads']


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    birth_date = serializers.DateField(allow_null=True, required=False)
    age = serializers.SerializerMethodField()
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            DomainBlackList('rambler.ru')
        ]
    )

    class Meta:
        model = User
        fields = '__all__'

    def validate_birth_date(self, birth_date):

        today = date.today()
        age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 9:
            raise serializers.ValidationError("You're too young for this content")
        return birth_date

    def get_age(self, obj):
        today = date.today()
        if hasattr(obj.birth_date, "year"):
            age = today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
            return age

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(user.password)

        for location in self._locations:
            location_obj, created = Location.objects.get_or_create(
                name=location,
                defaults={
                    "lat": 0,
                    "lng": 0
                }
            )
            user.locations.add(location_obj)

        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "age", "locations"]

    def is_valid(self, raise_exception=False):

        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        user.set_password(self.initial_data['password'])

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(
                name=location,
                defaults={
                    "lat": 0,
                    "lng": 0
                }
            )
            user.locations.add(location_obj)

        for location in user.locations.all():
            if location.name not in self._locations:
                user.locations.remove(location)

        user.save()

        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


''' #################### Ads #################### '''


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]


class AdUpdateSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="first_name"
    )

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author_id', 'author', 'price', 'description', 'is_published', 'category_id', 'image']


''' #################### Selections #################### '''


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Ad.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):

        self._items = self.initial_data.pop("items", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        selection = Selection.objects.create(**validated_data)

        for item in self._items:
            if item not in Ad.objects.all().values_list("id", flat=True):
                print(f'Ad with id {item} not presented in Ads list')
                continue
            selection.items.add(item)

        return selection


class SelectionUpdateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Ad.objects.all(),
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = ['name', 'owner', 'items']

    def is_valid(self, *, raise_exception=False):
        self._items = self.initial_data.pop("items", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        selection = super().save()
        for item in self._items:
            if item not in Ad.objects.all().values_list("id", flat=True):
                print(f'Ad with id {item} not presented in source ads list and was excluded from query')
                continue
            selection.items.add(item)

        for item in Ad.objects.all().values_list("id", flat=True):
            if item not in self._items:
                selection.items.remove(item)

        return selection


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]
