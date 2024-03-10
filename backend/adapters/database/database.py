"""Database ORM models for SQLAlchemy."""

from sqlalchemy import create_engine, Engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Text
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base

import sys
sys.path.append('../../../')

from backend.core.domain.models import (
    Aluno, ResponsavelPorAluno, PeriodoLetivo, DiaSemAula
)

class DatabaseSession:
    """Database session class for SQLAlchemy. It creates a database engine
    and a session. The engine is used to create the database tables and
    the session is used to query the database. The engine and session
    are passed to the repositories.\\
    """
    def __init__(self):
        """Initializes the database engine and session."""
        ips = ['172.19.0.2', '172.18.0.2']
        for ip in ips:
            try:
                # postgresql://<username>:<password>@<host>:<port>/<database_name>
                self.engine = create_engine(
                    f'postgresql://postgres:postgres@{ip}:5432/postgres',
                    echo=True)
                break  # exit loop if connection is successful
            except Exception as error:
                print(f"Error connecting to {ip}: {error}")
        self.db_session = Session(bind=self.engine)

    def get_db_session(self) -> Session:
        """Returns the SQLAlchemy session."""
        return self.db_session

    def close_db_session(self):
        """Closes the database session."""
        self.db_session.close()

    def get_engine(self) -> Engine:
        """Returns the SQLAlchemy engine."""
        return self.engine


Base = declarative_base()

# Association table
responsavel_aluno_association = Table('responsavel_aluno', Base.metadata,
    Column('responsavel_id', Integer, ForeignKey('responsavel_por_aluno.id')),
    Column('aluno_id', Integer, ForeignKey('aluno.id'))
)


class AlunoORM(Base):
    """Aluno ORM class for SQLAlchemy."""
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    born_date = Column(Date, nullable=False)
    class_shift = Column(String(20), nullable=False)

    # Relationship with ResponsavelPorAlunoORM
    responsaveis = relationship(
        "ResponsavelPorAlunoORM",
        secondary=responsavel_aluno_association,
        back_populates="alunos",
    )

    @staticmethod
    def from_aluno(aluno):
        """Converts an Aluno object to an AlunoORM object."""
        return AlunoORM(
            name=aluno.name,
            born_date=aluno.born_date,
            # school_name=aluno.school_name,
            # commute_type=aluno.commute_type, # se a pé ou acompanhado por alguém
            class_shift=aluno.class_shift
        )

    @staticmethod
    def to_aluno(aluno_orm):
        """Converts an AlunoORM object to an Aluno object."""
        return Aluno(
            id=aluno_orm.id,
            name=aluno_orm.name,
            born_date=aluno_orm.born_date,
            class_shift=aluno_orm.class_shift
        )

