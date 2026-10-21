# Путевые заметки

Дневник путешествий на Python с веб-интерфейсом на Django: поездки,
путешественники и заметки по дням.

## 1. Назначение проекта

Приложение помогает путешественнику вести записи о поездках: хранить
маршруты, фиксировать впечатления по дням и находить их после поездки.
Проект развивается поэтапно: консольная версия (ПР1–ПР3) дополнена
веб-интерфейсом на Django (ПР5), веб-страницы переведены на систему
шаблонов Django (ПР6), а данные для страниц теперь берутся из
реляционной базы SQLite с помощью SQL-запросов (ПР7).

**Целевая аудитория:** путешественники, любители походов, travel-блогеры.

## 2. Используемые технологии

- Python 3.11+;
- Django 5.2 (LTS);
- Django Template Language (DTL);
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3.3 (локальная копия в `homepage/static/homepage/css/`);
- SQLite и модуль `sqlite3` (SQL-запросы без Django ORM);
- JSON — исходные данные и консольная версия;
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

**На текущем этапе:** веб-страницы читают данные из базы SQLite
(`data/travelnotes.sqlite`) обычными SQL-запросами через `sqlite3`.
JSON-файлы остаются исходными данными для импорта и источником для
консольной версии (`main.py`). Django ORM, Django-модели и веб-формы
пока не используются: они относятся к следующим практическим работам.

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
├── db/                      # работа с SQLite (ПР7)
│   ├── database.py          # подключение, создание схемы
│   ├── import_json.py       # перенос JSON -> SQLite
│   └── testing.py           # временная БД для тестов
├── sql/
│   ├── schema.sql           # CREATE TABLE, ключи, индексы
│   └── queries.sql          # 15 SQL-запросов с комментариями
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
│   ├── notes.json
│   └── travelnotes.sqlite   # база данных SQLite (ПР7)
└── tests/                   # pytest: модель, хранилище, БД и запросы
```

## 5. Веб-интерфейс

| URL | Имя маршрута | View | Шаблон |
|-----|--------------|------|--------|
| `/` | `homepage:index` | `index()` | `homepage/index.html` |
| `/trips/` | `trips:list` | `trips()` | `trips/trip_list.html` |
| `/trips/available/` | `trips:available` | `available_trips()` | `trips/available.html` |
| `/trips/<int:trip_id>/` | `trips:detail` | `trip_detail()` | `trips/trip_detail.html` |
| `/notes/` | `notes:list` | `notes()` | `notes/note_list.html` |
| `/notes/statistics/` | `notes:statistics` | `statistics()` | `notes/statistics.html` |
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

## 8. База данных и SQL (ПР7)

### Структура базы

Три таблицы (файл `sql/schema.sql`):

| Таблица | Поля | Ключи и ограничения |
|---------|------|---------------------|
| `trips` | `id`, `title`, `country`, `start_date`, `end_date` | PK `id`; `CHECK (end_date >= start_date)` |
| `travelers` | `id`, `name`, `email` | PK `id` |
| `notes` | `id`, `trip_id`, `traveler_id`, `note_date`, `text`, `is_archived` | PK `id`; FK `trip_id` → `trips.id`; FK `traveler_id` → `travelers.id`; `is_archived IN (0, 1)` |

Связи: одна поездка — много заметок (1:N), один путешественник — много
заметок (1:N). Правило предметной области «одна активная заметка на день
поездки» закреплено уникальным частичным индексом
`ux_notes_active_day ON notes (trip_id, note_date) WHERE is_archived = 0`.
Даты хранятся как текст `ГГГГ-ММ-ДД`, логическое значение — как 0/1
(в SQLite нет отдельных типов даты и bool).

### Создание базы и перенос данных

```text
python -m db.import_json
```

Команда создаёт `data/travelnotes.sqlite`, таблицы из `sql/schema.sql` и
переносит данные из JSON в одной транзакции. Порядок импорта —
`trips`, `travelers`, `notes` (из-за внешних ключей). Повторный запуск
безопасен: записи обновляются (`ON CONFLICT(id) DO UPDATE`), дубли не
создаются.

Просмотр базы: расширение «SQLite Viewer» в VS Code или консоль:

```text
sqlite3 data/travelnotes.sqlite
.tables
.schema notes
```

### SQL-запросы

Файл `sql/queries.sql` содержит 15 запросов с комментариями, каждый
проверен на данных проекта:

| Вид | Запросы |
|-----|---------|
| Списки | Q1 поездки, Q2 путешественники |
| `WHERE` | Q3 поездки по стране и длительности, Q4 активные заметки, Q5 заметки за период |
| `JOIN` | Q6 заметки с поездкой и автором, Q7 заметки поездки с авторами |
| Подзапрос | Q8 поездки без заметки на выбранный день (`NOT IN`) |
| Агрегаты | Q9 `COUNT`, Q10 `COUNT`, `MIN`, `MAX`, `AVG` |
| `GROUP BY` / `HAVING` | Q11 заметки по поездкам (`LEFT JOIN`), Q12 поездки по странам (`SUM`), Q13 поездки с несколькими заметками (`HAVING`), Q14 заметки по авторам |
| `LIMIT` | Q15 три последние заметки |

Длительность поездки считается в SQL:
`julianday(end_date) - julianday(start_date) + 1`.

### SQL в Django-представлениях

Представления используют `sqlite3` напрямую, без ORM:

- соединение берётся из `db.database.get_connection()`;
- `conn.row_factory = sqlite3.Row` — к полям можно обращаться по имени, а
  в шаблонах — `{{ note.trip_title }}`;
- значения передаются только параметрами `?`, f-строки в SQL не
  используются (защита от SQL-инъекций);
- соединение закрывается через `contextlib.closing`.

| Страница | Что делает SQL |
|----------|----------------|
| `/trips/` | список с фильтром по стране и минимальной длительности (`WHERE`, параметры из формы) |
| `/trips/<id>/` | поездка по `id`, её заметки (`JOIN`), есть ли заметка на сегодня (`COUNT`) |
| `/trips/available/?date=...` | поездки без активной заметки на дату (`BETWEEN`, `NOT IN`) |
| `/notes/?status=...` | активные, архивные или все заметки (`JOIN`) |
| `/notes/<id>/` | заметка с поездкой и автором (`JOIN`) |
| `/notes/statistics/` | `COUNT`, `MIN`, `MAX`, `AVG`, `GROUP BY`, `HAVING`, `LIMIT` |

Если страницы пишут ошибку «no such table», база не создана — выполните
`python -m db.import_json`.

## 9. Запуск

```text
python -m venv venv
venv\Scripts\activate          # Windows; Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python -m db.import_json       # создать базу SQLite (если её ещё нет)
python manage.py runserver
```

Адрес: http://127.0.0.1:8000/

Консольная версия (сохранена):

```text
python main.py
```

## 10. Проверка

```text
python manage.py check
pytest -v                          # модель, хранилище, БД и SQL-запросы
python manage.py test              # веб-страницы, шаблоны, SQL-страницы
flake8 . --extend-exclude=venv
python manage.py findstatic homepage/img/logo.png
```

## 11. Git

Коммиты практических работ начинаются с метки `PR1:` … `PR7:`.
Метки `pr1`, `pr2`, `pr3`, `pr5`, `pr6`, `pr7` указывают на состояние проекта
после соответствующей работы.

## 12. План развития

- перенос `Trip`, `Traveler`, `Note` в Django ORM и Django-модели
  вместо прямых SQL-запросов;
- формы создания и редактирования заметок;
- регистрация и авторизация пользователей;
- использование отложенной логики ПР3 (создание и архивирование заметок,
  поиск, сортировка) в веб-интерфейсе;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
