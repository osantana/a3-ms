# Vapor — Plataforma de Venda e Distribuição Digital de Jogos

## Tema

Desenvolvimento de uma plataforma web de comércio eletrônico voltada à venda, distribuição e gerenciamento de jogos digitais.

## Descrição do Projeto

O **Vapor** é uma aplicação web que permite a compra, venda e download de jogos digitais. A plataforma conecta duas categorias de usuários: **jogadores**, que navegam por um catálogo, compram títulos e gerenciam sua biblioteca pessoal; e **criadores**, que cadastram, precificam e distribuem seus jogos.

O sistema contempla funcionalidades essenciais de uma loja digital: catálogo com busca e filtros, carrinho de compras, processamento de pagamentos, biblioteca pessoal com histórico de compras e gerenciamento de downloads, além de um sistema de avaliações e um painel administrativo para moderação de conteúdo.

## Análise de Requisitos

### Requisitos Funcionais

**RF-01 — Cadastro de usuário**
> O sistema deve permitir o registro de novos usuários com e-mail, senha e nome de exibição.
>
> Prioridade: Essencial

---

**RF-02 — Autenticação**
> O sistema deve permitir login e logout com credenciais de e-mail e senha.
>
> Prioridade: Essencial

---

**RF-03 — Perfis de acesso**
> O sistema deve distinguir três perfis: Jogador, Criador e Administrador.
>
> Prioridade: Essencial

---

**RF-04 — Catálogo de jogos**
> O sistema deve exibir uma listagem paginada de jogos disponíveis para compra.
>
> Prioridade: Essencial

---

**RF-05 — Busca e filtros**
> O sistema deve permitir busca por nome e filtragem por gênero, preço, plataforma e data de lançamento.
>
> Prioridade: Essencial

---

**RF-06 — Página de detalhes do jogo**
> O sistema deve exibir informações detalhadas de cada jogo: descrição, mídia, requisitos de sistema, preço e avaliações.
>
> Prioridade: Essencial

---

**RF-07 — Carrinho de compras**
> O sistema deve permitir adicionar, remover e visualizar itens em um carrinho antes da compra.
>
> Prioridade: Essencial

---

**RF-08 — Processamento de pagamento**
> O sistema deve processar pagamentos via cartão de crédito, PIX e saldo da carteira virtual.
>
> Prioridade: Essencial

---

**RF-09 — Carteira virtual**
> O sistema deve permitir que o jogador adicione fundos a uma carteira e utilize o saldo em compras.
>
> Prioridade: Importante

---

**RF-10 — Biblioteca pessoal**
> O sistema deve manter uma biblioteca com todos os jogos adquiridos pelo jogador.
>
> Prioridade: Essencial

---

**RF-11 — Download de jogos**
> O sistema deve fornecer links de download para os jogos presentes na biblioteca do jogador.
>
> Prioridade: Essencial

---

**RF-12 — Histórico de compras**
> O sistema deve exibir o histórico completo de transações do jogador, com data, valor e itens.
>
> Prioridade: Importante

---

**RF-13 — Lista de desejos**
> O sistema deve permitir que o jogador adicione jogos a uma lista de desejos para compra futura.
>
> Prioridade: Importante

---

**RF-14 — Avaliações e notas**
> O sistema deve permitir que jogadores que possuem o jogo publiquem uma avaliação com nota e comentário.
>
> Prioridade: Importante

---

**RF-15 — Cadastro de jogos (criador)**
> O sistema deve permitir que criadores cadastrem novos jogos com metadados, mídias e arquivos de instalação.
>
> Prioridade: Essencial

---

**RF-16 — Gerenciamento de preços**
> O sistema deve permitir que criadores definam e alterem o preço de seus jogos, incluindo promoções.
>
> Prioridade: Essencial

---

**RF-17 — Painel de vendas (criador)**
> O sistema deve exibir ao criador métricas de vendas: unidades vendidas, receita e avaliações.
>
> Prioridade: Importante

---

**RF-18 — Promoções e descontos**
> O sistema deve suportar a criação de promoções com percentual de desconto e período de validade.
>
> Prioridade: Importante

---

