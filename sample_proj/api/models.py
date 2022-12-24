from django.db import models


class Division(models.Model):
    name = models.CharField(max_length=30)  # 部署名


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)  # 社員番号
    name = models.CharField(max_length=30)  # 氏名
    division = models.ForeignKey("Division", on_delete=models.CASCADE)  # 所属部署
