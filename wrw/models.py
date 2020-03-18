from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


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
    approved_at = models.DateTimeField('Approved at', default=timezone.now)
    is_auto_renew = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    member_started_date = models.DateTimeField("Member started date", null=True, blank=True)
    member_expiration_date = models.DateTimeField("Member expiration date", null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def getFactorStartAndEndDates(self, factor):
        uifs = UserIntermittentFactor.objects.filter(
            user_factors__user=self, factor=factor).order_by('user_factors__created_at')

        created_at_list = [uif.getCreatedAt() for uif in uifs]

        udfms = UserDailyFactorMeta.objects.filter(
            user_daily_factor_start__user=self, user_daily_factor_start__factor=factor).order_by('created_at')

        for udfm in udfms:
            created_at_list.append(udfm.getCreatedAt())

            if udfm.isEnded():
                created_at_list.append(udfm.getEndedAt())

        created_at_list = sorted(created_at_list)

        return [
            created_at_list[0] if len(created_at_list) else None,
            created_at_list[-1] if len(created_at_list) > 1 else None
        ]

    def getSymptomSeverities(self, symptom, factor):
        [started_at, ended_at] = self.getFactorStartAndEndDates(factor)

        if started_at and ended_at:
            uss_list = [uss for uss in UserSingleSymptomSeverity.objects.filter(
                symptom=symptom,
                user_symptom_severities__user=self,
                user_symptom_severities__created_at__range=(started_at, ended_at)).order_by('user_symptom_severities__created_at')]

            if len(uss_list) > 1:
                severities = [
                    uss_list[0].getLevelNum(), uss_list[-1].getLevelNum()]
                return severities

        return None

    def getFactorsBySymptom(self, symptom):
        factors = []

        for factor in Factor.objects.all():
            severities = self.getSymptomSeverities(symptom, factor)

            if severities is not None:
                factors.append(factor)

        return factors


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
        return [getattr(self, 'level_%s' % i) for i in [1, 2, 3, 4, 5]]


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
        return [getattr(self.symptom, 'level_%s' % i) for i in [1, 2, 3, 4, 5]]


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
        return UserSingleSymptomSeverity.objects.filter(user_symptom_severities=self)

    def getTitle(self):
        return self.title

    def getCreatedAt(self):
        return self.created_at


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
        return getattr(self.symptom, 'level_%s' % self.selected_level)
    getLevel.short_description = 'Symptom Level'

    def getLevelNum(self):
        return self.selected_level

    def getTitle(self):
        return self.user_symptom_severities.getTitle()

    def getDescription(self):
        return self.description

    def getCreatedAt(self):
        return self.user_symptom_severities.getCreatedAt()


# Factor
class Factor(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level_0 = 'Skipped?'
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

    def getFactorLevels(self):
        return [getattr(self, 'level_%s' % i) for i in [1, 2, 3, 4, 5, 0]]


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

    def getFactorLevels(self):
        return [getattr(self.factor, 'level_%s' % i) for i in [1, 2, 3, 4, 5, 0]]


# User Factors
class UserFactors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'User-Factors'
        verbose_name_plural = 'Users-Factors'

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

    def getUIFList(self):
        return UserIntermittentFactor.objects.filter(user_factors=self)

    def getUDFSList(self):
        udfs_list = [udfs for udfs in UserDailyFactorStart.objects.filter(
            user=self.user, created_at__lt=self.created_at) if not udfs.isEnded()]
        # get udfs with created_at < UF created_at if the udfs is active

        for factor in Factor.objects.all():
            udfs_last = UserDailyFactorStart.objects.filter(
                user=self.user, factor=factor, created_at__lt=self.created_at).order_by('-created_at').first()
            # get oldest udfs from udfs_list

            # avoid case where oldest udf has been ended
            # if the most recent udfs has been ended
            if udfs_last and udfs_last not in udfs_list:
                # if the end date is after the UF created_at
                if udfs_last.getEndedAt() and udfs_last.getEndedAt() > self.created_at:
                    # append the udfs to the list which has all the active udfs's.
                    udfs_list.append(udfs_last)

        return udfs_list

    def getTitle(self):
        return self.title

    def getCreatedAt(self):
        return self.created_at


# User Intermittent Factor
class UserIntermittentFactor(models.Model):
    user_factors = models.ForeignKey(
        UserFactors, on_delete=models.CASCADE, blank=True, null=True)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    selected_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'User Intermittent Factor'
        verbose_name_plural = 'User Intermittent Factors'

    def getUserFirstName(self):
        return self.user_factors.getUserFirstName()
    getUserFirstName.short_description = 'First Name'

    def getUserLastName(self):
        return self.user_factors.getUserLastName()
    getUserLastName.short_description = 'Last Name'

    def getUserName(self):
        return self.user_factors.getUserName()
    getUserName.short_description = 'Username'

    def getUserEmail(self):
        return self.user_factors.getUserEmail()
    getUserEmail.short_description = 'Email'

    def getFactor(self):
        return self.factor

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'

    def getLevelNum(self):
        return self.selected_level

    def getLevel(self):
        return getattr(self.factor, 'level_%s' % self.selected_level) if self.selected_level is not None else None
    getLevel.short_description = 'Factor Level'

    def getTitle(self):
        return self.user_factors.getTitle()

    def getDescription(self):
        return self.description

    def getCreatedAt(self):
        return self.user_factors.getCreatedAt()


# User Daily Factor Start
class UserDailyFactorStart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'User Daily Factor Start'
        verbose_name_plural = 'User Daily Factor Starts'

    def getFactor(self):
        return self.factor

    def getFactorTitle(self):
        return self.factor.title
    getFactorTitle.short_description = 'Factor'

    def getTheLatestMeta(self):
        return UserDailyFactorMeta.objects.filter(
            user_daily_factor_start=self).order_by('-created_at').first()

    def getLevel(self, created_at=None):
        udfm = UserDailyFactorMeta.objects.filter(
            user_daily_factor_start=self, created_at=created_at) if created_at else self.getTheLatestMeta()

        udfm = udfm[0] if len(udfm) else None
        selected_level = udfm.selected_level if udfm is not None else None

        return getattr(self.factor, 'level_%s' % selected_level) if selected_level is not None else None
    getLevel.short_description = 'Factor Level'

    def getFactorLevels(self):
        return [getattr(self.factor, 'level_%s' % i) for i in [1, 2, 3, 4, 5, 0]]

    def getDescription(self):
        udfm = self.getTheLatestMeta()

        return udfm.getDescription() if udfm else ''

    def getCreatedAt(self):
        return self.created_at

    def isEnded(self):
        try:
            UserDailyFactorEnd.objects.get(user_daily_factor_start=self)

            return True
        except ObjectDoesNotExist:
            return False

    def getEndedAt(self):
        try:
            udfe = UserDailyFactorEnd.objects.get(user_daily_factor_start=self)

            return udfe.created_at
        except ObjectDoesNotExist:
            return None


# User Daily Factor End
class UserDailyFactorEnd(models.Model):
    user_daily_factor_start = models.ForeignKey(
        UserDailyFactorStart, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'User Daily Factor End'
        verbose_name_plural = 'User Daily Factor Ends'


# User Daily Factor Meta
class UserDailyFactorMeta(models.Model):
    user_daily_factor_start = models.ForeignKey(
        UserDailyFactorStart, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    selected_level = models.SmallIntegerField(blank=True, null=True)
    is_skipped = models.BooleanField(default=False)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    class Meta:
        verbose_name = 'User Daily Factor Meta'
        verbose_name_plural = 'User Daily Factor Metas'

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description if self.description else ''

    def getLevelNum(self):
        return self.selected_level

    def getCreatedAt(self):
        return self.created_at

    def isEnded(self):
        return self.user_daily_factor_start.isEnded()

    def getEndedAt(self):
        return self.user_daily_factor_start.getEndedAt()