**RF-19 — Reembolso**
> O sistema deve permitir a solicitação de reembolso dentro de um prazo configurável após a compra.
>
> Prioridade: Desejável

---

**RF-20 — Painel administrativo**
> O sistema deve fornecer ao administrador ferramentas para moderação de jogos, avaliações e usuários.
>
> Prioridade: Essencial

---

**RF-21 — Notificações**
> O sistema deve notificar jogadores sobre promoções em jogos da lista de desejos e status de compras.
>
> Prioridade: Desejável

---

### Requisitos Não Funcionais

**RNF-01 — Responsividade**
> A interface deve ser utilizável em dispositivos com largura mínima de 375px (mobile) até desktop.
>
> Categoria: Usabilidade

---

**RNF-02 — Tempo de resposta**
> As páginas do catálogo devem carregar em no máximo 2 segundos sob carga normal.
>
> Categoria: Desempenho

---

**RNF-03 — Disponibilidade**
> O sistema deve ter disponibilidade mínima de 99% (exceto janelas de manutenção programada).
>
> Categoria: Confiabilidade

---

**RNF-04 — Segurança de senhas**
> Senhas devem ser armazenadas com hash seguro (bcrypt ou argon2) e nunca trafegar em texto plano.
>
> Categoria: Segurança

---

**RNF-05 — HTTPS obrigatório**
> Toda comunicação entre cliente e servidor deve ocorrer via HTTPS/TLS.
>
> Categoria: Segurança

---

**RNF-06 — Proteção contra fraudes**
> O módulo de pagamento deve validar dados e implementar proteção contra ataques de replay e CSRF.
>
> Categoria: Segurança

---

**RNF-07 — Escalabilidade horizontal**
> A arquitetura deve permitir escalar horizontalmente os serviços de catálogo e download de forma independente.
>
> Categoria: Escalabilidade

---

**RNF-08 — Armazenamento de arquivos**
> Arquivos de jogos devem ser armazenados em serviço de object storage com redundância geográfica.
>
> Categoria: Infraestrutura

---

**RNF-09 — Internacionalização**
> O sistema deve suportar pelo menos pt-BR e en-US na interface.
>
> Categoria: Usabilidade

---

**RNF-10 — Acessibilidade**
> A interface deve seguir as diretrizes WCAG 2.1 nível AA.
>
> Categoria: Usabilidade

---

**RNF-11 — Compatibilidade**
> O sistema deve funcionar nos navegadores Chrome, Firefox, Safari e Edge em suas duas últimas versões estáveis.
>
> Categoria: Portabilidade

---

**RNF-12 — LGPD**
> O sistema deve estar em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).
>
> Categoria: Legal

---

### Regras de Negócio

**RN-01 — Avaliação restrita a compradores**
> Um jogador só pode avaliar um jogo que esteja em sua biblioteca.

---

**RN-02 — Avaliação única por jogo**
> Cada jogador pode publicar no máximo uma avaliação por jogo.

---

**RN-03 — Condições de reembolso**
> O reembolso só pode ser solicitado em até 14 dias após a compra e com menos de 2 horas de uso registrado.

---

**RN-04 — Preço mínimo em promoção**
> Promoções não podem resultar em preço final inferior a R$ 0,00. Jogos gratuitos devem ser cadastrados como gratuitos desde a origem.

---

**RN-05 — Split de receita**
> O criador recebe 70% do valor líquido de cada venda; os 30% restantes são retidos pela plataforma.

---

**RN-06 — Aprovação de jogos**
> Jogos cadastrados por criadores ficam com status "Em análise" até aprovação do administrador.

---

**RN-07 — Compra única por título**
> Um jogo já presente na biblioteca do jogador não pode ser comprado novamente.

---

**RN-08 — Reembolso via carteira**
> Reembolsos aprovados devolvem o valor à carteira virtual, não ao meio de pagamento original.

---

## User Stories

### Jogador

**US-01 — Cadastro**
> Como jogador, quero me cadastrar na plataforma com meu e-mail e senha, para ter acesso ao catálogo e poder realizar compras.

