# Урок 27. Знакомство с Django. 

Конвертация из csv в json c нужной структурой и возможностью 
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
