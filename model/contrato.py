from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from unidecode import unidecode


from  model import Base

class Contrato(Base):
    """
        Adiciona um novo contrato à base.

        Argumentos:
            id_contrato: campo de auto incremento gerado pelo banco.
            nr_contrato: número interno do contrato
            dt_assinatura: data em que o contrato foi assinado
            dt_inicio: data de inicio da vigência do contrato
            dt_fim: data fim da vigência do contrato
            cotacao_dolar: cotação do dólar na data de assinaura do contrato
            tipo_contrato: indica se o contrato é de despesa ou receita
            valor_ctr: valor total do contrato
            criado_em: data em que o registro foi adicionado à base (geração automática)
            atualizado_em: data em que o registro foi alterado na base (geração automática)
        """


    __tablename__ = 'ctr_contrato'

    id_contrato = Column("id_contrato", Integer, primary_key = True, index= True)
    nr_contrato = Column(String(20), unique = True)
    dt_assinatura = Column(String(15))
    dt_inicio = Column(String(20))
    dt_fim = Column(String(20))
    cotacao_dolar = Column(Float)
    tipo_contrato = Column(String(20))
    valor_ctr = Column(Float)
    criado_em =  Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    #Cria um relacionamento com a tabela cliente através da coluna id_cliente que será 
    #uma chave estrangeira na tabela contrato
    #fk_cliente = Column(Integer, ForeignKey("cli_cliente.id_cliente"))
    fk_cliente = Column(Integer, ForeignKey("cli_cliente.id_cliente", ondelete="CASCADE"))
    cliente = relationship("Cliente", back_populates="contratos")
    #Cria o relacionamento com a tabela item contrato permitindo a deleção em cascade
    itens = relationship("ItemContrato", back_populates="contrato", cascade="all, delete", passive_deletes=True,)


        
    def __init__(self, nr_contrato, dt_assinatura, dt_inicio, dt_fim, valor_ctr, tipo_contrato, fk_cliente, cotacao_dolar):
        self.nr_contrato = nr_contrato
        self.dt_assinatura = dt_assinatura
        self.dt_inicio = dt_inicio
        self.dt_fim = dt_fim
        self.cotacao_dolar = cotacao_dolar
        self.valor_ctr = valor_ctr
        self.tipo_contrato = tipo_contrato
        self.fk_cliente = fk_cliente
