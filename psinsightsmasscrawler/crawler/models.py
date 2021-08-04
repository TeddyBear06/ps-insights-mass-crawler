from django.db import models


class Site(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    WAITING = 'WAI'
    RUNNING = 'RUN'
    ERROR = 'ERR'
    FINISHED = 'FIN'
    STATES_CHOICES = [
        (WAITING, 'Waiting'),
        (RUNNING, 'Running'),
        (ERROR, 'Error'),
        (FINISHED, 'Finished'),
    ]
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=3,
        choices=STATES_CHOICES,
        default=WAITING,
    )
    batch_report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site.name


class Url(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+')
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class BatchUrl(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class UrlReport(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    batch_url = models.ForeignKey(BatchUrl, on_delete=models.CASCADE)
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch.site.name