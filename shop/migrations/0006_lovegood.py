# Generated by Django 2.1.1 on 2018-10-23 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20181021_1441'),
        ('shop', '0005_goodcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='loveGood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]