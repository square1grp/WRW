from django.contrib import admin
from wrw.models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'username',
        'email',
        'city',
        'state',
        'country']
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'ethnicity_top',
        'ethnicity_second',
        'ethnicity_third',
        'city',
        'state',
        'zipcode',
        'country']
    list_filter = ['gender', 'sexual_orientation']


class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CurrentUserSymptomAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getSymptomName']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'symptom__name']


class UserSymptomSeveritiesAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'title',
        'created_at']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'title']


class UserSingleSymptomSeverityAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getSymptomName',
        'getLevel']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'symptom__name']


class FactorAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


class CurrentIntermittentFactorAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'factor_title']


class CurrentDailyFactorAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'factor_title']


class UserFactorsAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'title',
        'created_at']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'title']


class UserIntermittentFactorAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle',
        'getLevel']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'factor_title']


class UserDailyFactorAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle',
        'getLevel']

    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__username',
        'user__email',
        'factor_title']


class LevelTransitionAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle',
        'getLevel',
        'created_at']

    search_fields = [
        'user_daily_factor__user__first_name',
        'user_daily_factor__user__last_name',
        'user_daily_factor__user__username',
        'user_daily_factor__user__email',
        'user_daily_factor__factor_title']


class SkippedDateAdmin(admin.ModelAdmin):
    list_display = [
        'getUserFirstName',
        'getUserLastName',
        'getUserName',
        'getUserEmail',
        'getFactorTitle',
        'getLevel',
        'created_at']

    search_fields = [
        'user_daily_factor__user__first_name',
        'user_daily_factor__user__last_name',
        'user_daily_factor__user__username',
        'user_daily_factor__user__email',
        'user_daily_factor__factor_title']


admin.site.register(User, UserAdmin)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(CurrentUserSymptom, CurrentUserSymptomAdmin)
admin.site.register(UserSymptomSeverities, UserSymptomSeveritiesAdmin)
admin.site.register(UserSingleSymptomSeverity, UserSingleSymptomSeverityAdmin)
admin.site.register(Factor, FactorAdmin)
admin.site.register(CurrentIntermittentFactor, CurrentIntermittentFactorAdmin)
admin.site.register(CurrentDailyFactor, CurrentDailyFactorAdmin)
admin.site.register(UserFactors, UserFactorsAdmin)
admin.site.register(UserIntermittentFactor, UserIntermittentFactorAdmin)
admin.site.register(UserDailyFactor, UserDailyFactorAdmin)
admin.site.register(LevelTransition, LevelTransitionAdmin)
admin.site.register(SkippedDate, SkippedDateAdmin)
