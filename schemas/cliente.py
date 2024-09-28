from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente

class ClienteSchema(BaseModel):
    
    """ 
        Formato dos dados recebidos pela API para inserção de um cliente na base.
    """
    id_cliente: int = 1
    nome: str ="Pontifícia Universidade Católica do Rio de Janeiro"
    cnpj: str ="33.555.921/0001-70"
    cep: str = "22.451-900"
    localizacao: str ="Rua Marquês de São Vicente"
    numero: str = "225"
    complemento: str = "não possui"
    bairro: str ="Gávea"
    localidade: str = "Rio de Janeiro"
    uf: str = "Rio de janeiro"
    estado: str = "Rio de Janeiro"


class ClienteViewSchema(BaseModel):
    
    """ 
        Formato do dado retornado pela API com as informações relativas a um cliente cadsatrado na base.
    """
    id_cliente: int = 1
    nome: str ="Pontifícia Universidade Católica do Rio de Janeiro"
    cnpj: str ="33.555.921/0001-70"
    cep: str = "22.451-900"
    localizacao: str ="Rua Marquês de São Vicente"
    numero: str = "225"
    complemento: str= ""
    bairro: str ="Gávea"
    localidade: str = "Rio de Janeiro"
    uf: str = "Rio de janeiro"
    estado: str = "Rio de Janeiro"


def ClientesApresentacao(clientes: List[Cliente]):

    """ 
        Formato dos dados retornados pela API com todos os registros existentes na tabela cli_cliente. Segue o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
        "id_cliente": cliente.id_cliente,
        "nome":cliente.nome,
        "cnpj":cliente.cnpj,
        "localizacao":cliente.localizacao,
        "cep":cliente.cep,
        "numero":cliente.numero,
        "complemento":cliente.complemento,
        "bairro":cliente.bairro,
        "localidade":cliente.localidade,
        "uf":cliente.uf,
        "estado":cliente.estado
        })

    return {"clientes": result}

def ClienteApresenta(cliente:Cliente):
    
    """ 
        Formato do dado retornado pela API de um registro da tabela cli_cliente. Segue o schema definido em
        ClienteViewSchema.
    """
    return {
    	"id_cliente": cliente.id_cliente,
        "nome":cliente.nome,
        "cnpj":cliente.cnpj,
        "localizacao":cliente.localizacao,
        "cep":cliente.cep,
        "numero":cliente.numero,
        "complemento":cliente.complemento,
        "bairro":cliente.bairro,
        "localidade":cliente.localidade,
        "uf":cliente.uf,
        "estado":cliente.estado
    }

class ClienteBuscaSchema(BaseModel):
    """ 
        Formato do dado recebido pela API para busca na base através do campo CNPJ.
    """
    cnpj: str = "33.555.921/0001-70"


class ClientesListagemSchema(BaseModel):
    
    """ 
        Formato do dado retornado pela API com todos os clientes da base.
    """
    clientes:List[ClienteSchema]
