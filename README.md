# WhatsApp Sender

Aplicacao desktop para envio de mensagens em massa via WhatsApp Web com interface grafica moderna.

## Indice

- [Recursos](#recursos)
- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)
- [Variaveis de Template](#variaveis-de-template)
- [Formato da Planilha](#formato-da-planilha)
- [Configuracoes](#configuracoes)
- [Solucao de Problemas](#solucao-de-problemas)
- [Licenca](#licenca)

## Recursos

- Interface grafica moderna com CustomTkinter
- Suporte a planilhas Excel (.xlsx, .xls) e CSV
- Envio de mensagens de texto personalizadas
- Envio de imagens (opcional)
- Variaveis curinga para personalizacao
- Preview da mensagem antes do envio
- Barra de progresso em tempo real
- Log detalhado de envios
- Estatisticas de envio (enviados, falhas, pulados)
- Deteccao automatica de numeros sem WhatsApp
- Validacao de telefones brasileiros
- Pausas automaticas para evitar bloqueio
- Sessao persistente (login unico)

## Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conexao com internet
- Conta no WhatsApp

## Instalacao

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/whatsapp-sender.git
cd whatsapp-sender


Thought for 1sVou criar o README.md completo para o projeto:

```markdown
# WhatsApp Sender

Aplicacao desktop para envio de mensagens em massa via WhatsApp Web com interface grafica moderna.

## Indice

- [Recursos](#recursos)
- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)
- [Variaveis de Template](#variaveis-de-template)
- [Formato da Planilha](#formato-da-planilha)
- [Configuracoes](#configuracoes)
- [Solucao de Problemas](#solucao-de-problemas)
- [Licenca](#licenca)

## Recursos

- Interface grafica moderna com CustomTkinter
- Suporte a planilhas Excel (.xlsx, .xls) e CSV
- Envio de mensagens de texto personalizadas
- Envio de imagens (opcional)
- Variaveis curinga para personalizacao
- Preview da mensagem antes do envio
- Barra de progresso em tempo real
- Log detalhado de envios
- Estatisticas de envio (enviados, falhas, pulados)
- Deteccao automatica de numeros sem WhatsApp
- Validacao de telefones brasileiros
- Pausas automaticas para evitar bloqueio
- Sessao persistente (login unico)

## Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conexao com internet
- Conta no WhatsApp

## Instalacao

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/whatsapp-sender.git
cd whatsapp-sender
```

### 2. Crie um ambiente virtual (recomendado)

```shellscript
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependencias

```shellscript
pip install -r requirements.txt
```

### 4. Execute a aplicacao

```shellscript
python main.py
```

## Estrutura do Projeto

```plaintext
whatsapp_sender/
├── main.py                     # Ponto de entrada
├── requirements.txt            # Dependencias
├── README.md                   # Documentacao
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuracoes centralizadas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── contact.py          # Modelo de contato
│   │   └── message.py          # Modelo de mensagem/template
│   ├── services/
│   │   ├── __init__.py
│   │   ├── spreadsheet_service.py  # Leitura de planilhas
│   │   ├── phone_service.py        # Validacao de telefones
│   │   └── whatsapp_service.py     # Envio via WhatsApp Web
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py              # Janela principal
│   │   ├── styles.py           # Estilos e cores
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── file_selector.py    # Seletor de arquivos
│   │       ├── message_editor.py   # Editor de mensagem
│   │       ├── preview_panel.py    # Preview da mensagem
│   │       ├── progress_panel.py   # Progresso e logs
│   │       └── control_panel.py    # Botoes de controle
│   └── utils/
│       └── __init__.py
├── uploads/                    # Planilhas enviadas
├── images/                     # Imagens para envio
├── logs/                       # Logs de execucao
└── chrome_profile/             # Perfil do Chrome (sessao)
```

## Como Usar

### Passo 1: Prepare sua planilha

Crie uma planilha com pelo menos duas colunas:

- **nome_completo** (ou: nome, name)
- **telefone** (ou: phone, celular, whatsapp)


### Passo 2: Abra a aplicacao

```shellscript
python main.py
```

### Passo 3: Carregue a planilha

Clique em "Selecionar" na secao "Planilha de Contatos" e escolha seu arquivo.

### Passo 4: Adicione uma imagem (opcional)

Se desejar enviar uma imagem junto com a mensagem, selecione-a na secao "Imagem".

### Passo 5: Escreva sua mensagem

Use o editor de mensagem e insira variaveis clicando nos botoes disponíveis.

Exemplo:

```plaintext
Ola {primeiro_nome}!

Tudo bem com voce?

Estamos entrando em contato para informar sobre nossa promocao especial.

Atenciosamente,
Equipe de Vendas
```

### Passo 6: Verifique o preview

Confira como a mensagem ficara para o primeiro contato.

### Passo 7: Inicie o envio

Clique em "Iniciar Envio". O navegador sera aberto automaticamente.

### Passo 8: Faca login no WhatsApp Web

Na primeira execucao, escaneie o QR Code com seu celular. Nas proximas vezes, o login sera automatico.

### Passo 9: Acompanhe o progresso

Monitore o envio pelo painel de progresso e log.

## Variaveis de Template

Use estas variaveis no texto da mensagem para personalizacao:

| Variavel | Descricao | Exemplo
|-----|-----|-----
| `{primeiro_nome}` | Primeiro nome do contato | Joao
| `{nome_completo}` | Nome completo | Joao Silva
| `{ultimo_nome}` | Ultimo nome | Silva
| `{telefone}` | Numero de telefone | 5511999998888


### Exemplo de uso

**Template:**

```plaintext
Ola {primeiro_nome}!

Seu cadastro com o nome {nome_completo} foi confirmado.

Obrigado!
```

**Resultado para "Joao Silva":**

```plaintext
Ola Joao!

Seu cadastro com o nome Joao Silva foi confirmado.

Obrigado!
```

## Formato da Planilha

### Colunas aceitas

A aplicacao reconhece automaticamente as seguintes colunas:

**Para nome:**

- nome_completo
- nome
- name
- full_name


**Para telefone:**

- telefone
- phone
- celular
- whatsapp
- tel


### Formato do telefone

Os seguintes formatos sao aceitos:

| Formato | Exemplo
|-----|-----|-----
| Somente numeros | 11999998888
| Com codigo do pais | 5511999998888
| Com zero inicial | 011999998888
| Com formatacao | (11) 99999-8888


A aplicacao normaliza automaticamente para o formato internacional.

### Exemplo de planilha

| nome_completo | telefone
|-----|-----|-----
| Joao Silva | 11999998888
| Maria Santos | 21988887777
| Pedro Oliveira | (31) 99999-6666


## Configuracoes

As configuracoes podem ser ajustadas no arquivo `src/config.py`:

```python
@dataclass
class AppConfig:
    # Tempos entre mensagens (segundos)
    MIN_DELAY: int = 5      # Minimo
    MAX_DELAY: int = 12     # Maximo
    
    # Timeouts
    PAGE_TIMEOUT: int = 15      # Carregar pagina
    MESSAGE_TIMEOUT: int = 10   # Enviar mensagem
    
    # Pausas automaticas
    PAUSE_AFTER: int = 50       # Pausar apos X mensagens
    PAUSE_DURATION: int = 60    # Duracao da pausa (segundos)
```

### Ajustes recomendados

| Cenario | MIN_DELAY | MAX_DELAY | PAUSE_AFTER
|-----|-----|-----
| Conservador | 30 | 60 | 20
| Moderado | 10 | 25 | 30
| Rapido | 5 | 12 | 50


## Solucao de Problemas

### Erro: "Navegador nao inicializa"

**Causa:** Chrome nao instalado ou versao incompativel.

**Solucao:**

1. Instale ou atualize o Google Chrome
2. Delete a pasta `chrome_profile` e tente novamente


### Erro: "Timeout no login"

**Causa:** QR Code nao escaneado a tempo.

**Solucao:**

1. Aumente o timeout em `whatsapp_service.py` (linha do `login`)
2. Escaneie o QR Code mais rapidamente


### Erro: "Colunas nao encontradas"

**Causa:** Nomes das colunas nao reconhecidos.

**Solucao:**

1. Renomeie as colunas para `nome_completo` e `telefone`
2. Ou use um dos nomes aceitos listados acima


### Muitos contatos "Sem WhatsApp"

**Causa:** Numeros incorretos ou sem WhatsApp.

**Solucao:**

1. Verifique se os numeros estao corretos
2. Confirme que os numeros possuem WhatsApp ativo
3. Verifique se o DDD esta correto


### Mensagens nao estao sendo enviadas

**Causa:** WhatsApp Web deslogou ou conexao instavel.

**Solucao:**

1. Verifique sua conexao com a internet
2. Delete a pasta `chrome_profile` e faca login novamente
3. Verifique se seu WhatsApp no celular esta funcionando


### Navegador fecha sozinho

**Causa:** Erro no driver ou memoria insuficiente.

**Solucao:**

1. Feche outros programas para liberar memoria
2. Atualize o Chrome para a versao mais recente
3. Reinicie o computador


## Avisos Importantes

1. **Use com responsabilidade:** O envio de mensagens em massa pode violar os Termos de Servico do WhatsApp.
2. **Evite spam:** Envie apenas para contatos que consentiram em receber suas mensagens.
3. **Limites:** O WhatsApp pode bloquear temporariamente contas que enviam muitas mensagens em pouco tempo.
4. **Backup:** Faca backup dos seus contatos do WhatsApp antes de usar.
5. **Teste:** Sempre teste com poucos contatos antes de enviar para listas grandes.


## Dependencias

| Pacote | Versao | Descricao
|-----|-----|-----
| customtkinter | 5.2.1 | Interface grafica moderna
| pandas | 2.1.4 | Manipulacao de dados
| openpyxl | 3.1.2 | Leitura de arquivos .xlsx
| xlrd | 2.0.1 | Leitura de arquivos .xls
| selenium | 4.17.2 | Automacao do navegador
| webdriver-manager | 4.0.1 | Gerenciamento do ChromeDriver
| Pillow | 10.2.0 | Manipulacao de imagens


## Contribuicao

Contribuicoes sao bem-vindas! Para contribuir:

1. Faca um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudancas (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


## Licenca

Este projeto esta sob a licenca MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Desenvolvido com Python e CustomTkinter.

---

**Aviso Legal:** Este software e fornecido "como esta", sem garantias de qualquer tipo. O uso e de responsabilidade do usuario. O autor nao se responsabiliza por bloqueios de conta ou qualquer outro problema decorrente do uso deste software.

```plaintext

---

O README inclui todas as informacoes necessarias para instalar, configurar e usar a aplicaca
```