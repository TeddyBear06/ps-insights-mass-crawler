from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
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
        return self.website.name


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
    url = models.CharField(max_length=255)
    report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class PageSpeedRequest(models.Model):
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return naturaltime(self.requested_at)