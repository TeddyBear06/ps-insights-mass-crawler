# PageSpeed Insights Mass Carwler (aka psinsightsmasscrawler)

## Quickstart

[1/4] Run the stack:

```bash
$ docker compose -p psinsightsmasscrawler up
```

[2/4] Open the app container shell:

```bash
$ docker exec -it psinsightsmasscrawler-app-1 sh
```

[3/4] Create a django admin super user (follow CLI instructions):

```bash
$ python manage.py createsuperuser
```

[4/4] Go to <a href="http://127.0.0.1:8000/admin/">http://127.0.0.1:8000/admin/</a>

## Usage

Have a look at this YouTube video : <a href="https://www.youtube.com/watch?v=AVuUznzflug">https://www.youtube.com/watch?v=AVuUznzflug</a>

## Useful commands

### Remove recents actions

Open a django shell:

```bash
$ python manage.py shell
```

Then:

```bash
>>> from django.contrib.admin.models import LogEntry
>>> LogEntry.objects.all().delete()
```

## Dependencies

Thanks to all contributors of thoose wonderful projects:

- [Django](https://www.djangoproject.com/)
- [ultimate-sitemap-parser](https://pypi.org/project/ultimate-sitemap-parser/)
- [redis](https://pypi.org/project/redis/)
- [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)