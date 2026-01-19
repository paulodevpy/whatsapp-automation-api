# 🚀 WhatsApp Sender Pro

Aplicação desktop para envio de mensagens em massa via WhatsApp Web com interface gráfica moderna e inteligente.

**Desenvolvido com ❤️ por [@paulodevpy](https://github.com/paulodevpy) - paulodevpy@gmail.com**

## Índice

- [Recursos](#recursos)
- [Capturas de Tela](#capturas-de-tela)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Usar](#como-usar)
- [Variáveis de Template](#variáveis-de-template)
- [Formato da Planilha](#formato-da-planilha)
- [Configurações](#configurações)
- [Solução de Problemas](#solução-de-problemas)
- [Licença](#licença)

## Recursos

### 🎨 Interface Moderna e Branding
- **Design elegante** com tema dark profissional
- **Painel de branding** com arte ASCII personalizada
- **Identidade visual** clara do desenvolvedor
- **Botão "Sobre"** facilmente acessível
- **Ícones e elementos visuais** customizados

### 📊 Gerenciamento de Dados
- Suporte a planilhas Excel (.xlsx, .xls) e CSV
- **Detecção automática de colunas** e criação dinâmica de variáveis
- Validação automática de telefones brasileiros
- Formatação inteligente de números

### 💬 Personalização Avançada
- **Variáveis dinâmicas** baseadas nas colunas da planilha
- **Variáveis padrão**: data atual, hora atual, saudação automática
- **Derivação inteligente** de primeiro nome e sobrenome
- Preview em tempo real da mensagem

### 🤖 Automação Inteligente
- **Gerenciamento automático do ChromeDriver**
- Detecção automática de números sem WhatsApp
- **Esperas inteligentes** com condições dinâmicas para conexões lentas
- Pausas automáticas para evitar bloqueio
- Sessão persistente (login único)

### 📈 Monitoramento
- Barra de progresso em tempo real
- Log detalhado de todos os envios
- Estatísticas completas (enviados, falhas, pulados)
- Relatórios de performance

### 🖼️ Mídias
- Envio de imagens (opcional)
- Upload automático e otimizado
- Suporte a múltiplos formatos

## 🆕 Últimas Melhorias (v1.0.0)

### ✨ Branding e Identidade Visual
- **Painel de branding personalizado** com arte ASCII exclusiva
- **Identidade visual profissional** com cores temáticas
- **Créditos do desenvolvedor** sempre visíveis na interface
- **Botão "Sobre" integrado** para informações completas
- **Ícones customizados** e elementos visuais únicos

### 🎨 Interface Aprimorada
- **Design moderno** com tema dark elegante
- **Paleta de cores expandida** com accents azul, roxo e rosa
- **Elementos visuais** com gradientes e efeitos
- **Layout responsivo** otimizado para diferentes telas
- **Experiência do usuário** refinada e intuitiva

### 👨‍💻 Autoria Clara
- **Nome profissional:** WhatsApp Sender Pro
- **Desenvolvedor:** Paulo Dev (@paulodevpy)
- **Contato direto:** paulodevpy@gmail.com
- **Links sociais** integrados na aplicação
- **Informações de versão** e data de lançamento

## Capturas de Tela

### Tela Principal com Branding
![Tela Principal](screenshots/main_screen.png)
*Tela principal mostrando a interface moderna com painel de branding personalizado e arte ASCII do desenvolvedor.*

### Editor de Mensagens com Variáveis
![Editor de Mensagens](screenshots/message_editor.png)
*Editor mostrando as variáveis dinâmicas geradas automaticamente da planilha.*

### Preview da Mensagem
![Preview](screenshots/preview.png)
*Preview em tempo real mostrando como a mensagem ficará para o contato.*

### Painel de Progresso
![Progresso](screenshots/progress.png)
*Monitoramento em tempo real do envio com logs detalhados.*

## Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conexão com internet
- Conta no WhatsApp

## Instalação

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

### 3. Instale as dependências

```shellscript
pip install -r requirements.txt
```

### 4. Execute a aplicação

```shellscript
python main.py
```

## 📦 Distribuição (Executável)

Para usuários que não querem instalar Python, foi gerado um executável standalone:

### Como Obter o Executável

1. Execute o comando de build:
```shellscript
pip install pyinstaller
pyinstaller --onefile --windowed --name="WhatsApp_Sender" --hidden-import=selenium --hidden-import=webdriver_manager --hidden-import=customtkinter main.py
```

2. O executável será criado em `dist/WhatsApp_Sender.exe`

### Usando o Executável

- **Arquivo:** `WhatsApp_Sender.exe`
- **Requisitos:** Apenas Google Chrome instalado
- **Instruções:** Consulte o arquivo `INSTRUCOES.txt` na pasta `dist/`

### Conteúdo da Distribuição

```
dist/
├── WhatsApp_Sender.exe    # Executável principal (~52MB)
├── INSTRUCOES.txt         # Instruções de uso
└── [pastas de dados]      # uploads/, images/, logs/
```

### Script de Build

Para facilitar futuras gerações do executável, execute:
```shellscript
./build_exe.bat
```

## Estrutura do Projeto

```
whatsapp_sender/
├── main.py                     # Ponto de entrada
├── requirements.txt            # Dependências
├── README.md                   # Documentação
├── .gitignore                  # Arquivos ignorados pelo Git
├── screenshots/                # Capturas de tela
├── src/
│   ├── __init__.py
│   ├── config.py               # Configurações centralizadas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── contact.py          # Modelo de contato
│   │   └── message.py          # Modelo de mensagem/template
│   ├── services/
│   │   ├── __init__.py
│   │   ├── spreadsheet_service.py  # Leitura de planilhas
│   │   ├── phone_service.py        # Validação de telefones
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
│   │       └── control_panel.py    # Botões de controle
│   └── utils/
│       └── __init__.py
├── uploads/                    # Planilhas enviadas
├── images/                     # Imagens para envio
├── logs/                       # Logs de execução
└── chrome_profile/             # Perfil do Chrome (sessão)
```

## Como Usar

### Passo 1: Prepare sua planilha

Crie uma planilha com pelo menos duas colunas. A aplicação detecta automaticamente os nomes das colunas.

### Passo 2: Abra a aplicação

```shellscript
python main.py
```

### Passo 3: Carregue a planilha

Clique em "Selecionar" na seção "Planilha de Contatos" e escolha seu arquivo. As variáveis serão geradas automaticamente.

### Passo 4: Adicione uma imagem (opcional)

Se desejar enviar uma imagem junto, selecione-a na seção "Imagem".

### Passo 5: Escreva sua mensagem

Use o editor de mensagem e insira variáveis clicando nos botões disponíveis. As variáveis são criadas dinamicamente baseadas na planilha.

### Passo 6: Verifique o preview

Confira como a mensagem ficará para o primeiro contato.

### Passo 7: Inicie o envio

Clique em "Iniciar Envio". O navegador abrirá automaticamente com o ChromeDriver gerenciado.

### Passo 8: Faça login no WhatsApp Web

Na primeira execução, escaneie o QR Code. Nas próximas vezes, o login será automático.

### Passo 9: Acompanhe o progresso

Monitore o envio pelo painel de progresso e logs em tempo real.

## Variáveis de Template

### Variáveis Dinâmicas (baseadas na planilha)

A aplicação lê automaticamente as colunas da planilha e cria variáveis correspondentes:

| Exemplo de Coluna | Variável Gerada | Descrição |
|-------------------|-----------------|-----------|
| nome_completo | `{nome_completo}` | Nome completo |
| email | `{email}` | Email do contato |
| cidade | `{cidade}` | Cidade |
| idade | `{idade}` | Qualquer coluna personalizada |

### Variáveis Derivadas

Quando há uma coluna de nome, variáveis extras são criadas automaticamente:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{primeiro_nome}` | Primeiro nome | João |
| `{ultimo_nome}` | Último nome | Silva |

### Variáveis Padrão

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{data_atual}` | Data atual | 19/01/2026 |
| `{hora_atual}` | Hora atual | 14:30 |
| `{saudacao}` | Saudação automática | Bom dia / Boa tarde / Boa noite |

### Exemplo Completo

**Planilha:**
| nome_completo | email | cidade |
|---------------|-------|--------|
| João Silva | joao@email.com | São Paulo |

**Mensagem:**
```
{saudacao} {primeiro_nome}!

Obrigado por se cadastrar em {cidade}.

Seu email {email} foi confirmado.

Enviado em {data_atual} às {hora_atual}.
```

**Resultado:**
```
Bom dia João!

Obrigado por se cadastrar em São Paulo.

Seu email joao@email.com foi confirmado.

Enviado em 19/01/2026 às 14:30.
```

## Formato da Planilha

### Colunas Reconhecidas Automaticamente

**Para nome:**
- nome_completo, nome, name, full_name

**Para telefone:**
- telefone, phone, celular, whatsapp, tel

**Outras colunas:** Qualquer nome será automaticamente uma variável.

### Formato do Telefone

| Formato | Exemplo |
|---------|---------|
| Apenas números | 11999998888 |
| Com código do país | 5511999998888 |
| Com zero | 011999998888 |
| Formatado | (11) 99999-8888 |

### Exemplo de Planilha

| nome_completo | telefone | email | cidade | empresa |
|---------------|----------|-------|--------|---------|
| João Silva | 11999998888 | joao@email.com | São Paulo | ABC Ltda |
| Maria Santos | 21988887777 | maria@email.com | Rio | XYZ Corp |

## Configurações

As configurações podem ser ajustadas em `src/config.py`:

```python
@dataclass
class AppConfig:
    # Tempos entre mensagens (segundos)
    MIN_DELAY: int = 5      # Mínimo
    MAX_DELAY: int = 12     # Máximo

    # Timeouts
    PAGE_TIMEOUT: int = 15      # Carregar página
    MESSAGE_TIMEOUT: int = 20   # Enviar mensagem

    # Pausas automáticas
    PAUSE_AFTER: int = 50       # Pausar após X mensagens
    PAUSE_DURATION: int = 60    # Duração da pausa
```

### Ajustes Recomendados

| Cenário | MIN_DELAY | MAX_DELAY | PAUSE_AFTER |
|---------|-----------|-----------|-------------|
| Conservador | 30 | 60 | 20 |
| Moderado | 10 | 25 | 30 |
| Rápido | 5 | 12 | 50 |

## Solução de Problemas

### Erro: "Navegador não inicializa"
**Causa:** Chrome não instalado ou versão incompatível.

**Solução:**
1. Instale ou atualize o Google Chrome
2. Delete a pasta `chrome_profile`
3. O ChromeDriver será baixado automaticamente

### Erro: "Timeout aguardando caixa de mensagem"
**Causa:** Conexão lenta ou página não carregou.

**Solução:**
1. Verifique sua conexão com a internet
2. Aguarde mais tempo (timeouts aumentados automaticamente)
3. Tente novamente

### Erro: "Colunas não encontradas"
**Causa:** Nomes das colunas não reconhecidos.

**Solução:**
1. Use nomes descritivos para as colunas
2. A aplicação detecta automaticamente qualquer coluna

### Muitos contatos "Sem WhatsApp"
**Causa:** Números incorretos ou sem WhatsApp.

**Solução:**
1. Verifique se os números estão corretos
2. Confirme que possuem WhatsApp ativo
3. Verifique o DDD

### Mensagens não estão sendo enviadas
**Causa:** WhatsApp Web deslogou ou conexão instável.

**Solução:**
1. Delete a pasta `chrome_profile` e faça login novamente
2. Verifique se o WhatsApp no celular está funcionando

## Avisos Importantes

1. **Use com responsabilidade:** Evite spam e respeite os Termos do WhatsApp
2. **Limites:** O WhatsApp pode bloquear contas com envios excessivos
3. **Backup:** Faça backup dos seus contatos
4. **Teste:** Sempre teste com poucos contatos primeiro

## Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| customtkinter | 5.2.1 | Interface gráfica moderna |
| pandas | 2.1.4 | Manipulação de dados |
| selenium | 4.17.2 | Automação do navegador |
| webdriver-manager | 4.0.1 | Gerenciamento do ChromeDriver |
| Pillow | 10.2.0 | Manipulação de imagens |

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

**👨‍💻 Paulo Dev**
- **GitHub:** [@paulodevpy](https://github.com/paulodevpy)
- **Email:** paulodevpy@gmail.com
- **LinkedIn:** [Paulo Developer](https://linkedin.com/in/paulodevpy)

*Desenvolvido com ❤️ usando Python, CustomTkinter e Selenium WebDriver*

---

**Aviso Legal:** Este software é fornecido "como está", sem garantias. O uso é de responsabilidade do usuário.
```