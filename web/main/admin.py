from django.contrib import admin
from .models import Certificate, Portfolio, Microblog, HomeSetting

admin.site.register(Certificate)
admin.site.register(Portfolio)
admin.site.register(Microblog)
admin.site.register(HomeSetting)