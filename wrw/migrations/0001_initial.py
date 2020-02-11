# Generated by Django 3.0.2 on 2020-02-11 09:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('level_1', models.CharField(default='Zero', max_length=50)),
                ('level_2', models.CharField(default='Low', max_length=50)),
                ('level_3', models.CharField(default='Medium', max_length=50)),
                ('level_4', models.CharField(default='High', max_length=50)),
                ('level_5', models.CharField(default='Max', max_length=50)),
            ],
            options={
                'verbose_name': 'Factor',
                'verbose_name_plural': 'Factors',
            },
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('level_1', models.CharField(default='None', max_length=50)),
                ('level_2', models.CharField(default='Mild', max_length=50)),
                ('level_3', models.CharField(default='Moderate', max_length=50)),
                ('level_4', models.CharField(default='Severe', max_length=50)),
                ('level_5', models.CharField(default='Very Severe', max_length=50)),
            ],
            options={
                'verbose_name': 'Symptom',
                'verbose_name_plural': 'Symptoms',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('email_to_confirm', models.EmailField(blank=True, max_length=254, null=True)),
                ('password', models.CharField(max_length=100)),
                ('birth_year', models.PositiveIntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2020)),
                ('ethnicity_top', models.CharField(max_length=50)),
                ('ethnicity_second', models.CharField(blank=True, max_length=50, null=True)),
                ('ethnicity_third', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10)),
                ('sexual_orientation', models.CharField(choices=[('hetero', 'Heterosexual'), ('homo', 'Homosexual'), ('bi', 'Bisexual')], default='hetero', max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(max_length=50)),
                ('confirm_token', models.TextField(blank=True, null=True, unique=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserFactors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.User')),
            ],
            options={
                'verbose_name': 'User-Factors',
                'verbose_name_plural': 'Users-Factors',
            },
        ),
        migrations.CreateModel(
            name='UserSymptomSeverities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.User')),
            ],
            options={
                'verbose_name': 'User-Symptom Severities',
                'verbose_name_plural': 'Users-Symptom Severities',
            },
        ),
        migrations.CreateModel(
            name='UserSingleSymptomSeverity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('selected_level', models.SmallIntegerField(blank=True, null=True)),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.Symptom')),
                ('user_symptom_severities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.UserSymptomSeverities')),
            ],
            options={
                'verbose_name': 'User-Single-Symptom Severity',
                'verbose_name_plural': 'User-Single-Symptom Severities',
            },
        ),
        migrations.CreateModel(
            name='UserIntermittentFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('selected_level', models.SmallIntegerField(blank=True, null=True)),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.Factor')),
                ('user_factors', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wrw.UserFactors')),
            ],
            options={
                'verbose_name': 'User Intermittent Factor',
                'verbose_name_plural': 'User Intermittent Factors',
            },
        ),
        migrations.CreateModel(
            name='UserDailyFactorStart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.Factor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.User')),
            ],
            options={
                'verbose_name': 'User Daily Factor Start',
                'verbose_name_plural': 'User Daily Factor Starts',
            },
        ),
        migrations.CreateModel(
            name='UserDailyFactorMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('selected_level', models.SmallIntegerField(blank=True, null=True)),
                ('is_skipped', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('user_daily_factor_start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.UserDailyFactorStart')),
            ],
            options={
                'verbose_name': 'User Daily Factor Meta',
                'verbose_name_plural': 'User Daily Factor Metas',
            },
        ),
        migrations.CreateModel(
            name='UserDailyFactorEnd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('user_daily_factor_start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.UserDailyFactorStart')),
            ],
            options={
                'verbose_name': 'User Daily Factor End',
                'verbose_name_plural': 'User Daily Factor Ends',
            },
        ),
        migrations.CreateModel(
            name='CurrentUserSymptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.Symptom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.User')),
            ],
            options={
                'verbose_name': 'Current User-Symptom',
                'verbose_name_plural': 'Current User-Symptoms',
            },
        ),
        migrations.CreateModel(
            name='CurrentIntermittentFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.Factor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrw.User')),
            ],
            options={
                'verbose_name': 'Current Intermittent Factor',
                'verbose_name_plural': 'Current Intermittent Factors',
            },
        ),
    ]
