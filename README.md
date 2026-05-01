# Motor Asset Data Pipeline — Sprint 1

> Automação inicial para coleta, registro e atualização de dados de ativos de motores elétricos industriais.

---

## Contexto

Este repositório contém as automações desenvolvidas na **Sprint 1** de uma solução de monitoramento e manutenção preditiva de motores elétricos industriais (WEG W22 Monofásico).

O foco desta sprint é estruturar o fluxo de dados do ativo — desde a ingestão bruta até a persistência histórica — formando a base para o **Digital Twin** e futuras análises inteligentes.

---

## Objetivos da Sprint

- Ingestão automatizada de dados a partir do catálogo técnico do motor (PDF)
- Transformação e normalização dos dados extraídos
- Registro estruturado em base de dados
- Rotina de atualização periódica dos dados operacionais simulados via sensor IoT
- Persistência histórica com rastreabilidade via logs

---

## Estrutura do Projeto

```
sprint-RPA/
├── data/
│   ├── pdf/
│   │   └── sprint_data.pdf       # Catálogo técnico WEG W22
│   └── ativos.json               # Base de dados gerada automaticamente
│
├── src/
│   ├── __init__.py
│   ├── process_pdf.py            # Extração e normalização do PDF
│   ├── database.py               # Persistência em JSON com audit log
│   ├── sensor_simulator.py       # Simulação de leituras IoT
│   ├── scheduler.py              # Rotina de atualização periódica
│   └── logger.py                 # Logging padronizado
│
├── logs/                         # Logs gerados em execução
├── tests/
│   └── test_database.py          # Testes automatizados
├── main.py                       # Ponto de entrada do pipeline
├── Dockerfile                    # Container da solução
├── requirements.txt              # Dependências do projeto
└── README.md
```

---

## Arquitetura da Automação

```
PDF (Catálogo WEG W22)
        │
        ▼
  process_pdf.py
  ├── pdfplumber → extrai tabelas da página 6
  ├── PyMuPDF   → extrai texto corrido de todas as páginas
  └── pandas    → normaliza, limpa e tipifica os dados
        │
        ▼
  database.py
  └── persiste em ativos.json com audit_log
        │
        ├──────────────────────────────┐
        ▼                              ▼
  scheduler.py                  logs/YYYYMMDD.log
  └── APScheduler (10s)         └── rastreabilidade
      └── sensor_simulator.py        de execuções
          └── leituras IoT simuladas
```

### Fluxo de dados

**Entrada → Processamento → Saída**

1. **Entrada:** PDF do catálogo WEG W22 (fonte estática) + leituras simuladas de sensores IoT (fonte dinâmica)
2. **Processamento:** extração de tabelas com `pdfplumber`, normalização de colunas com `pandas`, separação por grupo de polos (II, IV, VI)
3. **Saída:** `ativos.json` com os registros dos motores e `audit_log` de cada operação; arquivo de log diário na pasta `logs/`

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade | Justificativa |
|---|---|---|---|
| `pdfplumber` | 0.11.9 | Extração de tabelas do PDF | Melhor suporte a tabelas com células mescladas vs PyPDF2 |
| `PyMuPDF` | 1.27.2 | Extração de texto corrido | Alta fidelidade na extração de texto por página |
| `pandas` | 3.0.2 | Transformação e normalização | Padrão de mercado para manipulação tabular em Python |
| `APScheduler` | 3.10.4 | Rotina de atualização periódica | Leve, sem dependência de infraestrutura externa (sem Redis, sem Celery) |
| `JSON` | — | Persistência estruturada | Justificativa abaixo |
| `logging` | stdlib | Rastreabilidade das execuções | Nativo do Python, sem dependência adicional |
| `Docker` | — | Execução reprodutível | Elimina divergências de ambiente entre máquinas |
| `pytest` | 8.4.0 | Testes automatizados | Padrão da comunidade Python |

---

## Decisões Técnicas e Justificativas

### Por que JSON e não banco relacional?

O volume de dados desta sprint é pequeno e previsível — aproximadamente 50 registros estáticos do catálogo WEG W22. Não há queries complexas, joins ou concorrência de escrita neste estágio. O JSON oferece portabilidade total (zero dependências externas), é legível sem ferramentas adicionais e facilita o versionamento no GitHub.

**Limitação assumida:** JSON não suporta queries eficientes nem acesso concorrente. Na Sprint 2, quando o scheduler estiver gerando leituras de sensor em volume contínuo, a persistência será migrada para SQLite ou PostgreSQL com SQLAlchemy e Alembic para versionamento de schema.

### Por que o cabeçalho da tabela foi definido manualmente?

O cabeçalho da tabela de dados elétricos no PDF possui estrutura hierárquica de 3 níveis com células mescladas. O `pdfplumber` retorna esse cabeçalho fragmentado em múltiplas linhas com valores `None`. A reconstrução automática introduziria risco de erro nos nomes das colunas, comprometendo a rastreabilidade dos dados de engenharia. A definição manual da constante `COLUNAS` garante consistência e documentação explícita de cada campo.

### Por que APScheduler e não cron?

Cron é dependente do sistema operacional e exige configuração fora do repositório. O APScheduler roda dentro do próprio processo Python, é configurável via código, e funciona identicamente dentro do container Docker sem configuração adicional de SO.

### Por que Docker?

Garante que o pipeline execute de forma idêntica em qualquer máquina — desenvolvimento, CI e eventual ambiente de produção — sem divergências de versão de Python ou bibliotecas. Atende diretamente ao requisito de execução reprodutível da sprint.

---

## Como Executar

### Pré-requisitos

- Python 3.10+ ou Docker Desktop

### Com Docker (recomendado)

```bash
docker build -t sprint-rpa .
docker run sprint-rpa
```

### Localmente

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd sprint-RPA
pip install -r requirements.txt
python main.py
```

### Scheduler (atualização periódica)

```bash
python -m src.scheduler
```

---

## Evidências de Execução

Após rodar `python main.py` ou `docker run sprint-rpa`:

- `data/ativos.json` — base populada com os motores extraídos do PDF e audit_log de cada inserção
- `logs/YYYYMMDD.log` — log com timestamp de cada etapa do pipeline

---

## Status da Sprint

| Requisito | Descrição | Status |
|---|---|---|
| RF01 | Ingestão de dados do PDF | ✅ Concluído |
| RF02 | Transformação e normalização | ✅ Concluído |
| RF03 | Registro em base estruturada (JSON) | ✅ Concluído |
| RF04 | Rotina de atualização periódica | ✅ Concluído |
| RF05 | Persistência histórica com audit log | ✅ Concluído |
| RF06 | Logs de rastreabilidade | ✅ Concluído |
| RNF | Docker — execução reprodutível | ✅ Concluído |
| RNF | Código versionado no GitHub | ⏳ Pendente |
| RNF | Testes automatizados (pytest) | ⏳ Pendente |

---

## Equipe

> Preencher com os nomes do time

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos.