import pytest
from datetime import datetime

import sys
sys.path.append('../')
print(sys.path)
from backend.core.domain.models import Aluno
from backend.tests.database_mock import AlunoRepositoryPostgresMock, ProfessorRepositoryPostgresMock
from backend.core.domain.services import AlunoService

class TestAlunoService():

    @pytest.fixture()
    def setup(self):
        aluno_repository = AlunoRepositoryPostgresMock()
        aluno_service = AlunoService(aluno_repository)
        ### adiciona um novo no banco de dados
        return aluno_service


    def test_create_aluno(self, setup):
        name = "John Doe"
        born_date = datetime.strptime("2000-01-01", "%Y-%m-%d").date()
        address = "123 Main St"
        tutor_name = "Jane Doe"
        tutor_phone = "555-555-5555"
        class_shift = "morning"

        result = setup.create_aluno(name, born_date, address, tutor_name, tutor_phone, class_shift)
        #print(result)
        assert result.name == name
        assert result.born_date == born_date
        assert result.address == address
        assert result.tutor_name == tutor_name
        assert result.tutor_phone == tutor_phone
        assert result.class_shift == class_shift


    def test_update_aluno(self, setup):
        name = "Joao Pedro"
        born_date = datetime.strptime("2000-01-01", "%Y-%m-%d").date()
        address = "123 Main St"
        tutor_name = "Maria Joaquina"
        tutor_phone = "666-333333333"
        class_shift = "morning"

        result = setup.update_aluno(1, name, born_date, address, tutor_name, tutor_phone, class_shift)
        
        assert result.name == name
        assert result.born_date == born_date
        assert result.address == address
        assert result.tutor_name == tutor_name
        assert result.tutor_phone == tutor_phone
        assert result.class_shift == class_shift

    def test_remove_aluno(self, setup):
        result = setup.remove_aluno(1)
        assert result is None

    def test_update_aluno_name(self, setup):
        new_name = "Joao Henrique"
    
        result = setup.update_aluno(1, name=new_name)

        assert result.name == new_name

    def test_update_aluno_address(self, setup):
        new_address = "Lugar algum"
    
        result = setup.update_aluno(1, address=new_address)

        assert result.address == new_address

    def test_update_aluno_tutor_name(self, setup):
        new_tutor_name = "Maria Joaquina"
    
        result = setup.update_aluno(1, tutor_name=new_tutor_name)

        assert result.tutor_name == new_tutor_name

    def test_update_aluno_tutor_phone(self, setup):
        new_tutor_phone = "3188888888"
    
        result = setup.update_aluno(1, tutor_phone=new_tutor_phone)

        assert result.tutor_phone == new_tutor_phone

    def test_update_aluno_class_shift(self, setup):
        new_class_shift = "afternoon"
    
        result = setup.update_aluno(1, class_shift=new_class_shift)

        assert result.class_shift == new_class_shift


