from pydantic import BaseModel
from typing import Optional, List
from model.contrato import Contrato
from model.cliente import Cliente

class ContratoSchema(BaseModel):
    """ 
        Define como um novo contrato deve ser inserido na base deve ser representado.
        
    """
    id_contrato:int = 1 
    nr_contrato: str ="0001"
    dt_assinatura: str="2024-01-01 00:00:00"
    dt_inicio: str="2024-01-01 00:00:00"
    dt_fim: str="2024-01-01 00:00:00"
    tipo_contrato: str="Receita"
    cotacao_dolar:float=1.00
    fk_cliente:int=1
    valor_ctr: float=1000.00


class ContratoViewSchema(BaseModel):
    """ 
        Define como os registros de contrato retornados da base serão apresentados.
    """
    id_contrato: int = 1 
    nr_contrato: str ="0001"
    dt_assinatura: str="2024-01-01 00:00:00"
    dt_inicio: str="2024-01-01 00:00:00"
    dt_fim: str="2024-01-01 00:00:00"
    cotacao_dolar:float=1.00
    tipo_contrato: str="Receita"
    fk_cliente:int=1
    valor_ctr: float=1000.00


def ContratosApresentacao(contratos: List[Contrato]):
    """ 
        Retorna uma representação dos contratos seguindo o schema definido em
        ContratoViewSchema.
    """
    result = []
    for contrato in contratos:
        result.append({
        "id_contrato": contrato.id_contrato, 
        "nr_contrato":contrato.nr_contrato,
        "dt_assinatura":contrato.dt_assinatura,
        "dt_inicio":contrato.dt_inicio,
        "dt_fim":contrato.dt_fim,
        "cotacao_dolar":contrato.cotacao_dolar,
        "tipo_contrato":contrato.tipo_contrato,
        "valor_ctr":contrato.valor_ctr,
        })

    return {"contratos": result}

def ContratoApresenta(contrato: Contrato):
    """ 
        Retorna uma representação do contrato seguindo o schema definido em
        ContratoViewSchema.
    """

    return {
        "id_contrato": contrato.id_contrato,    
        "nr_contrato": contrato.nr_contrato,
        "dt_assinatura": contrato.dt_assinatura,
        "dt_incio": contrato.dt_inicio,
        "dt_fim": contrato.dt_fim,
        "cotacao_dolar":contrato.cotacao_dolar,
        "tipo_contrato": contrato.tipo_contrato,
        "valor_ctr": contrato.valor_ctr,
        "nome": contrato.cliente.nome
    }
    

class ContratoBuscaSchema(BaseModel):
    """ 
        Define como será a estrutura da busca pelo número do contrato.
    """
    nr_contrato: str = "0001"



class ContratosListagemSchema(BaseModel):
    
    """ 
        Define como uma listagem de contratos será retornada.
    """
    contratos:List[ContratoSchema]
