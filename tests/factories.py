from ads.models import User, Category, Ad
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "test_pwd"
    first_name = "Test"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test_cat"
    slug = factory.fuzzy.FuzzyText(length=10)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "Test ad"
    description = "..."
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
