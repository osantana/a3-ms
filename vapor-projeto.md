# Vapor: Plataforma de Venda e Distribuição Digital de Jogos

Professor: João Armênio <joao.armenio@ulife.com.br>

Equipe:

 * Osvaldo Santana Neto <172320146@ulife.com.br>
 * João Roiko <...@ulife.com.br>
 * ... <...@ulife.com.br>

## Tema

Desenvolvimento de uma plataforma web de comércio eletrônico voltada à venda, distribuição e gerenciamento de jogos digitais.

## Descrição do Projeto

O **Vapor** é uma aplicação web que permite a compra, venda e download de jogos digitais. A plataforma conecta duas categorias de usuários: **jogadores**, que navegam por um catálogo, compram títulos e gerenciam sua biblioteca pessoal; e **criadores**, que cadastram, precificam e distribuem seus jogos.

O sistema contempla funcionalidades essenciais de uma loja digital: catálogo com busca e filtros, carrinho de compras, processamento de pagamentos, biblioteca pessoal com gerenciamento de downloads e solicitação de reembolso.

## Análise de Requisitos

### Requisitos Funcionais

**RF-01: Cadastro de usuário**
> O sistema deve permitir o registro de novos usuários com e-mail, senha e nome de exibição.
>
> Prioridade: Essencial

**RF-02: Autenticação**
> O sistema deve permitir login e logout com credenciais de e-mail e senha.
>
> Prioridade: Essencial

**RF-03: Perfis de acesso**
> O sistema deve distinguir três perfis: Jogador, Criador e Administrador.
>
> Prioridade: Essencial

**RF-04: Catálogo de jogos**
> O sistema deve exibir uma listagem paginada de jogos disponíveis para compra.
>
> Prioridade: Essencial

**RF-05: Busca e filtros**
> O sistema deve permitir busca por nome e filtragem por gênero, preço, plataforma e data de lançamento.
>
> Prioridade: Essencial

**RF-06: Página de detalhes do jogo**
> O sistema deve exibir informações detalhadas de cada jogo: descrição, mídia, requisitos de sistema e preço.
>
> Prioridade: Essencial

**RF-07: Carrinho de compras**
> O sistema deve permitir adicionar, remover e visualizar itens em um carrinho antes da compra.
>
> Prioridade: Essencial

**RF-08: Processamento de pagamento**
> O sistema deve processar pagamentos via cartão de crédito, PIX e saldo da carteira virtual.
>
> Prioridade: Essencial

**RF-09: Carteira virtual**
> O sistema deve permitir que o jogador adicione fundos a uma carteira e utilize o saldo em compras.
>
> Prioridade: Importante

**RF-10: Biblioteca pessoal**
> O sistema deve manter uma biblioteca com todos os jogos adquiridos pelo jogador.
>
> Prioridade: Essencial

**RF-11: Download de jogos**
> O sistema deve fornecer links de download para os jogos presentes na biblioteca do jogador.
>
> Prioridade: Essencial

**RF-12: Cadastro de jogos (criador)**
> O sistema deve permitir que criadores cadastrem novos jogos com metadados, mídias e arquivos de instalação.
>
> Prioridade: Essencial

**RF-13: Gerenciamento de preços**
> O sistema deve permitir que criadores definam e alterem o preço de seus jogos.
>
> Prioridade: Essencial

**RF-14: Painel de vendas (criador)**
> O sistema deve exibir ao criador métricas de vendas: unidades vendidas e receita.
>
> Prioridade: Importante

**RF-15: Reembolso**
> O sistema deve permitir a solicitação de reembolso dentro de um prazo configurável após a compra.
>
> Prioridade: Desejável

**RF-16: Moderação de jogos (administrador)**
> O sistema deve fornecer ao administrador uma fila de jogos submetidos para revisão, permitindo aprová-los ou rejeitá-los antes de ficarem disponíveis no catálogo.
>
> Prioridade: Essencial

### Requisitos Não Funcionais

**RNF-01: Responsividade**
> A interface deve ser utilizável em dispositivos com largura mínima de 375px (mobile) até desktop.
>
> Categoria: Usabilidade

**RNF-02: Tempo de resposta**
> As páginas do catálogo devem carregar em no máximo 2 segundos sob carga normal.
>
> Categoria: Desempenho

