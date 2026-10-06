from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-страницу: каркас, Bootstrap и навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/trips/">Поездки</a>
        <a class="nav-link" href="/notes/">Заметки</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Путевые заметки</h1>
    <p class="lead">Дневник путешествий: поездки и заметки по дням.</p>
    <p>Основные разделы:</p>
    <a href="/trips/" class="btn btn-primary me-2">Поездки</a>
    <a href="/notes/" class="btn btn-secondary">Заметки</a>
    """
    return HttpResponse(page("Путевые заметки", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
