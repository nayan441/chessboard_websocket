# Generated by Django 4.1.4 on 2022-12-19 18:34

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
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_side', models.CharField(default='white', max_length=10)),
                ('owner_online', models.BooleanField(default=False)),
                ('opponent_online', models.BooleanField(default=False)),
                ('fen', models.CharField(blank=True, max_length=92, null=True)),
                ('pgn', models.TextField(blank=True, null=True)),
                ('winner', models.CharField(blank=True, max_length=20, null=True)),
                ('level', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Game Created. Waiting for opponent'), (2, 'Game Started'), (3, 'Game Ended')], default=1)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
