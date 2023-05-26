# Floripa Rent Watch
## Objetivo do projeto
Realizar análises históricas e de tendência da flutuação de preços de aluguel no mercado imobiliário de Florianópolis/SC. Essas análises serão divulgadas em formato de dashboard na internet, por meio de um web-app e bots de rede social, com atualizações contínuas e automatizadas.

## Tecnologias utilizadas
Este projeto foi desenvolvido em Python3 utilizando a framework Scrapy devido à sua robustez e customizabilidade. Recursos como ItemLoaders permitem o tratamento e pré-processamento dos dados. Além disso, Pipelines permitem processar ainda mais os dados e criar um fluxo de informações que garante que não hajam registros duplicados e os integra a um banco de dados PostgreSQL.

## Hospedagem dos serviços de raspagem de dados
Atualmente, o serviço está hospedado em uma máquina virtual (VM) do Google Cloud Computing. Essa decisão foi tomada após analisarmos diversas possibilidades de hospedagem. Embora serviços como ScrapeOps e Zyte tenham sido considerados, optamos por centralizar as operações em um servidor único, incluindo os crawlers e o banco de dados.

## Automação das operações
Para automatizar tarefas utilizamos scripts bash e python agendados no crontab. Configuramos o shebang (declaração de compilador) e as variáveis de ambiente, além das permissões de usuários no OS Debian.

Um dos nossos scripts, por exemplo, envia relatórios semanais com detalhes sobre o último job realizado pela spider. Esses relatórios contêm informações como a quantidade de itens raspados, o sucesso do job e a data de execução.

## Metas

- Enviar relatórios semanais sobre a variação dos preços dos aluguéis em Florianópolis nos períodos semanal, mensal, trimestral, semestral e anual.
- Alimentar um perfil de Twitter automaticamente com as análises mencionadas, por meio de posts.
- Implementar um chatbot responsivo no Telegram, capaz de gerar relatórios dinamicamente com base nos comandos recebidos.
- Desenvolver um web-app com um dashboard interativo para visualização e análise dos dados coletados.

## Como contribuir
Se você deseja contribuir para este projeto, fique à vontade para fazer um fork deste repositório, implementar melhorias e enviar um pull request. Agradecemos antecipadamente pelo seu interesse em ajudar no desenvolvimento deste projeto!

## Licença
Este projeto é licenciado sob a MIT License.