Critérios de aceitação:
- Validação de formato de e-mail.
- Senha com no mínimo 8 caracteres, contendo letra e número.
- Confirmação de e-mail via link enviado ao endereço informado.
- Exibição de mensagem de erro caso o e-mail já esteja cadastrado.

---

**US-02 — Login**
> Como jogador, quero fazer login com meu e-mail e senha, para acessar minha conta e biblioteca.

Critérios de aceitação:
- Redirecionamento para a página principal após login bem-sucedido.
- Mensagem de erro genérica para credenciais inválidas (sem revelar se o e-mail existe).
- Bloqueio temporário após 5 tentativas falhas consecutivas.

---

**US-03 — Navegar pelo catálogo**
> Como jogador, quero navegar pelo catálogo de jogos disponíveis, para descobrir novos títulos.

Critérios de aceitação:
- Listagem paginada com 20 jogos por página.
- Exibição de capa, nome, preço e nota média de cada jogo.
- Ordenação por relevância, preço, data de lançamento e avaliação.

---

**US-04 — Buscar e filtrar jogos**
> Como jogador, quero buscar jogos por nome e aplicar filtros, para encontrar rapidamente o que procuro.

Critérios de aceitação:
- Campo de busca com sugestão automática (autocomplete).
- Filtros combinados: gênero, faixa de preço, plataforma (Windows/macOS/Linux).
- Resultados atualizados sem recarregar a página (AJAX/SPA).

---

**US-05 — Visualizar detalhes do jogo**
> Como jogador, quero ver a página de detalhes de um jogo, para decidir se quero comprá-lo.

Critérios de aceitação:
- Exibição de: descrição, screenshots/trailer, gêneros, data de lançamento, criador, requisitos de sistema, preço e avaliações.
- Botão "Adicionar ao Carrinho" visível (ou "Na Biblioteca" se já adquirido).

---

**US-06 — Adicionar ao carrinho**
> Como jogador, quero adicionar jogos ao meu carrinho de compras, para adquirir múltiplos títulos em uma única transação.

Critérios de aceitação:
- Feedback visual ao adicionar item.
- Impedimento de adicionar jogo já presente no carrinho ou na biblioteca.
- Contador de itens visível no ícone do carrinho.

---

**US-07 — Finalizar compra**
> Como jogador, quero finalizar a compra dos jogos no meu carrinho, para adicioná-los à minha biblioteca.

Critérios de aceitação:
- Resumo do pedido com itens, descontos e valor total.
- Seleção de meio de pagamento (cartão, PIX, saldo da carteira).
- Confirmação de compra com número do pedido.
- Jogos adicionados automaticamente à biblioteca após pagamento confirmado.

---

**US-08 — Acessar a biblioteca**
> Como jogador, quero acessar minha biblioteca pessoal, para ver e gerenciar os jogos que possuo.

Critérios de aceitação:
- Listagem de todos os jogos adquiridos com capa e nome.
- Busca e ordenação dentro da biblioteca.
- Botão de download em cada título.

---

**US-09 — Baixar um jogo**
> Como jogador, quero baixar um jogo da minha biblioteca, para instalá-lo no meu computador.

Critérios de aceitação:
- Geração de link de download temporário e seguro (URL assinada com expiração).
- Indicação do tamanho do arquivo antes do download.
- Seleção de plataforma quando o jogo tiver múltiplas versões.

---

**US-10 — Avaliar um jogo**
> Como jogador, quero avaliar um jogo que possuo, para compartilhar minha opinião com outros usuários.

Critérios de aceitação:
- Formulário com nota (1 a 5 estrelas) e campo de comentário.
- Possibilidade de editar ou excluir a avaliação posteriormente.
- Exibição da avaliação na página de detalhes do jogo.

---

**US-11 — Gerenciar lista de desejos**
> Como jogador, quero adicionar e remover jogos da minha lista de desejos, para acompanhar títulos que pretendo comprar futuramente.

Critérios de aceitação:
- Botão de "Adicionar à Lista de Desejos" na página do jogo.
- Página dedicada com todos os itens da lista.
- Indicação visual quando um jogo da lista entra em promoção.

---

