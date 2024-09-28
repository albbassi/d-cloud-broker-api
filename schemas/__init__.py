#schemas para apresentação dos dados de cliente
from schemas.cliente import ClienteSchema, ClienteViewSchema, ClientesApresentacao, ClienteApresenta, ClienteBuscaSchema, ClientesListagemSchema

#schemas para apresentação dos dados de contrato
from schemas.contrato import ContratoSchema, ContratoViewSchema, ContratoApresenta, ContratosApresentacao, ContratoBuscaSchema, ContratosListagemSchema

#schema para apresentação das informações de itens de contrato
from schemas.item_contrato import ItemContratoSchema, ItemContratoViewSchema, ItensContratosApresentacao, ItemContratoApresenta, ItemContratoBuscaSchema, ItensContratoListagemSchema, ItemContratoIdBuscaSchema

#schema para apresentação dos dados de log
from schemas.error import ErrorSchema