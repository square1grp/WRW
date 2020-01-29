from django.db import models
from django.utils import timezone
from datetime import datetime


# User Model
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    email_to_confirm = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField(
        choices=[(r, r) for r in range(1900, datetime.today().year+1)],
        default=datetime.today().year)
    ethnicity_top = models.CharField(max_length=50)
    ethnicity_second = models.CharField(max_length=50, null=True, blank=True)
    ethnicity_third = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
                              ('male', 'Male'), ('female', 'Female')], default='male')
    sexual_orientation = models.CharField(max_length=10,
                                          choices=[
                                              ('hetero', 'Heterosexual'), ('homo', 'Homosexual'), ('bi', 'Bisexual')],
                                          default='hetero')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50)
    confirm_token = models.TextField(unique=True, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Symptom Model
class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level_1 = models.CharField(max_length=50, default='None')
    level_2 = models.CharField(max_length=50, default='Mild')
    level_3 = models.CharField(max_length=50, default='Moderate')
    level_4 = models.CharField(max_length=50, default='Severe')
    level_5 = models.CharField(max_length=50, default='Very Severe')

    class Meta:
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'

    def __str__(self):
        return self.name

    def getSymptomLevels(self):
        return [getattr(self, 'level_%s' % (i+1)) for i in range(5)]


# Current User Symptom
class CurrentUserSymptom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Current User-Symptom'
        verbose_name_plural = 'Current User-Symptoms'

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getSymptomName(self):
        return self.symptom.name
    getSymptomName.short_description = 'Symptom'

    def getSymptomLevels(self):
        return [getattr(self.symptom, 'level_%s' % (i+1)) for i in range(5)]


# User Symptom Severities
class UserSymptomSeverities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'User-Symptom Severities'
        verbose_name_plural = 'Users-Symptom Severities'

    def __str__(self):
        return self.title

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getUSSSList(self):
        return UserSingleSymptomSeverity.objects.filter(user_symptom_severities__id=self.id)


# User Single Symptom Severity
class UserSingleSymptomSeverity(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    user_symptom_severities = models.ForeignKey(
        UserSymptomSeverities, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    selected_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'User-Single-Symptom Severity'
        verbose_name_plural = 'User-Single-Symptom Severities'

    def __str__(self):
        return '%s in %s' % (self.symptom, self.user_symptom_severities)

    def getUserFirstName(self):
        return self.user_symptom_severities.getUserFirstName()
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user_symptom_severities.getUserLastName()
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user_symptom_severities.getUserName()
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user_symptom_severities.getUserEmail()
    getUserEmail.short_description = 'Email'

    def getSymptom(self):
        return self.symptom

    def getSymptomName(self):
        return self.symptom.name
    getSymptomName.short_description = 'Symptom'

    def getLevel(self):
        return getattr(self.symptom, 'level_%s' % self.selected_level) if self.selected_level else None
    getLevel.short_description = 'Symptom Level'


# Factor
class Factor(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level_1 = models.CharField(max_length=50, default='Zero')
    level_2 = models.CharField(max_length=50, default='Low')
    level_3 = models.CharField(max_length=50, default='Medium')
    level_4 = models.CharField(max_length=50, default='High')
    level_5 = models.CharField(max_length=50, default='Max')

    class Meta:
        verbose_name = 'Factor'
        verbose_name_plural = 'Factors'

    def __str__(self):
        return self.title


# Current Intermittent Factor
class CurrentIntermittentFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Current Intermittent Factor'
        verbose_name_plural = 'Current Intermittent Factors'

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'


# Current Daily Factor
class CurrentDailyFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Current Daily Factor'
        verbose_name_plural = 'Current Daily Factors'

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'


# User Intermittent Factor
class UserIntermittentFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    selected_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'User Intermittent Factor'
        verbose_name_plural = 'User Intermittent Factors'

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'

    def getLevel(self):
        return getattr(self.factor, 'level_%s' % self.selected_level)
    getLevel.short_description = 'Factor Level'


# User Daily Factor
class UserDailyFactor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    selected_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'User Daily Factor'
        verbose_name_plural = 'User Daily Factors'

    def getUserFirstName(self):
        return self.user.first_name
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user.last_name
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user.username
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user.email
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'

    def getLevel(self):
        return getattr(self.factor, 'level_%s' % self.selected_level)
    getLevel.short_description = 'Factor Level'


# Level Transition
class LevelTransition(models.Model):
    user_daily_factor = models.ForeignKey(
        UserDailyFactor, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'Level Transitions'
        verbose_name_plural = 'Level Transitions'

    def getUserFirstName(self):
        return self.user_daily_factor.getUserFirstName()
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user_daily_factor.getUserLastName()
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user_daily_factor.getUserName()
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user_daily_factor.getUserEmail()
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.user_daily_factor.getFactorTitle()
    getFactorTitle.short_description = 'Factor'

    def getLevel(self):
        return self.user_daily_factor.getLevel()
    getLevel.short_description = 'Factor Level'


# Skipped Date
class SkippedDate(models.Model):
    user_daily_factor = models.ForeignKey(
        UserDailyFactor, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'Skipped Date'
        verbose_name_plural = 'Skipped Dates'

    def getUserFirstName(self):
        return self.user_daily_factor.getUserFirstName()
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user_daily_factor.getUserLastName()
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user_daily_factor.getUserName()
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user_daily_factor.getUserEmail()
    getUserEmail.short_description = 'Email'

    def getFactorTitle(self):
        return self.user_daily_factor.getFactorTitle()
    getFactorTitle.short_description = 'Factor'

    def getLevel(self):
        return self.user_daily_factor.getLevel()
