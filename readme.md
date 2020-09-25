# Sistema de cálculo logístico

Sistema de cálculo de rotas logísticas desenvolvido como parte de um teste de seleção para posição de desenvolvedor backend na empresa Koper. O projeto engloba um serviço web seguindo o padrão REST, que recebe dados pertinentes, e calcula a rota mais eficiente de entrega com base em um mapa (grafo), assim como a persistência destes mesmos dados.
## Conteúdo

1. Requisitos
1. Tecnologias
1. Instalação
1. Funcionamento

## Requistos
### Funcionais
Este algoritmo tinha alguns requisitos básicos funcionais:

* Deve utilizar a linguagem Python;
* Arquitetura e framework livres;
* Possuir documentação de uso;
* Testes Unitários importantes mas opcionais;
* Não possui a necessidade de um controle de acesso;
* Funcionará como um projeto independente de outros serviços;
* Para melhor compreensão do exemplo, os dados retornados no cálculo e os parâmetros solicitados estão em português, mas, para facilitar a manutenção, as variáveis internas do código encontram-se em inglês. Deixando claro que foi uma decisão para melhorar a ergonomia do uso, e não uma falha.
* Para facilitar o teste do sistema, o arquivo com as variáveis de ambiente (`.venv`) foi disponibilizado junto ao repositório. Esta é uma má-pratica. Este arquivo deve ir para o `.gitignore` em um projeto real.
* Como decisão de engenharia, não foram incluídos testes automatizados neste projeto. O responsável possui conhecimento e domínio da ferramenta Unittest, mas, devido a complexidade dos pontos a serem testados, e o curto espaço de tempo no qual o projeto foi realizado, não pode-se levantar os requisitos funcionais e operacionais necessários para um plano de testes coeso. Em contrapartida, a documentação de uso da API inclui casos de uso utilizados durante o teste prático da ferramenta.
### Requisitos para deploy e funcionamento
1. Python 3.8 ou superior e o pip;
1. Software de requisições REST, Postman, Insomnia ou similar;
## Tecnologias utilizadas
Durante o desenvolvimento do sistema, foi necessário a definição de quais tecnologias atenderiam melhor a demanda, sempre levando em consideração os requisitos definidos. A seguir, as tecnologias, juntamente com a justificativa de sua escolha quando necessário.
* [Python 3.8.5][1]
* [Django 3.11][2]
    * Selecionado por possuir um controle próprio de rotas, [ORM][3] e sistema de class-based views, que entrega um código muito mais simples e coeso, reduzindo a possibilidade de ocorrerem bugs. Um possível ganho de velocidade e modularidade em outros frameworks como Tornado ou Flask foram levados em conta nesta decisão, onde infelizmente não houve um peso preponderante para a escolha dos mesmos, os benefícios não justificavam a maior quantidade de trabalho braçal __neste projeto específico__.
* [Django rest framework 3.11][7]
    * Selecionado para entregar de forma prática as rotas (e o navegador integrado) da api REST, beneficia o projeto, além da praticidade, de ums sitema limpo e organizado de serializadores e viewsets de dados. Não aumenta a complexidade do projeto, uma vez que a arquitetura proposta no mesmo reduz o contato entre partes, tornando o restante do sistema independente dos controladores da API. Cada coisa em seu lugar.
* [Sqlite][8] e [PostgreSQL][9]
    * utilizada ambas as bases de dados, sendo o SQLite utilizado em ambiente de desenvolvimento, de forma a reduzir a necessidade computacional durante esta etapa. O ambiente de deploy do sistema roda uma versão atual do banco Postgresql, permitindo as escalabilidade necessária. 
# Instalação
1. Clonar o [repositório][4] para uma pasta local;
1. Dentro da pasta, é necessário criar um ambiente virtual, isolando as versões de python do projeto e do sistema.
    * O comando usado para gerar a mesma é `python3 -m venv nomeDaPastaDeDestino`, podendo diferenciar-se se o sistema utiliza algum gerenciador de versões para a linguagem.
1. Deve-se ativar o ambiente virtual. 
    * No Windows o comando é `'.\PathDaVenv\Scripts\activate.bat'`. NO Osx e sistemas Unix-like (linux, freebsd, etc), o comando é `% source PathDaVenv\bin\activate`
1. Após ativado, dentro da pasta raiz do projeto (onde encontra-se o arquivo `manage.py`), é necessário realizar as migrações com o comando `python manage.py migrate`, não é necessário preocupar-se com a criação da base de dados, o python possui suporte nativo ao banco SQLite, o suficiente para o teste;
1. O sistema deve ser iniciado com o comando `python manage.py runserver`, e ficará disponível no endereço local, tanto a interface da [API][5] quanto da [interface de administração][6] do sistema.
1. É recomendado (mas não obrigatório) o uso da ferramenta [Postman][10] para o teste do sistema. Similares funcionarão da mesma forma, porém, o postman integra-se com a documentação.

## Funcionamento
O sistema possui três interfaces de comunicação:
* A Interface de administração do próprio Django. Pode ser acessada por [esta URL][6], sendo necessário a criação de um superuser antes. Esta interface permite a manipulação visual da base de dados.
    * Para criar um superuser, deve-se usar o comando `python manage.py createsuperuser` na pasta raiz do sistema, e completar os dados solicitados (somente username e password são obrigatórios).
* A interface visual da API. O uso da lib Django Rest Framework nos entrega uma interface básica de testes e visualização da API, através [da mesma url][5] da API.
* O acesso a API diretamente, usando a url [`http://127.0.0.1:8000/api/`][5], juntamente com os endpoints de cada funcionalidade.

A documentação da API encontra-se no seguinte endereço:
[https://documenter.getpostman.com/view/4921337/TVKHTF56][11]

## Status do projeto
Este projeto não possui previsão de ser ampliado, revisado ou corrigido. Informações adicionais, podem ser solicitadas pelo [email][12] do autor.









[1]:https://www.python.org/downloads/release/python-385/
[2]: https://docs.djangoproject.com/en/3.1/
[3]: https://en.wikipedia.org/wiki/Object-relational_mapping
[4]: https://github.com/moreiradiego/grafos
[5]: http://127.0.0.1:8000/api/
[6]: http://127.0.0.1:8000/admin/
[7]: https://www.django-rest-framework.org/
[8]: https://sqlite.org/
[9]: https://www.postgresql.org/
[10]: https://www.postman.com/
[11]: https://documenter.getpostman.com/view/4921337/TVKHTF56
[12]: diego@moreira.bio.br