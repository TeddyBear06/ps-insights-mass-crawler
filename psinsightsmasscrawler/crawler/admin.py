from .models import Website, Batch, Url, BatchUrl, PageSpeedRequest
from django.contrib import messages
from django.contrib import admin
from django.http import HttpResponse
from .tasks import *
import time

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
    perform_pagespeed_requests.delay(list(queryset.values_list('id', flat=True)), 'even')
    time.sleep(2)
    perform_pagespeed_requests.delay(list(queryset.values_list('id', flat=True)), 'odd')
    messages.info(request, "PageSpeed in progress, please wait. It can take a while...")
    return True

# @admin.action(description='4. Export JSON reports')
# def export_json_reports_action(modeladmin, request, queryset):
#     export_json_reports.delay(list(queryset.values_list('id', flat=True)))
#     messages.info(request, "JSON export in progress, please wait. It can take a while...")
#     return True

@admin.action(description='Export CSV')
def export_csv_action(self, request, queryset):
    import csv
    meta = self.model._meta
    field_names = ['batch', 'url', 'performance', 'lcp', 'fid', 'cls', 'status_code', 'state']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    ordering = ['name']
    actions = [crawl_website_action, create_batch_action]

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_filter = ('website', 'state')
    list_display = ['website', 'state', 'created_at']
    ordering = ['website']
    actions = [perform_pagespeed_requests_action]

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_filter = ['website']
    list_display = ['website', 'url']
    ordering = ['website']

@admin.register(BatchUrl)
class BatchUrlAdmin(admin.ModelAdmin):
    list_filter = ('batch', 'status_code')
    list_display = ['batch', 'url', 'performance', 'lcp', 'fid', 'cls', 'status_code', 'state', 'fieldname_download']
    readonly_fields = ('fieldname_download', )
    ordering = ['batch']
    actions = [export_csv_action]

@admin.register(PageSpeedRequest)
class PageSpeedRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_at']
    ordering = ['requested_at']