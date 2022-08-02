from django.contrib import admin

from fitlife.practice.models import Practice, Exercise, Frequency, Checklist


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    pass
