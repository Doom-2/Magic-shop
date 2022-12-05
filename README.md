# Magic shop

### An API with bulletin board logic made on Django and DRF

1. Views inheritance
    - Ads

          list - generic view ListView

          detail - function based view

          create - generic view CreateView

          update - DRF UpdateAPIView

          delete - generic view DeleteView

    - Categories

          Django's generic views

    - Users

          DRF Generic API views

    - Locations

          DRF ViewSet

    - Selections

          DRF Generic API views


2. Convert from `csv` to `json` with `csv2json.py`

Usage: `python3 csv2json.py file_name.csv model_name`

Example: `python3 csv2json.py /datasets/categories.csv ads.Category`

Once executed, the `.json` extension will be added to the source file.

Output format:

```
[
  {
    "model": "myapp.person",
    "pk": 1,
    "fields": {
      "first_name": "John",
      "last_name": "Lennon"
    }
  },
  {
    "model": "myapp.person",
    "pk": 2,
    "fields": {
      "first_name": "Paul",
      "last_name": "McCartney"
    }
  }
]
```

3. An aditional field `total_ads` for each user, reflecting the quantity of his published ads (is_published = True)
   was
   realised by 2 steps:

    - in model 'Ad' an option `related_name` of field 'author' was added
    - in model 'User' a property `@total_ads` with filter and count logic was added


4. Creating a new user should be tested through 'Postman' app because if you test it through web browser an
   `AttributeError` `This QueryDict instance is immutable` will occur.


5. Access control is implemented in 3 ways:
    - for function-based views through `@api_view()` and `@permission_classes()` decorators
    - for Django's class-based generic views through inheritance from `LoginRequiredMixin` and `UserPassesTestMixin`
      classes
    - for DRF class-based generic views through `permission_classes` attribute


6. Validation:
    - field `price` of model 'Ad' through built-in `MinValueValidator()`
    - field `is_published` of model 'Ad' through `check_field_not_true()` function
    - field `birth_date` of model 'Ad' through function `validate_<field_name>()` in `UserCreateSerializer`
    - field `email` of model 'User' through custom `Domain BlackList` class, inherited from `EmailValidator` class and
      overridden `__call__()` method

   > Notice:
   > Field `age` in 'User' model was replaced with field `birth_day`, while `age` has become available in UserSerializer
   through `SerializerMethodField()` and `get_age()` method.

7. Tests:
    - the `jwt_access_token()` fixture is used for authentication that returns an access token of the newly created test
      user
    - `response.json()` instead of `response.data` is used when testing a CRUD for 'Ad' model because views created
      using
      Django's generic views rather than DRF 'generic views'
    - `factory.fuzzy.FuzzyText(length=10)` is used to get unique values of a certain length of the 'slug' field of the
      Category model.


8. To make the native and external validators of the Ad and Category models work, in Django's 'CreateView' of these
   models, a manual check was made for the post method via `full_clean()` using following template:

```
from django.core.exceptions import ValidationError
form app.models import MyModel

instance = MyModel(name="Some Name", size=15)
try:
    instance.full_clean()
except ValidationError as e:
    # Do something when validation is not passing
    return JsonResponse(e.message_dict, status=422)
else:
    # Validation is ok we will save the instance into DB
    instance.save()
```

9. API documentation with Swagger UI available on ['api/schema/docs/'](http://localhost:8000/api/schema/docs/). Make
   sure that the server is running before clicking the link.
