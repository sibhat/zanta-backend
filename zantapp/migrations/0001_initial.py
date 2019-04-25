# Generated by Django 2.1.7 on 2019-04-25 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import zantapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.CharField(default=zantapp.models.id_gen, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created time')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated time')),
                ('username', models.CharField(blank=True, max_length=255, verbose_name='Username')),
                ('email', models.EmailField(blank=True, max_length=255, unique=True, verbose_name='email address')),
                ('is_photographer', models.BooleanField(default=False, verbose_name='photographer')),
                ('is_client', models.BooleanField(default=True, verbose_name='client')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', zantapp.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=200, verbose_name='Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.CharField(default=zantapp.models.id_gen, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created time')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated time')),
                ('photo', models.URLField(blank=True, max_length=500)),
                ('Story', models.CharField(blank=True, max_length=500, verbose_name='Story')),
                ('headline', models.CharField(blank=True, max_length=500, verbose_name='headline')),
                ('confirm_spending', models.BooleanField(default=False)),
                ('credits', models.IntegerField(default=0)),
                ('partner_one_first_name', models.CharField(max_length=100)),
                ('partner_one_last_name', models.CharField(max_length=100)),
                ('partner_one_gender', models.CharField(choices=[('male', 'female')], max_length=50)),
                ('partner_two_first_name', models.CharField(max_length=100)),
                ('partner_two_last_name', models.CharField(max_length=100)),
                ('partner_two_gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=50)),
                ('wedding_date', models.DateField(blank=True, verbose_name='wedding date')),
                ('reception_location', models.CharField(blank=True, max_length=5000)),
                ('message', models.CharField(max_length=1000)),
                ('free_apps', models.IntegerField(default=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('friend_of', models.CharField(choices=[('groom', 'bride')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zantapp.Client', verbose_name='Client id')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.CharField(default=zantapp.models.id_gen, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created time')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated time')),
                ('photo', models.URLField(blank=True, max_length=500)),
                ('Story', models.CharField(blank=True, max_length=500, verbose_name='Story')),
                ('headline', models.CharField(blank=True, max_length=500, verbose_name='headline')),
                ('confirm_spending', models.BooleanField(default=False)),
                ('credits', models.IntegerField(default=0)),
                ('company_name', models.CharField(blank=True, max_length=100, verbose_name='company name')),
                ('free_calls', models.IntegerField(default=0)),
                ('postings', models.IntegerField(default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photographer', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=200, verbose_name='Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zantapp.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'Wedding'), (2, 'Baptism'), (3, 'Event')], max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='invitation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zantapp.Services', verbose_name='Invitation Type'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zantapp.Client', verbose_name='Client id'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='zantapp.Question', verbose_name='Question Id'),
        ),
    ]
