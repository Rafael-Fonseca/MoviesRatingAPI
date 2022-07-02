# MoviesRatingAPI
Uma REST API que consome uma API de validação de login e a OMDB API para obter informações sobre filmes esta API vai ainda prover várias funcionalidades para tornar possível iteração entre os usuários sobre suas opiniões dos filmes.

# Como executar esta API

1° Crie uma virtual env  
    `python3 -m venv project-venv`

2° Instale as dependências com o comando  
    `pip install -r requirements.txt`

3° Crie um banco de dados postegres, local com o nome movies_rating_db e senha 123  
OU altere a variável SQLALCHEMY_DATABASE_URL constante no arquivo MoviesRatingAPI/sql_app/database.py  
Para o padrão "postgresql://postgres:<SUA SENHA>@localhost/<NOME DO SEU BANCO>" sem os chevrons <>  

4° Popule a tabela profiles(que representam os perfis do usuário)  
executando os scripts sql constantes em MoviesRatingAPI/sql_app/initial_config/profiles_script.sql  
na ferramenta de sua preferência para se conectar com o banco, eu utilizei o pgAdmin4.  

5° Em um terminal, na raiz do projeto, execute o comando:  
` uvicorn main:app`

6° O terminal irá informar uma url onde a sua api está disponível  
Para checar todos os endpoints da API bem como, sua documentação adicione /docs ao final da URL apresentada.  
Como no exemplo http://127.0.0.1:8000/docs
