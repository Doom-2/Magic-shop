# Урок 31. Валидаторы и тестирование. 

1. Конвертация из csv в json c нужной структурой и возможностью 
последующей загрузки в таблицы БД произведена, .json файлы хранятся в /ads/fixtures

Для этого использовалась утилита csv2json.py

Формат использования:
```
python3 csv2json.py file_name.csv model_name
```

Пример:
python3 csv2json.py /datasets/categories.csv ads.Category

К имени исходного файла будет добавлено расширение .json

Формат вывода:
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

2. Вывод дополнительного поля total_ads с количеством опубликованных сообщений пользователя 
реализован 2-мя способами:

   - для списка пользователей - через метод annotate() c помощью фильтра и объектов специального класса Q
   - для отдельного пользователя - через обращение к полям модели объявления из модели пользователя с помощью параметра 'related_name'

3. Создание пользователя тестировать на Postman, т.к. если отправить POST-запрос /user/create/ из браузера, то это будет неизменяемый QueryDict

4. Управление доступом реализовано 3-мя способами:
   - для function-based views через декораторы @api_view() и @permission_classes() 
   - для class-based views на базе Django's GenericView через LoginRequiredMixin и UserPassesTestMixin
   - для class-based views на базе GenericAPIView DRF через атрибут класса permission_classes

5. Валидация:
   - поле 'price' модели Ad через встроенный валидатор MinValueValidator()
   - поле 'is_published' модели Ad через внешнюю функцию check_field_not_true()
   - поле 'birth_date' модели User через функцию сериализатора validate_<field_name>()
   - поле email модели User через пользовательский класс DomainBlackList() с наследованием от 
     класса EmailValidator и переопределением метода __call__()

6. Тесты:
   - для получения уникальных значений определенной длины поля 'slug' модели Category используется factory.fuzzy.FuzzyText(length=10)
   - для авторизации используется фикстура jwt_access_token(), которая возвращает access token созданного пользователя
   - при тестировании CRUD объявлений для получения данных в response используется response.json(), а не response.data
     потому что views для модели Ad написаны на базе Django's GenericView, а не DRF

7. Чтобы собственные валидаторы моделей Ad и Category работали в Django's CreateView для метода post сделана ручная проверка через full_clean():
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
    # Validation is ok we will save the instance
    instance.save()
```
Сохранение в БД происходит после успешной валидации модели.

8. Поле 'age' в модели User заменено на поле 'birth_date', а 'age' доступен в сериализаторе через SerializerMethodField() и метод get_age()
