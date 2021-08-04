from django.contrib import admin

from .models import Site
from .models import Batch
from .models import Url
from .models import BatchUrl
from .models import UrlReport

admin.site.register(Site)
admin.site.register(Batch)
admin.site.register(Url)
admin.site.register(BatchUrl)
admin.site.register(UrlReport)