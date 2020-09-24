# Sistema de cálculo logístico

Sistema de cálculo de rotas logísticas desenvolvido como parte de um teste de seleção para posição de desenvolvedor backend na empresa Koper. O projeto engloba um serviço web seguindo o padrão REST, que recebe dados pertinentes, e calcula a rota mais eficiente de entrega com base em um mapa (grafo), assim como a persistência destes mesmos dados.
## Conteúdo

1. Requisitos
1. Tecnologias
1. Instalação
1. Funcionamento

## Requistos

Este algoritmo tinha alguns requisitos básicos funcionais:

* Deve utilizar a linguagem Python;
* Arquitetura e framework livres;
* Possuir documentação de uso;
* Testes Unitários importantes mas opcionais;
* Não possui a necessidade de um controle de acesso;
* Funcionará como um projeto independente de outros serviços;

## Tecnologias utilizadas
Durante o desenvolvimento do sistema, foi necessário a definição de quais tecnologias atenderiam melhor a demanda, sempre levando em consideração os requisitos definidos. A seguir, as tecnologias, juntamente com a justificativa de sua escolha quando necessário.
* Python 3.8.5
* Django 3.11
 * Selecionado por possuir um controle próprio de rotas, [ORM][1] e sistema de class-based views, que entrega um código muito mais simples e coeso, reduzindo a possibilidade de ocorrerem bugs. Um possível ganho de velocidade e modularidade em outros frameworks como Tornado ou Flask foram levados em conta nesta decisão, onde infelizmente não houve um peso preponderante para a escolha dos mesmos, os benefícios não justificavam a maior quantidade de trabalho braçal __neste projeto específico__.
* Django rest framework 3.11
 * Selecionado para entregar de forma prática as rotas (e o navegador integrado) da api REST, beneficia o projeto, além da praticidade, de ums sitema limpo e organizado de serializadores e viewsets de dados. Não aumenta a complexidade do projeto, uma vez que a arquitetura proposta no mesmo reduz o contato entre partes, tornando o restante do sistema independente dos controladores da API. Cada coisa em seu lugar.
* Postgresql e Sqlite
 * utilizada ambas as bases de dados, sendo o SQLite utilizado em ambiente de desenvolvimento, de forma a reduzir a necessidade computacional durante esta etapa. O ambiente de deploy do sistema roda uma versão atual do banco Postgresql, permitindo as escalabilidade necessária. 
# Instalação

[1]: https://en.wikipedia.org/wiki/Object-relational_mapping