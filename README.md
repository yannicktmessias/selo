# selo
Ferramenta de gestão do selo de acessibilidade da Secretaria Municipal da Pessoa com Deficiência (SMPED)

### Passos básicos para instalação da ferramenta

Execute os seguintes comandos no terminal.

Baixe este repositório na sua máquina:
```
$ git clone https://github.com/yannicktmessias/selo.git
```
Instale o python3 e o postgresql
```
$ sudo apt update

$ sudo apt install python3-pip python3-dev python3-venv libpq-dev postgresql postgresql-contrib
```
Abra um prompt do PostgreSQL a partir do usuário padrão postgres:
```
$ sudo -u postgres psql
```
Crie o banco de dados da ferramenta:
```
postgres=# CREATE DATABASE djangoappdb;
```
Crie o usuário para o banco e defina uma senha:
```
postgres=# CREATE USER djangoappdbuser WITH PASSWORD 'password';
```
Modifique alguns parâmetros de conexão para o usuário (requisitos do Django):
```
postgres=# ALTER ROLE djangoappdbuser SET client_encoding TO 'utf8';

postgres=# ALTER ROLE djangoappdbuser SET default_transaction_isolation TO 'read committed';

postgres=# ALTER ROLE djangoappdbuser SET timezone TO 'America/Sao_Paulo';
```
Conceda permissão para o usuário administrar o banco de dados:
```
postgres=# GRANT ALL PRIVILEGES ON DATABASE djangoappdb TO djangoappdbuser;
```
E saia do prompt do PostgreSQL:
```
postgres=# \q
```
Talvez seja necessário iniciar o banco:
```
$ sudo /etc/init.d/postgresql start
```
Para conectar a ferramenta ao banco e definir outras configurações de deploy 

Crie o arquivo `deploy_config.py` na pasta `selo/web_app/django_app/`

Inclua no arquivo tudo o que estiver indicado nos comentários em `selo/web_app/django_app/settings.py`

Crie uma virtual environment do python3 dentro da pasta `selo`:
```
$ python3 -m venv env
```
E ative-a:
```
$ source env/bin/activate
```
Depois instale os packages do Django e do Scrapy:
```
(env) $ pip install -r requirements.txt
```
Crie e aplique as migrações do Django, referentes às tabelas do banco de dados:
```
(env) $ python web_app/manage.py makemigrations
(env) $ python web_app/manage.py migrate
```
Para testar localmente a ferramenta rode:
```
(env) $ python web_app/manage.py runserver localhost
```
Para rodar o sistema em produção é necessário utilizar o comando:
```
(env) $ python web_app/manage.py collectstatic
```
Para desativar sua virtual environment use:
```
(env) $ deactivate
```
