WAITING = 0
RUNNING = 1
ERROR = 2
FINISHED = 3
STATES_CHOICES = [
    (WAITING, 'Waiting'),
    (RUNNING, 'Running'),
    (ERROR, 'Error'),
    (FINISHED, 'Finished'),
]

PAGESPEED_API_URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&key=%s'