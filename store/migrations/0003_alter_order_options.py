# Generated by Django 4.1 on 2022-09-14 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'can cancel order')]},
        ),
    ]