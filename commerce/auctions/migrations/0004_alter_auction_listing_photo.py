# Generated by Django 5.0.4 on 2024-04-27 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='photo',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
