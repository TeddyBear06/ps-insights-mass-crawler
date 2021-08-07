from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.safestring import mark_safe
from django.db import models
from .constants import *


class Website(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    state = models.SmallIntegerField(
        choices=STATES_CHOICES,
        default=WAITING,
    )
    batch_report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website.name+' ('+self.created_at.strftime("%d/%m/%y %H:%M:%S")+')'


class Url(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='+')
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class BatchUrl(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    state =  models.SmallIntegerField(
        choices=STATES_CHOICES,
        default=WAITING,
    )
    status_code = models.SmallIntegerField(null=True)
    performance = models.SmallIntegerField(null=True)
    lcp = models.SmallIntegerField(null=True, help_text="Largest Contentful Paint: Performance de la page")
    fid = models.SmallIntegerField(null=True, help_text="First Input Delay: Interactivité de la page (TBT in Lighthouse)")
    cls = models.SmallIntegerField(null=True, help_text="Cumulative Layout Shift: Stabilité de la page")
    url = models.CharField(max_length=255)
    report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def fieldname_download(self):
        return mark_safe('<a href="/crawler/report/%s" download>%s</a>' % (self.pk, 'Report'))

    fieldname_download.short_description = 'Download report'


class PageSpeedRequest(models.Model):
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return naturaltime(self.requested_at)