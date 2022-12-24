from rest_framework import serializers

from api.models import Employee, Division


class DivisionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)

    def create(self, validated_data: dict):
        """.save()を既存のDivisionを引数に**渡さず**呼び出したときに呼び出される"""
        return Division.objects.create(**validated_data)

    def update(self, division, validated_data: dict):
        """.save()を既存のDivisionを引数に**渡して**呼び出したときに呼び出される"""
        division.name = validated_data.get("name", division.name)
        division.save()
        return division


class DivisionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "division"]
