# Generated by Django 3.2.16 on 2023-05-10 07:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20230510_1342'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_name_owner',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'following')},
        ),
    ]
