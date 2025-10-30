# Deploy na Shard Cloud

## 🚀 Deploy na Shard Cloud

A Shard Cloud oferece hospedagem moderna e confiável para seus projetos Python. Siga este guia para fazer deploy da sua API em minutos.

### 📋 Pré-requisitos

- Conta na [Shard Cloud](https://shardcloud.app)
- Projeto funcionando localmente
- Arquivo `.shardcloud` configurado
- Banco PostgreSQL (pode usar o da Shard Cloud)

## 🔧 Configuração do projeto

### 1. Criar arquivo `.shardcloud`

Crie um arquivo `.shardcloud` na raiz do projeto:

```bash
DISPLAY_NAME=Notes API
ENTRYPOINT=src/main.py
MEMORY=1024
VERSION=recommended
SUBDOMAIN=notes-api
START=pip install -r requirements.txt && python src/main.py
DESCRIPTION=API REST para gerenciamento de notas com FastAPI e PostgreSQL
```

### 2. Configurar variáveis de ambiente

Configure as variáveis no dashboard da Shard Cloud:

```env
# Database - REQUIRED
DATABASE=postgres://user:password@host:port/database?ssl=true

# Server - REQUIRED
PORT=80
HOST=0.0.0.0

# Security - REQUIRED
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Environment - REQUIRED
ENVIRONMENT=production
DEBUG=false
```

## 📦 Preparação para deploy

### 1. Testar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Testar aplicação
python src/main.py
```

### 2. Verificar funcionamento

```bash
# Testar health endpoint
curl http://localhost/health

# Testar API
curl http://localhost/docs
```

## 🚀 Deploy na Shard Cloud

### Método 1: Upload direto (Recomendado)

1. **Acesse o Dashboard**
   - Vá para [Shard Cloud Dashboard](https://shardcloud.app/dash)
   - Faça login na sua conta

2. **Criar nova aplicação**
   - Clique em **"New app"**
   - Selecione **"Upload"**

3. **Preparar arquivos**
   - Zip toda a pasta do projeto (incluindo `.shardcloud`)
   - Certifique-se de que o `requirements.txt` está incluído

4. **Upload e deploy**
   - Arraste o arquivo ZIP ou clique para selecionar
   - Aguarde o processamento (alguns minutos)
   - Sua aplicação estará disponível em `https://notes-api.shardweb.app`

### Método 2: Deploy via Git

1. **Conectar repositório**
   - No dashboard, clique em **"New app"**
   - Selecione **"Git Repository"**
   - Conecte seu repositório GitHub/GitLab

2. **Configurar build**
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python src/main.py`
   - **Python version:** `3.11` (recomendado)

3. **Deploy automático**
   - Cada push na branch principal fará deploy automático
   - Configure webhooks se necessário

## 🗄️ Banco de dados

### Usar PostgreSQL da Shard Cloud

1. **Criar banco**
   - Vá para [Databases Dashboard](https://shardcloud.app/dash/databases)
   - Clique em **"New Database"**
   - Selecione **PostgreSQL**
   - Escolha a quantidade de RAM

2. **Configurar conexão**
   - Copie a string de conexão do dashboard
   - Configure como variável `DATABASE` na aplicação
   - Exemplo: `postgres://user:pass@host:port/db?ssl=true`

3. **Executar migrações**
   - As migrações Alembic são executadas automaticamente na inicialização
   - Verifique logs para confirmar sucesso

### Banco externo

Se preferir usar banco externo:

```env
DATABASE=postgres://user:password@external-host:5432/database?ssl=true
```

## 🌐 Configurações avançadas

### Subdomínio personalizado

No arquivo `.shardcloud`:

```bash
SUBDOMAIN=minha-api
```

Sua aplicação ficará disponível em: `https://minha-api.shardweb.app`

### Domínio personalizado

1. **Configurar DNS**
   - Adicione um registro CNAME apontando para `notes-api.shardweb.app`
   - Ou configure A record com o IP fornecido

2. **Ativar no dashboard**
   - Vá para configurações da aplicação
   - Adicione seu domínio personalizado
   - Configure certificado SSL (automático)

### Variáveis de ambiente

Configure variáveis sensíveis no dashboard:

1. Acesse configurações da aplicação
2. Vá para **"Environment Variables"**
3. Adicione suas variáveis:
   ```
   DATABASE=postgres://user:pass@host:port/db?ssl=true
   SECRET_KEY=sua-chave-secreta-super-segura
   ENVIRONMENT=production
   DEBUG=false
   ```

## 🔍 Monitoramento e logs

### Logs da aplicação

- Acesse o dashboard da aplicação
- Vá para a aba **"Logs"**
- Monitore erros e performance em tempo real

### Métricas

- **Uptime:** Monitoramento automático
- **Performance:** Métricas de resposta
- **Tráfego:** Estatísticas de acesso
- **Database:** Monitoramento de conexões

### Health checks

A aplicação inclui endpoints de monitoramento:

- `GET /health` - Status geral da API
- `GET /docs` - Documentação Swagger
- `GET /redoc` - Documentação ReDoc

## 🔒 Segurança

### HTTPS automático

- Todos os deploys na Shard Cloud incluem HTTPS automático
- Certificados SSL gerenciados automaticamente
- Renovação automática

### Autenticação JWT

A aplicação usa JWT com hash PBKDF2:

- Tokens expiram em 24 horas por padrão
- Senhas são hashadas com PBKDF2 + salt
- Headers de segurança configurados automaticamente

## 🚦 CI/CD com GitHub Actions

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Shard Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Deploy to Shard Cloud
        run: |
          # Zip project
          zip -r deploy.zip . -x "*.git*" "__pycache__/*" "*.pyc"
          
          # Upload to Shard Cloud (configure API token)
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.SHARD_TOKEN }}" \
            -F "file=@deploy.zip" \
            https://api.shardcloud.app/deploy
