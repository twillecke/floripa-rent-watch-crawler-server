# Floripa Rent Watch
## Objetivo do projeto
O objetivo deste projeto é realizar análises históricas e de tendência da flutuação de preços de aluguel no mercado imobiliário de Florianópolis/SC. Essas análises serão divulgadas em formato de dashboard na internet, por meio de um web-app e bots de rede social, com atualizações contínuas e automatizadas.

## Tecnologias utilizadas
Este projeto foi desenvolvido utilizando o framework Scrapy devido à sua robustez, customizabilidade e facilidade de implementação. Recursos como ItemLoaders permitem o tratamento e pré-processamento dos dados de forma simples. Alguns exemplos de uso do ItemLoaders são o tratamento de caracteres e a formatação. Além disso, utilizamos Pipelines para processar ainda mais os dados e criar um fluxo de informações. Os Pipelines garantem que não tenhamos registros duplicados e armazenam as informações coletadas em um banco de dados PostgreSQL.

## Hospedagem dos serviços de raspagem de dados
Atualmente, o serviço de raspagem de dados está hospedado em uma máquina virtual (VM) do Google Cloud Computing. Essa decisão foi tomada após analisarmos diversas possibilidades de hospedagem. Embora serviços como ScrapeOps e Zyte tenham sido considerados, optamos por centralizar tudo em um único servidor, incluindo os crawlers e o banco de dados. A solução de hospedagem em uma máquina virtual da Google foi a escolha ideal para atender a essas necessidades.

## Automação com scripts bash e crontab
Para automatizar tarefas e minimizar a interação humana, utilizamos scripts bash e o agendador de tarefas crontab. Configuramos o shebang (declaração de compilador) e as variáveis de ambiente, além das permissões de usuários no sistema operacional Debian. Essas configurações garantem que os scripts sejam executados corretamente pelo cronjob. Além disso, configuramos o arquivo .profile para carregar corretamente as variáveis de ambiente durante a execução dos scripts em Python.

Um dos nossos scripts envia relatórios semanais com detalhes sobre o último job realizado pela spider. Esses relatórios contêm informações como a quantidade de itens raspados, o sucesso do job e a data de execução.

## Metas
Nossas metas principais incluem:

Enviar relatórios semanais sobre a variação dos preços dos aluguéis em Florianópolis nos períodos semanal, mensal, trimestral, semestral e anual.
Alimentar um perfil de Twitter automaticamente com as análises mencionadas, por meio de posts. Referência: Dólar Bipolar; GPU Bipolar.
Implementar um chatbot responsivo no Telegram, capaz de gerar relatórios dinamicamente com base nos comandos recebidos.
Desenvolver um web-app com um dashboard interativo para visualização e análise dos dados coletados.

## Como contribuir
Se você deseja contribuir para este projeto, fique à vontade para fazer um fork deste repositório, implementar melhorias e enviar um pull request. Agradecemos antecipadamente pelo seu interesse em ajudar no desenvolvimento deste projeto!