**US-12 — Consultar histórico de compras**
> Como jogador, quero consultar meu histórico de compras, para verificar valores pagos e itens adquiridos.

Critérios de aceitação:
- Listagem cronológica de transações com data, itens, valores e status.
- Filtro por período.
- Link para solicitar reembolso (quando elegível conforme RN-03).

---

**US-13 — Solicitar reembolso**
> Como jogador, quero solicitar o reembolso de um jogo, caso ele não atenda às minhas expectativas dentro do prazo permitido.

Critérios de aceitação:
- Validação das condições de elegibilidade (RN-03).
- Campo para motivo do reembolso.
- Crédito automático na carteira virtual após aprovação.

---

### Criador

**US-14 — Cadastrar um jogo**
> Como criador, quero cadastrar um novo jogo na plataforma, para disponibilizá-lo para venda.

Critérios de aceitação:
- Formulário com: título, descrição, gêneros, plataformas suportadas, requisitos de sistema, mídia (screenshots, trailer) e arquivo de instalação.
- Validação de campos obrigatórios e formatos de arquivo.
- Status inicial "Em análise" até aprovação pelo administrador (RN-06).

---

**US-15 — Definir e alterar preço**
> Como criador, quero definir e alterar o preço do meu jogo, para adequá-lo à estratégia comercial.

Critérios de aceitação:
- Campo de preço em BRL com máscara monetária.
- Opção de marcar o jogo como gratuito (preço R$ 0,00).
- Histórico de alterações de preço visível.

---

**US-16 — Criar promoção**
> Como criador, quero criar uma promoção temporária para meu jogo, para atrair mais compradores.

Critérios de aceitação:
- Definição de percentual de desconto e período (data de início e fim).
- Exibição do preço original riscado e preço promocional no catálogo.
- Validação: preço final não pode ser negativo (RN-04).

---

**US-17 — Visualizar métricas de vendas**
> Como criador, quero visualizar as métricas de vendas dos meus jogos, para acompanhar o desempenho comercial.

Critérios de aceitação:
- Dashboard com: unidades vendidas, receita bruta, receita líquida (após split da plataforma), nota média e número de avaliações.
- Filtro por jogo e período.
- Exportação de relatório em CSV.

---

### Administrador

**US-18 — Aprovar ou rejeitar jogos**
> Como administrador, quero aprovar ou rejeitar jogos cadastrados por criadores, para garantir a qualidade e conformidade do catálogo.

Critérios de aceitação:
- Fila de jogos com status "Em análise".
- Visualização completa dos dados e mídias do jogo.
- Opção de aprovar, rejeitar (com motivo) ou solicitar ajustes.

---

**US-19 — Moderar avaliações**
> Como administrador, quero moderar avaliações de jogos, para remover conteúdo inadequado.

Critérios de aceitação:
- Listagem de avaliações denunciadas.
- Opção de ocultar avaliação com registro do motivo.
- Notificação ao autor da avaliação moderada.

---

**US-20 — Gerenciar usuários**
> Como administrador, quero gerenciar contas de usuários, para manter a integridade da plataforma.

Critérios de aceitação:
- Busca de usuários por nome, e-mail ou ID.
- Ações disponíveis: desativar conta, alterar perfil de acesso, resetar senha.
- Log de todas as ações administrativas realizadas.

---

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
- **Review** (id, user_id, game_id, rating, comment, created_at)
- **Wishlist** (id, user_id, game_id, added_at)
- **Promotion** (id, game_id, discount_percent, starts_at, ends_at)
- **Refund** (id, order_item_id, reason, status, created_at)

---

## Espaço Reservado para Diagramas

Os diagramas a seguir serão desenvolvidos utilizando Mermaid:

### Diagrama de Classes
```mermaid
%% TODO: Diagrama de classes baseado nas entidades acima
```

### Diagrama de Casos de Uso
```mermaid
%% TODO: Diagrama de casos de uso por ator
```

### Diagrama de Sequência — Fluxo de Compra
```mermaid
%% TODO: Sequência do fluxo carrinho → pagamento → biblioteca
```

### Diagrama ER
```mermaid
%% TODO: Diagrama entidade-relacionamento
```
