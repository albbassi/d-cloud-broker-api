from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session , Contrato, Cliente, ItemContrato
from logger import logger
from schemas import *
from flask_cors import CORS



info = Info(title="API Cloud Broker - MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)


CORS(app)


# definindo tags
documentacao_tag = Tag(name="Documentação", description="Seleção do formato de exibição da documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="1.Cliente", description="Adição, visualização e remoção de clientes da base")
contrato_tag = Tag(name="2.Contrato", description="Adição, visualização e remoção de contratos da base")
item_contrato_tag = Tag(name="3.ItemContrato", description="Adição, visualização e remoção de itens de contrato da base")

@app.get('/',  tags=[documentacao_tag])
def documentacao():
    """
        Redireciona para /openapi. Nesta tela, o usuário pode escolher o estilo de apresentação da documentação.
    """
    return redirect('/openapi')


#----------Cliente-----------------#
# Rotas de Cliente

@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """
        Adiciona um novo Cliente à base de dados

        Retorna uma representação dos Clientes.
    """
    cliente = Cliente(
        nome=form.nome,
        cnpj=form.cnpj,
        localizacao=form.localizacao,
        cep=form.cep,
        numero=form.numero,
        complemento=form.complemento,
        bairro=form.bairro,
        localidade=form.localidade,
        uf=form.uf,
        estado=form.estado

        )
    logger.debug(f"Adicionando um novo cnpj: '{cliente.cnpj}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(cliente)
        # efetivando o comando de adição de novo cliente na tabela
        session.commit()
        logger.debug(f"Adicionado cliente com o cnpj: '{cliente.cnpj}'")
        return ClienteApresenta(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente com mesmo cnpj já salvo na base :/"
        logger.warning(f"Erro ao adicionar: cliente em duplicidade'{cliente.cnpj}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo cliente :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.cnpj}', {error_msg}")
        return {"message": error_msg}, 400

#----------rota para deleção de um cliente----------------#

@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteViewSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """
        Deleta um cliente a partir do seu cnpj

        Retorna uma mensagem confirmando que o cliente foi deletado ou que o mesmo não conta na base.
    """
    cnpj = unquote(unquote(query.cnpj))
    print(cnpj)
    logger.debug(f"Deletando o cnpj #{cnpj}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.cnpj == cnpj).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado o cliente #{cnpj}")
        return {"message": "Cliente removido", "cnpj": cnpj}
    else:
        # se o produto não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cnpj #'{cnpj}', {error_msg}")
        return {"message": error_msg}, 404


#-------------Rota para Listagem dos Clientes e Apresentação na Tabela Clientes--------#
@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ClientesListagemSchema, "404": ErrorSchema})
def get_clientes():
    """
        Faz a busca por todos os clientes cadastrados

        Retorna uma representação da listagem dos clientes atualmente presentes na base.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d Existem atualmente na base % {len (clientes)} clientes")
        # retorna a representação de produto
        print(clientes)
        return ClientesApresentacao(clientes), 200
    

#-------------Rota para Retorno da busca para um Cliente inscrito na Tabela Clientes--------#
@app.get('/cliente', tags=[cliente_tag],
            responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    
    """
        Busca na base um cliente a partir do seu cnpj

        Retorna uma mensagem confirmando que o cliente existe na base.
    """
    cnpj = unquote(unquote(query.cnpj))
    print(cnpj)
    logger.debug(f"procura o cnpj #{cnpj}")
    # criando conexão com a base
    session = Session()
    # verificando se existe o cliente
    achou = session.query(Cliente).filter(Cliente.cnpj == cnpj).first()

    if achou:
        # retorna uma mensagem de confirmação
        logger.debug(f"Cliente encontrato #{cnpj}")
        return {"message": "Cliente Encontrato", "nome": achou.nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"O cnpj não existe na base #'{cnpj}', {error_msg}")
        return {"message": error_msg}, 404
    

@app.put('/cliente', tags=[cliente_tag],
            responses={"200": ClienteViewSchema, "404": ErrorSchema})
def put_cliente(form: ClienteSchema):
    
    """
        Edita as informações de um cliente na base a partir do cnpj

        **<font color="red">OBS:Somente os campos Nome e Endereço serão alterados.</font>**

        Retorna uma mensagem confirmando que o cliente foi editado.
    """
    dados = Cliente(
        nome=form.nome,
        cnpj=form.cnpj,
        localizacao=form.localizacao
         )

    cnpj = unquote(unquote(dados.cnpj))
    print(cnpj)
    logger.debug(f"procura o cnpj # {cnpj}")
    
    # criando conexão com a base
    session = Session()
    
    # verificando se existe o cliente
    achou = session.query(Cliente).filter(Cliente.cnpj == cnpj).first()

    if (achou):
        # retorna uma mensagem de confirmação
        logger.debug(f"Cliente encontrato #{cnpj}")

        if (( dados.nome != achou.nome) and (dados.nome != "")):
            atualiza_nome = dados.nome
        else:
            atualiza_nome = achou.nome
        if (( dados.localizacao != achou.localizacao) and (dados.localizacao != "")):
            atualiza_localizacao = dados.localizacao
        else:
            atualiza_localizacao = achou.localizacao
        
        achou.nome =  atualiza_nome
        achou.localizacao = atualiza_localizacao
        
        # Commit das alterações
        session.commit()

        # Feche a sessão
        session.close()

        return {"message": "Cliente encontrato e dado(s) alterado(s)", "nome": dados.nome}
    else:
        # se o cliente não foi encontrado
        error_msg = "O campo CNPJ não pode ser alterado :/"
        logger.warning(f"O cnpj '{cnpj}' não existe na base #, {error_msg}")
        return {"message": error_msg}, 404
    

#Rotas de contrato
@app.post('/contrato', tags=[contrato_tag],
          responses={"200": ContratoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_contrato(form: ContratoSchema):
    """
        Adicionar um novo contrato à base de dados

        Retorna uma representação dos Contratos.
    """
    contrato = Contrato(
        nr_contrato=form.nr_contrato,
        dt_assinatura=form.dt_assinatura,
        dt_inicio=form.dt_inicio,
        dt_fim=form.dt_fim,
        cotacao_dolar=form.cotacao_dolar,
        tipo_contrato=form.tipo_contrato,
        valor_ctr=form.valor_ctr,
        fk_cliente=form.fk_cliente
        )
    logger.debug(f"Adicionando um novo contrato: '{contrato.nr_contrato}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(contrato)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado contrato de número: '{contrato.nr_contrato}'")
        return ContratoApresenta(contrato), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Contrato de mesmo número já salvo na base :/"
        logger.warning(f"Erro ao adicionar contrato '{contrato.nr_contrato}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo contrato :/"
        logger.warning(f"Erro ao adicionar contrato '{contrato.nr_contrato}', {error_msg}")
        return {"message": error_msg}, 400


# rota de delecao de contratos
@app.delete('/contrato', tags=[contrato_tag],
            responses={"200": ClienteViewSchema, "404": ErrorSchema})
def del_contrato(query: ContratoBuscaSchema):
    
    """
        Deletar um contrato a partir do seu número de registro

        Retorna uma mensagem confirmando que o registro foi deletado ou que o mesmo não conta na base.

    """
    numero_contrato = unquote(unquote(query.nr_contrato))
    print(numero_contrato)
    logger.debug(f"Deletando o contrato número #{numero_contrato}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Contrato).filter(Contrato.nr_contrato == numero_contrato).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado o contrato #{numero_contrato}")
        return {"message": "Contrato removido", "Numero": numero_contrato}
    else:
        # se o produto não foi encontrado
        error_msg = "Contrato não encontrado na base :/"
        logger.warning(f"Erro ao deletar contrato de número #'{numero_contrato}', {error_msg}")
        return {"message": error_msg}, 404


@app.get('/contratos', tags=[contrato_tag],
         responses={"200": ContratosListagemSchema, "404": ErrorSchema})
def get_contratos():

    """
        Buscar todos os contratos cadastrados

        Retorna uma representação da listagem dos contratos atualmente presentes na base.
    """
    logger.debug(f"Coletando contratos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    contratos = session.query(Contrato).all()

    if not contratos:
        # se não há produtos cadastrados
        return {"contratos": []}, 200
    else:
        logger.debug(f"%d Existem na base atualmente % {len (contratos)} contratos")
        # retorna a representação de contrato
        print(contratos)
        return ContratosApresentacao(contratos), 200
    


@app.get('/filtra-contratos', tags=[contrato_tag],
         responses={"200": ContratosListagemSchema, "404": ErrorSchema})
def get_filtra_contratos(query:ClienteBuscaSchema ):

    """
        Buscar todos os contratos cadastrados para o cnpj informado

        Retorna uma representação da listagem dos contratos atualmente presentes na base.
    """
    logger.debug(f"Coletando contratos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    procura = str(query.cnpj)
    contratos = session.query(Contrato).filter(Contrato.cliente.has(cnpj=procura)).all()

    if not contratos:
        # se não há contratos cadastrados
        return {"contratos": []}, 200
    else:
        # retorna a representação de contrato
        print(contratos)
        return ContratosApresentacao(contratos), 200
    

@app.get('/contrato', tags=[contrato_tag],
         responses={"200": ContratoBuscaSchema, "404": ErrorSchema})
def get_contrato(query:ContratoBuscaSchema ):
    
    """
        Faz a busca por um os contrato especifico cadastrado na base

        Retorna uma representação do contrato.
    """
    logger.debug(f"Procurando contrato")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    nr_contrato = unquote(unquote(query.nr_contrato))
    contrato = session.query(Contrato).filter(Contrato.nr_contrato == nr_contrato).first()

    if not contrato:
        # se o contrato não está cadastrado
        return {"contrato": []}, 200
    else:
        logger.debug(f"%d Contrato encontrado - % {(contrato.nr_contrato)} ")
        # retorna a representação de produto
        print(contrato)
        return ContratoApresenta(contrato), 200
    

############PUT CONTRATO############

@app.put('/contrato', tags=[contrato_tag],
            responses={"200": ContratoViewSchema, "404": ErrorSchema})
def put_contrato(form: ContratoSchema):
    
    """
        Edita as informações de um contrato na base a partir do seu número de conbtrato

        **<font color="red">OBS:Preencha apenas os campos dt_assintatura e valor_ctr podem ser alterados.</font>**

        Retorna uma mensagem confirmando que o contrato foi editado e registra no banco a data da alteração.
    """
    dados = Contrato(
        nr_contrato=form.nr_contrato,
        dt_inicio=form.dt_inicio,
        dt_fim=form.dt_fim,
        dt_assinatura = form.dt_assinatura,
        tipo_contrato=form.tipo_contrato,
        valor_ctr=form.valor_ctr,
        fk_cliente=form.fk_cliente
         )

    nr_contrato = unquote(unquote(dados.nr_contrato))
    print(nr_contrato)
    logger.debug(f"procura o contrato # {nr_contrato}")
    # criando conexão com a base
    
    session = Session()
    
    # verificando se existe o contrato
    achou = session.query(Contrato).filter(Contrato.nr_contrato == nr_contrato).first()

    if (achou):
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Contrato encontrato #{nr_contrato}")

        if (( dados.dt_assinatura != achou.dt_assinatura) and (dados.dt_assinatura != "")):
            atualiza_dt_assinatura = dados.dt_assinatura
        else:
            atualiza_dt_assinatura = achou.dt_assinatura
        if (( dados.valor_ctr != achou.valor_ctr) and (dados.valor_ctr != "")):
            atualiza_valor_ctr = dados.valor_ctr
        else:
            atualiza_valor_ctr = achou.valor_ctr
        
        achou.dt_assinatura =  atualiza_dt_assinatura
        achou.valor_ctr = atualiza_valor_ctr
        
        # Commit (confirmar) as alterações
        session.commit()

        # Feche a sessão
        session.close()

        return {"message": "Contrato encontrato e dado(s) alterado(s)", "Data da Assinatura": dados.dt_assinatura, "Valor": dados.valor_ctr }
    else:
        # se o cliente não foi encontrado
        error_msg = "Contrato não encontrado na base :/"
        logger.warning(f"O Contrato '{nr_contrato}' não existe na base #, {error_msg}")
        return {"message": error_msg}, 404



#----------Itens de Contrato-----------------#
# Rotas de Item de Contrato

@app.post('/item_contrato', tags=[item_contrato_tag],
          responses={"200": ItemContratoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_item_contrato(form: ItemContratoSchema):
    """
        Adiciona um novo Item de Contrato à base de dados

        Retorna uma representação dos Itens de Contrato.
    """
    item_contrato = ItemContrato(
        nome_item=form.nome_item,
        quantidade=form.quantidade,
        valor_unitario=form.valor_unitario,
        fk_contrato=form.fk_contrato,
        )
    logger.debug(f"Adicionando um novo item ao contrato: '{item_contrato.nome_item}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando um novo item
        session.add(item_contrato)
        # efetivando o camando de adição de novo item de contrato à tabela
        session.commit()
        logger.debug(f"Adicionado ao contrato o item de nome: '{item_contrato.nome_item}'")
        return ItemContratoApresenta(item_contrato), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "O contrato já possui um item com este nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar item '{item_contrato.nome_item}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item de contrato :/"
        logger.warning(f"Erro ao adicionar item de contrato '{item_contrato.nome_item}', {error_msg}")
        return {"message": error_msg}, 400
        
#----------Itens de Contrato-----------------#
# Rota para listagem de todos os itens de um Contrato    
        
@app.get('/filtra-itens', tags=[item_contrato_tag],
	responses={"200": ItensContratoListagemSchema, "404": ErrorSchema})
def get_filtra_itens(query:ContratoBuscaSchema ):

    """
        Buscar todos os itens contratos cadastrados para o contrato

        Retorna uma representação da listagem dos itens de contrato atualmente presentes na base para o referido contrato.
    """
    logger.debug(f"Coletando itens ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    procura = str(query.nr_contrato)
    itens = session.query(ItemContrato).filter(ItemContrato.contrato.has(nr_contrato=procura)).all()
    print (itens)
    if not itens:
        # se não há contratos cadastrados
        return {"itens": []}, 200
    else:
        # retorna a representação de contrato
        print(itens)
        return ItensContratosApresentacao(itens), 200
    

@app.delete('/filtra-itens', tags=[item_contrato_tag],
            responses={"200": ItemContratoViewSchema, "404": ErrorSchema})
def del_item_contrato(query: ItemContratoIdBuscaSchema):
    
    """
        Deletar um item de contrato a partir do seu ID

        Retorna uma mensagem confirmando que o registro foi deletado ou que o mesmo não conta na base.

    """
    id_item = query.id_item
    logger.debug(f"Deletando o item #{id_item}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(ItemContrato).filter(ItemContrato.id_item == int(id_item)).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado o contrato #{id_item}")
        return {"message": "Contrato removido", "Numero": id_item}
    else:
        # se o produto não foi encontrado
        error_msg = "Contrato não encontrado na base :/"
        logger.warning(f"Erro ao deletar contrato de número #'{id_item}', {error_msg}")
        return {"message": error_msg}, 404

