from django.contrib import admin
from models import *


class ProjectStageInline(admin.TabularInline):
    model = Stage


class ProjectAdm(admin.ModelAdmin):
    list_display = ('name', 'repository')
    search_fields = ('name',)
    inlines = [
        ProjectStageInline
    ]

    class Media:
        css = {
            'all': ('codemirror/codemirror.css',)
        }
        js = (
            'codemirror/codemirror.js',
            'codemirror/python.js',
            'codemirror/setup-project.js',
        )


class ProjectParamAdm(admin.ModelAdmin):
    list_display = ('project', 'name', 'value')
    list_filter = ('project',)
    search_fields = ('name',)


class StageUserInline(admin.TabularInline):
    model = Stage.users.through


class StageTaskInline(admin.TabularInline):
    model = Stage.tasks.through


class StageAdm(admin.ModelAdmin):
    list_display = ('project', 'name')
    inlines = [
        StageUserInline,
        StageTaskInline,
    ]


class StageParamAdm(admin.ModelAdmin):
    list_display = ('stage', 'name', 'value')
    list_filter = ('stage',)
    search_fields = ('name',)


class TaskAdm(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

    class Media:
        css = {
            'all': ('codemirror/codemirror.css',)
        }
        js = (
            'codemirror/codemirror.js',
            'codemirror/python.js',
            'codemirror/setup-task.js',
        )


class DeployAdm(admin.ModelAdmin):
    list_display = ('stage', 'user', 'status')


admin.site.register(Project, ProjectAdm)
admin.site.register(ProjectParam, ProjectParamAdm)
admin.site.register(Stage, StageAdm)
admin.site.register(StageParam, StageParamAdm)
admin.site.register(Task, TaskAdm)
admin.site.register(Deploy, DeployAdm)