class ResponsavelPorAlunoORM(Base):
    """ResponsavelPorAluno ORM class for SQLAlchemy."""
    __tablename__ = 'responsavel_por_aluno'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    kinship = Column(String(100), nullable=False) # se mãe, pai, avó, tia, etc
    identity = Column(String(20), nullable=False)
    cpf = Column(String(11), nullable=False)
    born_date = Column(Date, nullable=False)
    civil_status = Column(String(20), nullable=False)
    street_name = Column(String(100), nullable=False)
    street_number = Column(String(10), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    housing_additional_info = Column(String(100), nullable=False)
    cep = Column(String(8), nullable=False)
    phone = Column(String(20), nullable=False)
    landline = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    observation = Column(String(200), nullable=False)

    # Relationship with AlunoORM
    alunos = relationship(
        "AlunoORM",
        secondary=responsavel_aluno_association,
        back_populates="responsaveis",
    )

    @staticmethod
    def from_responsavel(responsavel):
        """Converts a Responsavel object to a ResponsavelPorAlunoORM object."""
        return ResponsavelPorAlunoORM(
            name=responsavel.name,
            kinship=responsavel.kinship,
            identity=responsavel.identity,
            cpf=responsavel.cpf,
            born_date=responsavel.born_date,
            civil_status=responsavel.civil_status,
            street_name=responsavel.street_name,
            street_number=responsavel.street_number,
            neighborhood=responsavel.neighborhood,
            housing_additional_info=responsavel.housing_additional_info,
            cep=responsavel.cep,
            phone=responsavel.phone,
            landline=responsavel.landline,
            email=responsavel.email,
            observation=responsavel.observation
        )

    @staticmethod
    def to_responsavel(responsavel_orm):
        """Converts a ResponsavelPorAlunoORM object to a Responsavel object."""
        return ResponsavelPorAluno(
            id=responsavel_orm.id,
            name=responsavel_orm.name,
            kinship=responsavel_orm.kinship,
            identity=responsavel_orm.identity,
            cpf=responsavel_orm.cpf,
            born_date=responsavel_orm.born_date,
            civil_status=responsavel_orm.civil_status,
            street_name=responsavel_orm.street_name,
            street_number=responsavel_orm.street_number,
            neighborhood=responsavel_orm.neighborhood,
            housing_additional_info=responsavel_orm.housing_additional_info,
            cep=responsavel_orm.cep,
            phone=responsavel_orm.phone,
            landline=responsavel_orm.landline,
            email=responsavel_orm.email,
            observation=responsavel_orm.observation
        )

class ProfessorORM(Base):
    """Professor ORM class for SQLAlchemy."""
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @staticmethod
    def from_professor(professor):
        """Converts a Professor object to a ProfessorORM object."""
        return ProfessorORM(
            name=professor.name,
            email=professor.email,
            password=professor.password
        )

    @staticmethod
    def to_professor(professor_orm):
        """Converts a ProfessorORM object to a Professor object."""
        return Professor(
            id=professor_orm.id,
            name=professor_orm.name,
            email=professor_orm.email,
            password=professor_orm.password
        )


class PeriodoLetivoORM(Base):
    """PeriodoLetivo ORM class for SQLAlchemy."""
    __tablename__ = 'periodo_letivo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    class_shift = Column(String(100), nullable=False)
    dias_sem_aula = relationship("DiaSemAulaORM", backref="periodo_letivo")

    @staticmethod
    def from_periodo_letivo(periodo_letivo):
        """Converts a PeriodoLetivo object to a PeriodoLetivoORM object."""
        return PeriodoLetivoORM(
            start_date=periodo_letivo.start_date,
            end_date=periodo_letivo.end_date,
            class_shift=periodo_letivo.class_shift
        )

    @staticmethod
    def to_periodo_letivo(periodo_letivo_orm):
        """Converts a PeriodoLetivoORM object to a PeriodoLetivo object."""
        return PeriodoLetivo(
            id=periodo_letivo_orm.id,
            start_date=periodo_letivo_orm.start_date,
            end_date=periodo_letivo_orm.end_date,
            class_shift=periodo_letivo_orm.class_shift
        )


class DiaSemAulaORM(Base):
    """DiaSemAula ORM class for SQLAlchemy."""
    __tablename__ = 'dia_sem_aula'

    id = Column(Integer, primary_key=True, autoincrement=True)
    periodo_letivo_id = Column(Integer, ForeignKey('periodo_letivo.id'), nullable=False)
    date = Column(Date, nullable=False)
    reason = Column(String(100), nullable=False)

    @staticmethod
    def from_dia_sem_aula(dia_sem_aula):
        """Converts a DiaSemAula object to a DiaSemAulaORM object."""
        return DiaSemAulaORM(
            periodo_letivo_id=dia_sem_aula.periodo_letivo_id,
            date=dia_sem_aula.date,
            reason=dia_sem_aula.reason
        )

    @staticmethod
    def to_dia_sem_aula(dia_sem_aula_orm):
        """Converts a DiaSemAulaORM object to a DiaSemAula object."""
        return DiaSemAula(
            id=dia_sem_aula_orm.id,
            periodo_letivo_id=dia_sem_aula_orm.periodo_letivo_id,
            date=dia_sem_aula_orm.date,
            reason=dia_sem_aula_orm.reason
        )


def create_tables(engine: Engine):
    """Creates the database tables."""
    Base.metadata.create_all(engine)


def create_some_alunos(engine: Engine):
    """Creates some Aluno objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    aluno_list = [
        {'name': 'Pedro Souza', 'born_date': '2000-01-01',
         'class_shift': 'Manhã'},
        {'name': 'Maria Silva', 'born_date': '2000-01-02',
         'class_shift': 'Manhã'},
        {'name': 'João Santos', 'born_date': '2000-01-03',
         'class_shift': 'Manhã'},
    ]

    for aluno in aluno_list:
        new_aluno = AlunoORM(name=aluno['name'], born_date=aluno['born_date'],
                             class_shift=aluno['class_shift'])

        existing_aluno = session.query(AlunoORM).filter_by(name=new_aluno.name,
                                                           born_date=new_aluno.born_date).first()
        if existing_aluno: # avoid duplicates and errors for existing data
            continue

        # Insert a new student
        session.add(new_aluno)
        session.commit()

def create_some_responsaveis(engine: Engine):
    """Creates some ResponsavelPorAluno objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    responsavel_list = [
        {'name': 'Ana Souza', 'kinship': 'Mãe', 'identity': '123456',
         'cpf': '12345678901', 'born_date': '1980-01-01',
         'civil_status': 'Casada', 'street_name': 'Rua Dona Flor',
         'street_number': '123', 'neighborhood': 'Bairro Abril',
         'housing_additional_info': 'Casa', 'cep': '32345678',
         'phone': '31995678901', 'landline': '3134567890',
         'email': 'ana@email.com.br', 'observation': ''},
        {'name': 'José Silva', 'kinship': 'Pai', 'identity': '123457',
         'cpf': '12345678902', 'born_date': '1980-01-02',
         'civil_status': 'Casado', 'street_name': 'Rua Dona Flor',
         'street_number': '124', 'neighborhood': 'Bairro Bonsucesso',
         'housing_additional_info': 'Casa', 'cep': '32345679',
         'phone': '31995678902', 'landline': '3134567891',
         'email': 'jose@email.com.br', 'observation': ''},
    ]

    for responsavel in responsavel_list:
        new_responsavel = ResponsavelPorAlunoORM(name=responsavel['name'],
                                                 kinship=responsavel['kinship'],
                                                 identity=responsavel['identity'],
                                                 cpf=responsavel['cpf'],
                                                 born_date=responsavel['born_date'],
                                                 civil_status=responsavel['civil_status'],
                                                 street_name=responsavel['street_name'],
                                                 street_number=responsavel['street_number'],
                                                 neighborhood=responsavel['neighborhood'],
                                                 housing_additional_info=responsavel['housing_additional_info'],
                                                 cep=responsavel['cep'],
                                                 phone=responsavel['phone'],
                                                 landline=responsavel['landline'],
                                                 email=responsavel['email'],
                                                 observation=responsavel['observation'])

        existing_responsavel = session.query(ResponsavelPorAlunoORM).filter_by(cpf=new_responsavel.cpf).first()
        if existing_responsavel:
            continue

        # Insert a new responsible
        session.add(new_responsavel)
        session.commit()
    
    # Retrieve Maria Silva and her parents
    maria = session.query(AlunoORM).filter_by(name='Maria Silva').first()
    ana = session.query(ResponsavelPorAlunoORM).filter_by(name='Ana Souza').first()
    jose = session.query(ResponsavelPorAlunoORM).filter_by(name='José Silva').first()

    # Associate Maria with her parents
    if maria and ana and jose:
        maria.responsaveis.append(ana)
        maria.responsaveis.append(jose)
        session.commit()


def delete_all_responsaveis(engine: Engine):
    """Deletes all ResponsavelPorAluno objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # TODO: Does it delete the relationship between Aluno and ResponsavelPorAluno?
    #       and alunos too?
    # Delete all responsaveis
    session.query(ResponsavelPorAlunoORM).delete()
    session.commit()


def create_some_professor(engine: Engine):
    """Creates some Professor objects and saves it to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    professor_list = [
        {'name': 'William', 'email': 'william@bhzconnection.org.br',
        'password': 'password123'}
    ]
    for professor in professor_list:
        new_professor = ProfessorORM(name=professor['name'],
                                     email=professor['email'],
                                     password=professor['password'])

        existing_professor = session.query(ProfessorORM).filter_by(email=new_professor.email).first()
        if existing_professor: # avoid duplicates and errors for existing data
            continue

        # Insert a new professor
        session.add(new_professor)
        session.commit()

def delete_all_alunos(engine: Engine):
    """Deletes all Aluno objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all alunos
    session.query(AlunoORM).delete()
    session.commit()


def delete_all_professors(engine: Engine):
    """Deletes all Professor objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all professors
    session.query(ProfessorORM).delete()
    session.commit()


def create_some_periodos_letivos(engine: Engine):
    """Creates some PeriodoLetivo objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    periodo_letivo_list = [
        {'start_date': '2023-01-01', 'end_date': '2023-06-30', 'class_shift': 'Manhã'},
    ]

    for periodo_letivo in periodo_letivo_list:
        new_periodo_letivo = PeriodoLetivoORM(start_date=periodo_letivo['start_date'],
                                              end_date=periodo_letivo['end_date'],
                                              class_shift=periodo_letivo['class_shift'])

        existing_periodo_letivo = session.query(PeriodoLetivoORM).filter_by(start_date=new_periodo_letivo.start_date, end_date=new_periodo_letivo.end_date).first()
        if existing_periodo_letivo: # avoid duplicates and errors for existing data
            continue

        # Insert a new periodo letivo
        session.add(new_periodo_letivo)
        session.commit()


def create_some_dias_sem_aula(engine: Engine):
    """Creates some DiaSemAula objects and saves them to the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    dia_sem_aula_list = [
        {'periodo_letivo_id': 1, 'date': '2023-01-01', 'reason': 'Feriado'},
        {'periodo_letivo_id': 1, 'date': '2023-01-02', 'reason': 'Feriado'},
        {'periodo_letivo_id': 1, 'date': '2023-01-03', 'reason': 'Feriado'},
    ]

    for dia_sem_aula in dia_sem_aula_list:
        new_dia_sem_aula = DiaSemAulaORM(periodo_letivo_id=dia_sem_aula['periodo_letivo_id'],
                                        date=dia_sem_aula['date'],
                                        reason=dia_sem_aula['reason'])

        existing_dia_sem_aula = session.query(DiaSemAulaORM).filter_by(periodo_letivo_id=new_dia_sem_aula.periodo_letivo_id, date=new_dia_sem_aula.date, reason=new_dia_sem_aula.reason).first()
        if existing_dia_sem_aula: # avoid duplicates and errors for existing data
            continue

        # Insert a new dia sem aula
        session.add(new_dia_sem_aula)
        session.commit()


def delete_all_periodos_letivos(engine: Engine):
    """Deletes all PeriodoLetivo objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all periodos letivos
    session.query(PeriodoLetivoORM).delete()
    session.commit()

def delete_all_dias_sem_aula(engine: Engine):
    """Deletes all DiaSemAula objects from the database."""
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # Delete all dias sem aula
    session.query(DiaSemAulaORM).delete()
    session.commit()
