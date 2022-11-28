# Урок 30. Пользователи: управление доступом и разделение ролей. 

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
