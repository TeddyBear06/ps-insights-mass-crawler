from django.contrib import admin

from .models import Website
from .models import Batch
from .models import Url
from .models import BatchUrl
from .models import UrlReport


@admin.action(description='Crawl website URLs')
def crawl_website(modeladmin, request, queryset):
    for website in queryset:
        # @TODO Retrieve website URLs (for real)
        urls = [
            'https://paysdufle.fr/pages/contact.html',
            'https://paysdufle.fr/pages/a-propos.html'
        ]
        for fake_url in urls:
            url = Url(website=website, url=fake_url)
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


class BatchUrlAdmin(admin.ModelAdmin):
    list_display = ['batch', 'url', 'state']
    ordering = ['batch']


admin.site.register(Website, WebsiteAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(BatchUrl, BatchUrlAdmin)
admin.site.register(UrlReport)