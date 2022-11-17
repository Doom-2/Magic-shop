from rest_framework import serializers
from ads.models import Ad, Category, User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'locations', 'total_ads']


class UserCreateSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):

        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            location_obj, created = Location.objects.get_or_create(
                name=location,
                defaults={
                    "lat": 0,
                    "lng": 0
                }
            )
            user.locations.add(location_obj)

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

        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

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

        return user


class UserDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id"]
