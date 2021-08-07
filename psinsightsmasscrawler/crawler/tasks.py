from crawler.models import Website, Url, Batch, BatchUrl, PageSpeedRequest
from crawler.constants import *
from celery import shared_task

@shared_task
def crawl_website(websites_pks):
    from usp.tree import sitemap_tree_for_homepage
    for website_pk in websites_pks:
        website = Website.objects.get(pk=website_pk)
        tree = sitemap_tree_for_homepage(website.url)
        for page in tree.all_pages():
            url = Url(website=website, url=page.url)
            url.save()
    return True

# https://stackoverflow.com/questions/8706665/best-way-to-process-database-in-chunks-with-django-queryset#answer-39550574
def chunked_queryset(qs, batch_size, index='id'):
    """
    Yields a queryset split into batches of maximum size 'batch_size'.
    Any ordering on the queryset is discarded.
    """
    from django.db import models
    qs = qs.order_by()  # clear ordering
    min_max = qs.aggregate(min=models.Min(index), max=models.Max(index))
    min_id, max_id = min_max['min'], min_max['max']
    for i in range(min_id, max_id + 1, batch_size):
        filter_args = {'{0}__range'.format(index): (i, i + batch_size - 1)}
        yield qs.filter(**filter_args)

@shared_task
def create_batch(websites_pks):
    for website_pk in websites_pks:
        website = Website.objects.get(pk=website_pk)
        batch = Batch(website=website)
        batch.save()
        for chunk in chunked_queryset(Url.objects.filter(website=website), 2000):
            batch_urls = []
            for url in chunk:
                batch_urls.append(BatchUrl(batch=batch, url=url.url))
            BatchUrl.objects.bulk_create(batch_urls)
    return True

@shared_task
def perform_pagespeed_requests(batchs_pks):
    import requests, environ, time, json
    env = environ.Env()
    environ.Env.read_env()
    pagespeed_key = env("PAGESPEED_KEY")
    for batch_pk in batchs_pks:
        batch = Batch.objects.get(pk=batch_pk)
        batchModel = Batch.objects.filter(pk=batch.pk)
        if batch.state == WAITING:
            batchFinalState = FINISHED
            howManyUrlFinished = 0
            batchUrls = BatchUrl.objects.filter(batch=batch).exclude(state=FINISHED)
            totalNumberUrlsToBeRequested = batchUrls.count()
            for batchUrl in batchUrls:
                batchUrlModel = BatchUrl.objects.filter(pk=batchUrl.pk)
                psr = PageSpeedRequest()
                psr.save()
                response = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+batchUrl.url+'&key='+pagespeed_key)
                if response.status_code == 200:
                    state = FINISHED
                    howManyUrlFinished = howManyUrlFinished + 1
                elif response.status_code == 429:
                    # If we face a "Too Many Requests" it's a good time to sleep a while
                    return None
                else:
                    state = ERROR
                    batchFinalState = ERROR
                report = json.loads(response.text)
                performance = report['lighthouseResult']['categories']['performance']['score'] * 100
                lcp = report['lighthouseResult']['audits']['largest-contentful-paint']['score'] * 100
                fid = report['lighthouseResult']['audits']['total-blocking-time']['score'] * 100
                cls = report['lighthouseResult']['audits']['cumulative-layout-shift']['score'] * 100
                batchUrlModel.update(report=json.dumps(report), status_code=response.status_code, performance=performance, lcp=lcp, fid=fid, cls=cls, state=state)
                time.sleep(3.5)
            report_mess = '%s/%s URL(s) successfully requested against PageSpeed.' % (howManyUrlFinished, totalNumberUrlsToBeRequested)
            batchModel.update(state=batchFinalState, batch_report=report_mess)
    return True