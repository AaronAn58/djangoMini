# Generated by Django 5.0.1 on 2024-01-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "账号管理", "verbose_name_plural": "账号管理"},
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="user_permissions",
        ),
        migrations.AddField(
            model_name="customuser",
            name="creator",
            field=models.CharField(max_length=200, null=True, verbose_name="创建人"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="nickname",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="姓名"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(
                blank=True, max_length=11, null=True, verbose_name="电话"
            ),
        ),
    ]