from datetime import datetime

from backend.core.interfaces.repositories import(
    ProfessorRepository, AlunoRepository
    )
from backend.core.domain.models import Aluno, Professor


class AlunoRepositoryPostgresMock(AlunoRepository):
    def __init__(self):
        self.database = [
            Aluno(1, 'Joao', datetime.strptime("2001-01-01", "%Y-%m-%d").date(), 'Algum lugar', 'Maria', '3199999999', 'morning'),
            Aluno(2, 'Maria', datetime.strptime("2001-01-02", "%Y-%m-%d").date(), 'Lugar algum', 'Maria', '3199999998', 'morning'),
            ]

    def save(self, aluno: Aluno) -> Aluno | str:
        """Saves an Aluno object to the database. If the save fails, an error
        message is returned.\\"""

        # Verify if the aluno already exists
        if aluno.id is None:
            aluno.id = len(self.database) + 1
            self.database.append(aluno)
            return aluno

        for aluno_database in self.database:
            if aluno_database.id == aluno.id:
                aluno_database = aluno
                return aluno


    def get_by_id(self, aluno_id: int) -> Aluno | str:
        for aluno in self.database:
            if aluno.id == aluno_id:
                return aluno
        return f"Aluno with ID {aluno_id} not found"


    def delete(self, aluno_id: int) -> str:
        
        for aluno_database in self.database:
            if aluno_database.id == aluno_id:
                self.database.remove(aluno_database)
        return "Removed successfully"

    def get_by_name(self, aluno_name: str) -> list[Aluno]:
        results = []
        for aluno in self.database:
            if aluno.name == aluno_name:
                results.append(aluno)
        return results


class ProfessorRepositoryPostgresMock(ProfessorRepository):
    def __init__(self):
        self.database = [Professor(1, 'Maria', 'maria@professora.com', '1234')]

    def verify_login(self, email, password) -> bool:
        for professor_database in self.database:
            if email == professor_database.email and password == professor_database.password:
                return True
        return False

    def save(self, professor: Professor) -> Professor | str:
        """Saves an Professor object to the database. If the save fails, an error
        message is returned.\\"""

        # Verify if the professor already exists
        if professor.id is None:
            professor.id = len(self.database) + 1
            self.database.append(professor)
            return professor

        for professor_database in self.database:
            if professor_database.id == professor.id:
                professor_database = professor
                return professor


    def get_by_id(self, professor_id: int) -> Professor | str:
        for professor in self.database:
            if professor.id == professor_id:
                return professor
        return f"Professor with ID {professor_id} not found"

    def login(self, email, password):
        for professor in self.database:
            if professor.email == email and professor.password == password:
                return True
        return False

    def delete(self, professor_id: int) -> str:
        for professor_database in self.database:
            if professor_database.id == professor_id:
                self.database.remove(professor_database)
        return "Removed successfully"

    def get_by_name(self, professor_name: str) -> list[Professor]:
        results = []
        for professor in self.database:
            if professor.name == professor_name:
                results.append(professor)
        return results