```

## 🐛 Troubleshooting

### Build falha

```bash
# Limpar cache pip
pip cache purge

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar dependências
pip check
```

### Aplicação não inicia

1. Verifique logs no dashboard
2. Confirme se `ENTRYPOINT` está correto
3. Teste localmente com `python src/main.py`

### Erro de conexão com banco

1. Verifique string de conexão `DATABASE`
2. Confirme se banco está acessível
3. Teste conexão localmente

### Erro de módulo não encontrado

- Confirme se todas as dependências estão no `requirements.txt`
- Verifique se imports estão corretos
- Teste localmente primeiro

## ✅ Checklist de deploy

- [ ] Arquivo `.shardcloud` configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Testado localmente (`python src/main.py`)
- [ ] Banco PostgreSQL configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Projeto zipado ou conectado ao Git
- [ ] Deploy realizado no dashboard
- [ ] Aplicação acessível via URL
- [ ] Health endpoint funcionando (`/health`)
- [ ] API endpoints testados (`/docs`)
- [ ] HTTPS ativo
- [ ] Logs monitorados

## 🎉 Sucesso!

Sua API está no ar na Shard Cloud! 

### Próximos passos:

1. **Teste completo:** Verifique todos os endpoints
2. **Documentação:** Acesse `/docs` para Swagger UI
3. **Autenticação:** Teste registro e login de usuários
4. **Monitoramento:** Configure alertas de uptime
5. **Backup:** Configure backup do banco de dados
6. **Otimização:** Monitore métricas e otimize performance

### URLs importantes:

- **Dashboard:** https://shardcloud.app/dash
- **Documentação:** https://docs.shardcloud.app/quickstart
- **Suporte:** https://shardcloud.app/support

---

**Precisa de ajuda?** Consulte a [documentação oficial da Shard Cloud](https://docs.shardcloud.app/quickstart) ou entre em contato com o suporte.