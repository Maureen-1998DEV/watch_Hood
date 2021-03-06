# Generated by Django 3.2.8 on 2021-10-30 14:02

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('occupants', models.IntegerField(null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neighborapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('bio', models.CharField(max_length=300)),
                ('profile_pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='profile/')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('type', models.CharField(max_length=50, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('neighborhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neighborapp.neighborhood')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neighborapp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=150, null=True)),
                ('email', models.EmailField(max_length=60)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neighborapp.category')),
                ('neighborhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_neighbourhood', to='neighborapp.neighborhood')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
