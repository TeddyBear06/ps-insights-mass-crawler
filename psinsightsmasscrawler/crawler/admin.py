from .models import Website, Batch, Url, BatchUrl, PageSpeedRequest
from django.contrib import messages
from django.contrib import admin
from .tasks import *

admin.site.site_header = 'PageSpeed mass crawler'

@admin.action(description='1. Crawl website URLs')
def crawl_website_action(modeladmin, request, queryset):
    crawl_website.delay(list(queryset.values_list('id', flat=True)))
    messages.info(request, "Crawl in progress, please wait. It can take a while...")
    return True

@admin.action(description='2. Create a new batch')
def create_batch_action(modeladmin, request, queryset):
    create_batch.delay(list(queryset.values_list('id', flat=True)))
    messages.info(request, "Batch creation in progress, please wait. It can take a while...")
    return True

@admin.action(description='3. Perform PageSpeed test')
def perform_pagespeed_requests_action(modeladmin, request, queryset):
    perform_pagespeed_requests.delay(list(queryset.values_list('id', flat=True)))
    messages.info(request, "PageSpeed in progress, please wait. It can take a while...")
    return True

class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    ordering = ['name']
    actions = [crawl_website_action, create_batch_action]

class BatchAdmin(admin.ModelAdmin):
    list_filter = ('website', 'state')
    list_display = ['website', 'state']
    ordering = ['website']
    actions = [perform_pagespeed_requests_action]

class UrlAdmin(admin.ModelAdmin):
    list_display = ['website', 'url']
    ordering = ['website']

class BatchUrlAdmin(admin.ModelAdmin):
    list_filter = ('batch', 'status_code')
    list_display = ['batch', 'url', 'performance', 'status_code', 'state']
    ordering = ['batch']

class PageSpeedRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_at']
    ordering = ['requested_at']

admin.site.register(Website, WebsiteAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(BatchUrl, BatchUrlAdmin)
admin.site.register(PageSpeedRequest, PageSpeedRequestAdmin)