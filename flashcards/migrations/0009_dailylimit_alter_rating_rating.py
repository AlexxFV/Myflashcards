# Generated by Django 5.1.2 on 2024-11-20 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0008_alter_rating_unique_together_rating_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_flashcards', models.PositiveIntegerField(default=20)),
                ('max_collections', models.PositiveIntegerField(default=20)),
            ],
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
