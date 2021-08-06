from celery import shared_task
from crawler.models import Website, Url, Batch, BatchUrl, PageSpeedRequest
from crawler.constants import *

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

@shared_task
def create_batch(websites_pks):
    for website_pk in websites_pks:
        website = Website.objects.get(pk=website_pk)
        batch = Batch(website=website)
        batch.save()
        urls = Url.objects.filter(website=website)
        for url in urls:
            batch_url = BatchUrl(batch=batch, url=url.url)
            batch_url.save()
    return True

@shared_task
def perform_pagespeed_requests(batchs_pks):
    import requests
    import environ
    import time
    env = environ.Env()
    environ.Env.read_env()
    pagespeed_key = env("PAGESPEED_KEY")
    for batch_pk in batchs_pks:
        batch = Batch.objects.get(pk=batch_pk)
        batchModel = Batch.objects.filter(pk=batch.pk)
        if batch.state == WAITING:
            batchFinalState = FINISHED
            howManyUrlFinished = 0
            batchUrls = BatchUrl.objects.filter(batch=batch)
            totalNumberUrlsToBeRequested = batchUrls.count()
            for batchUrl in batchUrls:
                if batchUrl.state != FINISHED:
                    batchUrlModel = BatchUrl.objects.filter(pk=batchUrl.pk)
                    psr = PageSpeedRequest()
                    psr.save()
                    response = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+batchUrl.url+'&key='+pagespeed_key)
                    if response.status_code == 200:
                        state = FINISHED
                        howManyUrlFinished = howManyUrlFinished + 1
                    else:
                        state = ERROR
                        batchFinalState = ERROR
                    batchUrlModel.update(report=response.json(), status_code=response.status_code, state=state)
                    time.sleep(3)
            report_mess = '%s/%s URL(s) successfully requested against PageSpeed.' % (howManyUrlFinished, totalNumberUrlsToBeRequested)
            batchModel.update(state=batchFinalState, batch_report=report_mess)
    return True