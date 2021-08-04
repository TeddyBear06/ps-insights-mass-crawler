from django.contrib import admin

from .models import Website
from .models import Batch
from .models import Url
from .models import BatchUrl


@admin.action(description='Crawl website URLs')
def crawl_website(modeladmin, request, queryset):
    from usp.tree import sitemap_tree_for_homepage
    for website in queryset:
        tree = sitemap_tree_for_homepage(website.url)
        for page in tree.all_pages():
            url = Url(website=website, url=page.url)
            url.save()


@admin.action(description='Create a new batch')
def create_batch(modeladmin, request, queryset):
    for website in queryset:
        batch = Batch(website=website)
        batch.save()
        urls = Url.objects.filter(website=website)
        for url in urls:
            batch_url = BatchUrl(batch=batch, url=url.url)
            batch_url.save()


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    ordering = ['name']
    actions = [crawl_website, create_batch]


class BatchAdmin(admin.ModelAdmin):
    list_display = ['website', 'state']
    ordering = ['website']


class UrlAdmin(admin.ModelAdmin):
    list_display = ['website', 'url']
    ordering = ['website']


@admin.action(description='Perform PageSpeed test')
def perform_pagespeed_test(modeladmin, request, queryset):
    import requests
    import environ
    import time
    env = environ.Env()
    environ.Env.read_env()
    pagespeed_key = env("PAGESPEED_KEY")
    for batchUrl in queryset:
        batchUrlModel = BatchUrl.objects.filter(pk=batchUrl.pk)
        batchUrlModel.update(state=1)
        response = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+batchUrl.url+'key='+pagespeed_key)
        if response.status_code == 200:
            state = 3
        else:
            state = 2
        batchUrlModel.update(report=response.json(), status_code=response.status_code, state=state)
        time.sleep(5)


class BatchUrlAdmin(admin.ModelAdmin):
    list_display = ['batch', 'url', 'status_code', 'state']
    ordering = ['batch']
    actions = [perform_pagespeed_test]


admin.site.register(Website, WebsiteAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(BatchUrl, BatchUrlAdmin)