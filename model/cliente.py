from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from unidecode import unidecode



from  model import Base, Contrato
class Cliente(Base):

    """
        Adiciona um novo cliente à base.

        Arguments:
            id_cliente: campo de auto incremento gerado pelo banco.
            nome: número do cliente
            cnpj: cnpj do cliente
            localizacao: endereço comṕleto do cliente
            cep: codigo de endereçamento posta
            numero: número no logradouro
            complemento: informações adicionais do endereço
            bairro: bairro do endereço
            localidade: localidade do cliente
            uf: uf do cliente
            estado: estado do cliente 
            criado_em: data em que o registro foi adicionado à base (geração automática)
            atualizado_em: data em que o registro foi alterado na base (geração automática)
    """

    __tablename__ = 'cli_cliente'
    id_cliente = Column(Integer, primary_key = True, index= True)
    nome = Column(String(254))
    cnpj = Column(String(18), unique=True)
    localizacao = Column(String(254))
    cep = Column(String(254))
    numero = Column(String(254))
    complemento = Column(String(254))
    bairro = Column(String(254))
    localidade = Column(String(254))
    uf = Column(String(254))
    estado = Column(String(254))
    created_on =  Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

    #Cria o relacionamento entre contrato e cliente com cascade delete nos contratos
    contratos = relationship("Contrato", back_populates="cliente", cascade="all, delete", passive_deletes=True,)


    def __init__(self, nome, cnpj, localizacao, cep, numero,complemento, bairro, localidade, uf, estado):
        self.nome = nome
        self.cnpj = cnpj
        self.localizacao = localizacao
        self.cep =cep
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.localidade = localidade
        self.uf = uf
        self.estado = estado
        