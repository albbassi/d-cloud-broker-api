from pydantic import BaseModel
from typing import Optional, List
from model.contrato import Contrato
from model.item_contrato import ItemContrato

class ItemContratoSchema(BaseModel):
    """ 
        Define como um novo item de contrato a ser inserido na base deve ser representado.
    """
    id_item:int = 1
    nome_item: str ="Serviços de Consultoria"
    quantidade: float=10.00
    fk_contrato:int=1
    valor_unitario: float=1000.00
    valor_total: float=10000.00


class ItemContratoViewSchema(BaseModel):
    """ 
        Define como um registro da tabela itens de contrato será apresentado.
    """
    
    id_item:int = 1
    nome_item: str ="Serviços de Consultoria "
    quantidade: float=10.00
    valor_unitario: float=1000.00
    valor_total: float=10000.00
    fk_contrato:int=1

def ItensContratosApresentacao(itens: List[ItemContrato]):
    """ 
        Retorna uma representação dos Itens de contrato seguindo o schema definido em ContratoViewSchema.
    """
    result = []
    for item in itens:
        result.append({
        "id_item":item.id_item,    
        "nome_item":item.nome_item,
        "quantidade":item.quantidade,
        "valor_unitario":item.valor_unitario,
        "valor_total":item.valor_total,
        })
    return {"itens": result}

def ItemContratoApresenta(item: ItemContrato):
    """ 
        Retorna uma representação do item de contrato seguindo o schema definido em ContratoViewSchema.
    """

    return {
        "id_item":item.id_item,    
        "nome_item":item.nome_item,
        "quantidade":item.quantidade,
        "valor_unitario":item.valor_unitario,
        "valor_total":item.valor_total,
        "fk_contrato":item.fk_contrato
    }
    

class ItemContratoBuscaSchema(BaseModel):
    """ 
        Define como será a estrutura da busca pelo nome do item de contrato.
    """
    nome_item: str = "Serviços de consultoria"


class ItemContratoIdBuscaSchema(BaseModel):
    """ 
        Define como será a estrutura da busca pelo nome do item de contrato.
    """
    id_item: int = 1



class ItensContratoListagemSchema(BaseModel):
    
    """ 
        Define como uma listagem dos Itens de contrato será retornada.
    """
    item:List[ItemContratoSchema]
