# Путевые заметки

Дневник путешествий на Python с веб-интерфейсом на Django: поездки,
путешественники и заметки по дням.

## 1. Назначение проекта

Приложение помогает путешественнику вести записи о поездках: хранить
маршруты, фиксировать впечатления по дням и находить их после поездки.
Проект развивается поэтапно: консольная версия (ПР1–ПР3) дополнена
веб-интерфейсом на Django (ПР5), а веб-страницы переведены на систему
шаблонов Django (ПР6).

**Целевая аудитория:** путешественники, любители походов, travel-блогеры.

## 2. Используемые технологии

- Python 3.11+;
- Django 5.2 (LTS);
- Django Template Language (DTL);
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3.3 (локальная копия в `homepage/static/homepage/css/`);
- JSON для хранения данных;
- Git, pytest, flake8.

## 3. Предметная область

Основные сущности (Python-классы в пакете `models/`):

- **Trip** — поездка: `id`, `title`, `country`, `start_date`,
  `end_date`; свойство `duration_days`, методы `lasts_at_least()`,
  `includes_day()`;
- **Traveler** — путешественник: `id`, `name`, `email`;
- **Note** — заметка: `id`, `trip` (объект `Trip`), `note_date`,
  `traveler` (объект `Traveler`), `text`, `is_archived`; метод
  `archive()`.

Правила: заметку можно создать только на день поездки; на один день
поездки — одна активная заметка; архивная заметка день не блокирует.

Данные хранятся в JSON-файлах `data/trips.json`,
`data/travelers.json`, `data/notes.json`. В JSON заметка хранит
идентификаторы `trip_id` и `traveler_id`; при загрузке
`storage.py` восстанавливает ссылки на объекты.

**На текущем этапе:** данные хранятся в JSON, Django ORM и база данных
приложения не используются, веб-формы пока не реализованы. Работа с
базой данных и формами относится к следующим практическим работам.

## 4. Структура проекта

```text
travel_notes/
├── README.md
├── requirements.txt
├── manage.py
├── main.py                  # консольная версия (ПР3)
├── storage.py               # JSON <-> объекты
├── utils.py                 # безопасный ввод
├── pytest.ini
├── .flake8
│
├── travelnotes/             # настройки и маршрутизация Django
│   ├── settings.py
│   └── urls.py
│
├── templates/               # шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
│
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/index.html
│   ├── urls.py
│   └── views.py
│
├── trips/
│   ├── templates/trips/
│   │   ├── includes/trip_card.html
│   │   ├── trip_list.html
│   │   └── trip_detail.html
│   ├── urls.py
│   └── views.py
│
├── notes/
│   ├── templates/notes/
│   │   ├── includes/note_status.html
│   │   ├── note_list.html
│   │   └── note_detail.html
│   ├── urls.py
│   └── views.py
│
├── models/                  # классы предметной области
│   ├── trips.py
│   ├── travelers.py
│   └── notes.py
├── data/
│   ├── trips.json
│   ├── travelers.json
│   └── notes.json
└── tests/                   # pytest: модель и хранилище
```

## 5. Веб-интерфейс

| URL | Имя маршрута | View | Шаблон |
|-----|--------------|------|--------|
| `/` | `homepage:index` | `index()` | `homepage/index.html` |
| `/trips/` | `trips:list` | `trips()` | `trips/trip_list.html` |
| `/trips/<int:trip_id>/` | `trips:detail` | `trip_detail()` | `trips/trip_detail.html` |
| `/notes/` | `notes:list` | `notes()` | `notes/note_list.html` |
| `/notes/<int:note_id>/` | `notes:detail` | `note_detail()` | `notes/note_detail.html` |

Если поездка или заметка не найдены, шаблон показывает сообщение, а
ответ имеет статус 404 (`render(..., status=404)`). Для несуществующих
адресов подключён `handler404` с шаблоном `templates/404.html`.

HTML в Python-коде не формируется: функция `page()` из ПР5 удалена,
все view-функции используют `render(request, "...html", context)`.

## 6. Django Template Language

- **Базовый шаблон** `templates/base.html`: структура страницы,
  подключение Bootstrap, собственного CSS и JS, шапка, навигация, подвал,
  блоки `{% block title %}` и `{% block content %}`.
- **Наследование:** дочерние шаблоны начинаются с
  `{% extends "base.html" %}`.
- **Включаемые шаблоны** (`{% include %}`): навигация
  `includes/navigation.html`, карточка поездки `trip_card.html`,
  статус заметки `note_status.html` (используется в списке заметок,
  на странице заметки и на странице поездки).
- **Контекст:** view готовит данные (`{"trips": ...}`, `{"note": ...}`)
  и передаёт их в `render()`.
- **Циклы и условия:** `{% for %}…{% empty %}`, `{% if %}…{% else %}`
  (пустые списки, ненайденные объекты, активная/архивная заметка).
- **Именованные URL и пространства имён:** в `urls.py` заданы
  `app_name` и `name`, ссылки строятся тегом
  `{% url 'trips:detail' trip.id %}`.
- **Фильтры:** `length` (количество поездок и заметок), `default`
  (название поездки по умолчанию), `truncatechars` (краткий текст
  заметки), `linebreaksbr` (переносы строк в тексте заметки).

## 7. Статические файлы

В `homepage/static/homepage/`:

- `css/bootstrap.min.css` — Bootstrap 5.3.3 (локальная копия, работает без доступа к CDN);
- `css/style.css` — собственные стили (карточки, шапка, статусы);
- `js/main.js` — текущий год в подвале и подсветка активного пункта
  навигации;
- `img/logo.png` — логотип.

Подключаются через `{% load static %}` и `{% static '...' %}`.

## 8. Запуск

```text
python -m venv venv
venv\Scripts\activate          # Windows; Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Адрес: http://127.0.0.1:8000/

Консольная версия (сохранена):

```text
python main.py
```

## 9. Проверка

```text
python manage.py check
pytest -v                          # модель и хранилище
python manage.py test              # веб-страницы и шаблоны
flake8 . --extend-exclude=venv
python manage.py findstatic homepage/img/logo.png
```

## 10. Git

Коммиты практических работ начинаются с метки `PR1:` … `PR6:`.
Метки `pr1`, `pr2`, `pr3`, `pr5`, `pr6` указывают на состояние проекта
после соответствующей работы.

## 11. План развития

- перенос `Trip`, `Traveler`, `Note` в Django ORM и подключение базы
  данных;
- формы создания и редактирования заметок;
- регистрация и авторизация пользователей;
- использование отложенной логики ПР3 (создание и архивирование заметок,
  поиск, сортировка) в веб-интерфейсе;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
