from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import event



import os

# importando os elementos definidos no modelo
from model.base import Base
from model.item_contrato import ItemContrato
from model.contrato import Contrato
from model.cliente import Cliente

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path


# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)


# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

#Evento criado para setar a configuração do banco sqlite para aceitar foreign key suport
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# criação do função para o gatilho # Criação do trigger
def calcular_produto(mapper, connection, target):
    target.valor_total = target.quantidade * target.valor_unitario

# Adicionar o trigger ao evento before_insert
event.listen(ItemContrato, 'before_insert', calcular_produto)
