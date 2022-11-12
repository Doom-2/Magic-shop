# Урок 28. Работа с ORM в Django. 

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
