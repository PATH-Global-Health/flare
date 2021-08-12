from django.contrib import admin
from .models import Language, Configuration, Channel


class configuration_inline(admin.TabularInline):
    model = Configuration
    extra = 1


class ChannelAdmin(admin.ModelAdmin):
    inlines = (configuration_inline,)


admin.site.register(Language)
admin.site.register(Channel, ChannelAdmin)