**RNF-03: Disponibilidade**
> O sistema deve ter disponibilidade mínima de 99% (exceto janelas de manutenção programada).
>
> Categoria: Confiabilidade

**RNF-04: Segurança de senhas**
> Senhas devem ser armazenadas com hash seguro (bcrypt ou argon2) e nunca trafegar em texto plano.
>
> Categoria: Segurança

**RNF-05: HTTPS obrigatório**
> Toda comunicação entre cliente e servidor deve ocorrer via HTTPS/TLS.
>
> Categoria: Segurança

**RNF-06: Proteção contra fraudes**
> O módulo de pagamento deve validar dados e implementar proteção contra ataques de replay e CSRF.
>
> Categoria: Segurança

**RNF-07: Escalabilidade horizontal**
> A arquitetura deve permitir escalar horizontalmente os serviços de catálogo e download de forma independente.
>
> Categoria: Escalabilidade

**RNF-08: Armazenamento de arquivos**
> Arquivos de jogos devem ser armazenados em serviço de object storage com redundância geográfica.
>
> Categoria: Infraestrutura

**RNF-09: Internacionalização**
> O sistema deve suportar pelo menos pt-BR e en-US na interface.
>
> Categoria: Usabilidade

**RNF-10: Acessibilidade**
> A interface deve seguir as diretrizes WCAG 2.1 nível AA.
>
> Categoria: Usabilidade

**RNF-11: Compatibilidade**
> O sistema deve funcionar nos navegadores Chrome, Firefox, Safari e Edge em suas duas últimas versões estáveis.
>
> Categoria: Portabilidade

**RNF-12: LGPD**
> O sistema deve estar em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).
>
> Categoria: Legal

### Regras de Negócio

**RN-01: Condições de reembolso**
> O reembolso só pode ser solicitado em até 14 dias após a compra e com menos de 2 horas de uso registrado.

**RN-02: Split de receita**
> O criador recebe 70% do valor líquido de cada venda; os 30% restantes são retidos pela plataforma.

**RN-03: Compra única por título**
> Um jogo já presente na biblioteca do jogador não pode ser comprado novamente.

**RN-04: Reembolso via carteira**
> Reembolsos aprovados devolvem o valor à carteira virtual, não ao meio de pagamento original.

**RN-05: Aprovação de jogos**
> Jogos cadastrados por criadores ficam com status "Em análise" até aprovação do administrador e só aparecem no catálogo após aprovados.

## User Stories

### Jogador

**US-01: Cadastro**
> Como jogador, quero me cadastrar na plataforma com meu e-mail e senha, para ter acesso ao catálogo e poder realizar compras.

Critérios de aceitação:
- Validação de formato de e-mail.
- Senha com no mínimo 8 caracteres, contendo letra e número.
- Confirmação de e-mail via link enviado ao endereço informado.
- Exibição de mensagem de erro caso o e-mail já esteja cadastrado.

**US-02: Login**
> Como jogador, quero fazer login com meu e-mail e senha, para acessar minha conta e biblioteca.

Critérios de aceitação:
- Redirecionamento para a página principal após login bem-sucedido.
- Mensagem de erro genérica para credenciais inválidas (sem revelar se o e-mail existe).
- Bloqueio temporário após 5 tentativas falhas consecutivas.

**US-03: Navegar pelo catálogo**
> Como jogador, quero navegar pelo catálogo de jogos disponíveis, para descobrir novos títulos.

Critérios de aceitação:
- Listagem paginada com 20 jogos por página.
- Exibição de capa, nome e preço de cada jogo.
- Ordenação por relevância, preço e data de lançamento.

**US-04: Buscar e filtrar jogos**
> Como jogador, quero buscar jogos por nome e aplicar filtros, para encontrar rapidamente o que procuro.

Critérios de aceitação:
- Campo de busca com sugestão automática (autocomplete).
- Filtros combinados: gênero, faixa de preço, plataforma (Windows/macOS/Linux).
- Resultados atualizados sem recarregar a página (AJAX/SPA).

**US-05: Visualizar detalhes do jogo**
> Como jogador, quero ver a página de detalhes de um jogo, para decidir se quero comprá-lo.

