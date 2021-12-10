# PageSpeed Insights Mass Carwler (aka psinsightsmasscrawler)

Psinsightsmasscrawler is a tool to make - mass - PageSpeed tests easier and obtain a clear report.

![Report view](medias/screen1.png?raw=true "Report view")

Just add a domain, crawl website's URLs (using sitemap.whatever, do not worry it's automagical), create a batch (a list of URLs to analyze) and run the batch to get a clean view of a website performance.

This tool store the report as a JSON downloadable file that you can analyse using [Lighthouse Report Viewer](https://googlechrome.github.io/lighthouse/viewer/).

Have a look at this YouTube video <a href="https://www.youtube.com/watch?v=AVuUznzflug">https://www.youtube.com/watch?v=AVuUznzflug</a> for a complete demo.

## Requirements

1. Pagespeed API keys (2 keys for async workers), see [Get Started with the PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started#APIKey)
2. Clone this repo:

```bash
$ git clone https://github.com/TeddyBear06/ps-insights-mass-crawler.git
```

3. Docker (tested with 4.30, latest actually)

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