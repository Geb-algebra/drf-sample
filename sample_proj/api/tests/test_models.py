import pytest
from django.db import IntegrityError

from api.models import Division, Employee


class TestDivision:
    @pytest.mark.django_db
    @pytest.fixture
    def setup(self):
        for dname in ["Sales", "Planning", "Development"]:
            Division.objects.create(name=dname)

    @pytest.mark.django_db
    def test_can_get_all(self, setup):
        all = Division.objects.all()
        assert len(all) == 3
        for d, name in zip(all, ["Sales", "Planning", "Development"]):
            assert d.name == name

    @pytest.mark.django_db
    def test_can_get_with_filter(self, setup):
        filtered = Division.objects.filter(id__lte=2)
        # filter
        assert len(filtered) == 2
        for d, name in zip(filtered, ["Sales", "Planning"]):
            assert d.name == name

    @pytest.mark.django_db
    def test_can_update(self, setup):
        sales = Division.objects.get(id=1)
        sales.name = "Business"
        sales.save()
        assert Division.objects.get(id=1).name == "Business"
        
    @pytest.mark.django_db
    def test_can_create_delete(self, setup):
        pass

    @pytest.mark.django_db
    def test_is_id_not_added_on_creation(self):
        sales = Division(name="Sales")
        assert sales.id is None

    @pytest.mark.django_db
    def test_is_incremental_integer_id_added_on_save(self):
        sales = Division(name="Sales")
        sales.save()
        assert sales.id == 1
        planning = Division(name="Planning")
        planning.save()
        assert planning.id == 2


class TestEmployee:
    @pytest.mark.django_db
    @pytest.fixture(autouse=True)
    def setup(self):
        for dname in ["Sales", "Planning", "Development"]:
            Division.objects.create(name=dname)

    @pytest.mark.django_db
    def test_is_duplicated_id_not_allowed(self):
        Employee.objects.create(
            id=1001, name="Alice", division=Division.objects.get(name="Sales")
        )
        with pytest.raises(IntegrityError):
            Employee.objects.create(
                id=1001,
                name="Bob",
                division=Division.objects.get(name="Planning"),
            )

    @pytest.mark.django_db
    def test_is_record_updated_on_save_models_with_existing_id(self):
        Employee.objects.create(
            id=1001, name="Alice", division=Division.objects.get(name="Sales")
        )
        who = Employee.objects.get(id=1001)
        assert who.name == "Alice"
        bob = Employee(
            id=1001, name="Bob", division=Division.objects.get(name="Planning")
        )
        bob.save()
        who = Employee.objects.get(id=1001)
        assert who.name == "Bob"

    @pytest.mark.django_db
    def test_can_obtain_division_record_through_foreign_key(self):
        alice = Employee.objects.create(
            id=1001, name="Alice", division=Division.objects.get(name="Sales")
        )
        division = alice.division
        assert type(division) is Division
        assert division.name == "Sales"