Critérios de aceitação:
- Exibição de: descrição, screenshots/trailer, gêneros, data de lançamento, criador, requisitos de sistema e preço.
- Botão "Adicionar ao Carrinho" visível (ou "Na Biblioteca" se já adquirido).

**US-06: Adicionar ao carrinho**
> Como jogador, quero adicionar jogos ao meu carrinho de compras, para adquirir múltiplos títulos em uma única transação.

Critérios de aceitação:
- Feedback visual ao adicionar item.
- Impedimento de adicionar jogo já presente no carrinho ou na biblioteca.
- Contador de itens visível no ícone do carrinho.

**US-07: Finalizar compra**
> Como jogador, quero finalizar a compra dos jogos no meu carrinho, para adicioná-los à minha biblioteca.

Critérios de aceitação:
- Resumo do pedido com itens e valor total.
- Seleção de meio de pagamento (cartão, PIX, saldo da carteira).
- Confirmação de compra com número do pedido.
- Jogos adicionados automaticamente à biblioteca após pagamento confirmado.

**US-08: Acessar a biblioteca**
> Como jogador, quero acessar minha biblioteca pessoal, para ver e gerenciar os jogos que possuo.

Critérios de aceitação:
- Listagem de todos os jogos adquiridos com capa e nome.
- Busca e ordenação dentro da biblioteca.
- Botão de download em cada título.

**US-09: Baixar um jogo**
> Como jogador, quero baixar um jogo da minha biblioteca, para instalá-lo no meu computador.

Critérios de aceitação:
- Geração de link de download temporário e seguro (URL assinada com expiração).
- Indicação do tamanho do arquivo antes do download.
- Seleção de plataforma quando o jogo tiver múltiplas versões.

**US-10: Solicitar reembolso**
> Como jogador, quero solicitar o reembolso de um jogo, caso ele não atenda às minhas expectativas dentro do prazo permitido.

Critérios de aceitação:
- Validação das condições de elegibilidade (RN-01).
- Campo para motivo do reembolso.
- Crédito automático na carteira virtual após aprovação.

### Criador

**US-11: Cadastrar um jogo**
> Como criador, quero cadastrar um novo jogo na plataforma, para disponibilizá-lo para venda.

Critérios de aceitação:
- Formulário com: título, descrição, gêneros, plataformas suportadas, requisitos de sistema, mídia (screenshots, trailer) e arquivo de instalação.
- Validação de campos obrigatórios e formatos de arquivo.
- Status inicial "Em análise" até aprovação pelo administrador (RN-05).

**US-12: Definir e alterar preço**
> Como criador, quero definir e alterar o preço do meu jogo, para adequá-lo à estratégia comercial.

Critérios de aceitação:
- Campo de preço em BRL com máscara monetária.
- Opção de marcar o jogo como gratuito (preço R$ 0,00).
- Histórico de alterações de preço visível.

**US-13: Visualizar métricas de vendas**
> Como criador, quero visualizar as métricas de vendas dos meus jogos, para acompanhar o desempenho comercial.

Critérios de aceitação:
- Dashboard com: unidades vendidas, receita bruta e receita líquida (após split da plataforma).
- Filtro por jogo e período.
- Exportação de relatório em CSV.

### Administrador

**US-14: Aprovar ou rejeitar jogos**
> Como administrador, quero aprovar ou rejeitar jogos cadastrados por criadores, para garantir a qualidade e conformidade do catálogo.

Critérios de aceitação:
- Fila de jogos com status "Em análise".
- Visualização completa dos dados e mídias do jogo.
- Opção de aprovar, rejeitar (com motivo) ou solicitar ajustes ao criador.

## Entidades Principais

As entidades abaixo servem de referência para os diagramas:

- **User** (id, name, email, password_hash, role, wallet_balance, created_at)
- **Game** (id, title, description, creator_id, price, release_date, status, created_at)
- **Genre** (id, name)
- **GameGenre** (game_id, genre_id)
- **Platform** (id, name)
- **GamePlatform** (game_id, platform_id, download_url, file_size)
- **CartItem** (id, user_id, game_id, added_at)
- **Order** (id, user_id, total, payment_method, status, created_at)
- **OrderItem** (id, order_id, game_id, price_paid)
- **Library** (id, user_id, game_id, acquired_at)
- **Refund** (id, order_item_id, reason, status, created_at)
