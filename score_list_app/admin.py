from django.contrib import admin
from .models import ToDo, UploadFile, ScoreList


class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


class UploadFileAdmin(admin.ModelAdmin):
    pass


class ScorelistAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)


# Register your models here.
admin.site.register(ToDo, ToDoAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(ScoreList, ScorelistAdmin)
