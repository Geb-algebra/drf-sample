import pytest

from api.serializers import (
    EmployeeSerializer,
    DivisionSerializer,
    DivisionModelSerializer,
)
from api.models import Employee, Division


class TestDivisionSerializer:
    @pytest.mark.django_db
    @pytest.fixture
    def divisions(self):
        return [Division.objects.create(name=n) for n in ["Sales", "Planning"]]

    @pytest.mark.django_db
    def test_serialize_single(self, divisions):
        s = DivisionSerializer(divisions[0])
        assert s.data == {"id": 1, "name": "Sales"}

    @pytest.mark.django_db
    def test_serialize_many(self, divisions):
        s = DivisionSerializer(divisions, many=True)
        assert s.data == [
            {"id": 1, "name": "Sales"},
            {"id": 2, "name": "Planning"},
        ]

    @pytest.mark.django_db
    def test_deserialize_single(self, divisions):
        s = DivisionSerializer(data={"id": 3, "name": "Development"})
        assert s.is_valid()
        division_model = s.save()
        assert type(division_model) == Division
        assert division_model.name == "Development"
        assert Division.objects.get(id=3).name == "Development"


class TestDivisionModelSerializer:
    @pytest.mark.django_db
    @pytest.fixture
    def divisions(self):
        return [Division.objects.create(name=n) for n in ["Sales", "Planning"]]

    @pytest.mark.django_db
    def test_serialize_single(self, divisions):
        s = DivisionModelSerializer(divisions[0])
        assert s.data == {"id": 1, "name": "Sales"}

    @pytest.mark.django_db
    def test_serialize_many(self, divisions):
        s = DivisionModelSerializer(divisions, many=True)
        assert s.data == [
            {"id": 1, "name": "Sales"},
            {"id": 2, "name": "Planning"},
        ]

    @pytest.mark.django_db
    def test_deserialize_single(self, divisions):
        s = DivisionModelSerializer(data={"id": 3, "name": "Development"})
        assert s.is_valid()
        division_model = s.save()
        assert type(division_model) == Division
        assert division_model.name == "Development"
        assert Division.objects.get(id=3).name == "Development"

    @pytest.mark.django_db
    def test_is_type_fit_automatically_on_deserialize(self, divisions):
        s = DivisionModelSerializer(data={"id": "hoge", "name": 1024})
        # assert not s.is_valid()
        s.is_valid()
        division_model = s.save()
        assert division_model.name == "1024"


class TestEmployeeSerializer:
    @pytest.mark.django_db
    @pytest.fixture
    def divisions(self):
        return [Division.objects.create(name=n) for n in ["Sales", "Planning"]]

    @pytest.mark.django_db
    @pytest.fixture
    def Employees(self):
        return [Employee.objects.create(name=n) for n in ["Sales", "Planning"]]
        
    @pytest.mark.django_db
    def test_deserialize_invalid(self, divisions):
        s = EmployeeSerializer(data={"id": "hoge", "name": "Alice", "division": "fuga"})
        assert not s.is_valid()
        with pytest.raises(AssertionError):
            s.save()
        # print(s.errors)
