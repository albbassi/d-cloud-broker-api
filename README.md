# MVP - API Cadastro de Clientes

Esta aplicação é o ponta pé inicial do projeto para criação de um sistema de gestão de contratos multinuvem (Cloud Broker). O sistema será dividido em módulos que farão a gestão de: Clientes, Contratos, Itens de contrato, Faturamento, Demandas, Usuários, Gestores e Billing. A implementação em forma de API, visa facilitar a integração com as ferramentas corporativas já em produção e ferrramentas de parceiros.  


# Tecnologias #

A versão atual da aplicação utiliza:

- flask (https://flask.palletsprojects.com/en/3.0.x/)
- sqlite (https://www.sqlite.org/)
- docker (https://www.docker.com/)
- sqlAlchemy (https://www.sqlalchemy.org/)
- OpenAPI (https://swagger.io/specification/)



# Atenção

Como o projeto está na fase de MVP, foi utlizada uma base Sqlite3 e esta precisa de configurações extras para permitir "delete cascade" (1). Além disso, foi criado um trigger para automatizar o cálculo do valor total dos produtos (2).

1. No arquivo **models/__init__.py** foi criado um evento para habilitar o suporte à foreignKey que não é nativo do Sqlite3. Essa configuração permite a execução de delete cascade nas tabelas.

    @event.listens_for(engine, "connect") \
        def set_sqlite_pragma(dbapi_connection, connection_record):\
            cursor = dbapi_connection.cursor()\
            cursor.execute("PRAGMA foreign_keys=ON")\
            cursor.close()\

2. Criação de um trigger para que na tabela item de contrato o valor total fosse calculado a partir dos dados inserido nas colunas valor unitário e quantidade preenchendo automaticamente a coluna valor total.

    Criação do trigger\
    def calcular_produto(mapper, connection, target):\
        target.valor_total = target.quantidade * target.valor_unitario\

    Adicionar o trigger ao evento before_insert\
        event.listen(ItemContrato, 'before_insert', calcular_produto)\

#### Documentação SQLITE: [https://www.sqlite.org/lang_createtrigger.html]

---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```$ docker build -t d-cloud-broker-api .```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```$ docker run -p 5000:5000 d-cloud-broker-api```

<hr>

**Fique Atento!**

Ao utilizar o Swagger para realizar operações de inserção, atualização ou exclusão de dados, é crucial seguir a sequência correta de inserção. Primeiro, deve-se cadastrar um Cliente, seguido pela criação de um Contrato e, por fim, a inclusão de um Item de Contrato. É fundamental estar ciente de que estas entidades - Cliente, Contrato e Item de Contrato - estão interligadas e possuem restrições associadas.

<hr>

**Finalmente**

Acesse [http://localhost:5000/](http://localhost:5000/) no seu navegador para selecionar o modo de visualização da documentação da API em execução.
<br>

**Divirta-se!**

