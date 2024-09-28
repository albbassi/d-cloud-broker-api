from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from unidecode import unidecode


from  model import Base

class ItemContrato(Base):
    """
        Adiciona um novo item a contrato existente na base.

        Argumentos:
            id_item: campo de auto incremento gerado pelo banco.
            nome_item: nome do item contratado
            quantidade: quantidade contratada
            valor_unitario: valor unitario do item
            criado_em: data em que o registro foi adicionado à base (geração automática)
            atualizado_em: data em que o registro foi alterado na base (geração automática)
        """


    __tablename__ = 'itc_item_contrato'

    id_item = Column("id_item", Integer, primary_key = True, index= True)
    nome_item = Column(String(100))
    quantidade = Column(Float)
    valor_unitario = Column(Float)
    valor_total = Column(Float)
    criado_em =  Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    #Cria um relacionamento com a tabela contrato através da coluna id_contrato que será 
    #uma chave estrangeira na tabela item contratado
    fk_contrato = Column(Integer, ForeignKey("ctr_contrato.id_contrato", ondelete="CASCADE"))
    contrato = relationship("Contrato", back_populates="itens")

        
    def __init__(self, nome_item, quantidade, valor_unitario,  fk_contrato):
        self.nome_item = nome_item
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.fk_contrato = fk_contrato