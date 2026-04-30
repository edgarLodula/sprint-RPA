# 🔧 Motor Asset Data Pipeline — Sprint 1

> Automação inicial para coleta, registro e atualização de dados de ativos de motores elétricos industriais.

---

## 📋 Contexto

Este repositório contém as automações desenvolvidas na **Sprint 1** de uma solução de monitoramento e manutenção preditiva de motores elétricos industriais (WEG W22 Monofásico).

O foco desta sprint é estruturar o fluxo de dados do ativo — desde a ingestão bruta até a persistência histórica — formando a base para o **Digital Twin** e futuras análises inteligentes.

---

## 🎯 Objetivos da Sprint

- Ingestão automatizada de dados a partir do catálogo técnico do motor (PDF)
- Transformação e normalização dos dados extraídos
- Registro estruturado em base de dados
- Rotina de atualização periódica dos dados operacionais
- Persistência histórica com rastreabilidade via logs

---

## 🗂️ Estrutura do Projeto

```
├── data/
│   ├── pdf/                  # Fonte de dados — catálogo técnico WEG W22
│   ├── raw/                  # Dados brutos extraídos
│   └── processed/            # Dados normalizados prontos para carga
│
├── src/
│   ├── ingestion/            # Requisito 1 — leitura e extração do PDF
│   ├── transformation/       # Requisito 2 — limpeza e normalização
│   ├── storage/              # Requisito 3 — persistência estruturada
│   ├── update/               # Requisito 4 — rotina de atualização
│   └── logs/                 # Requisito 6 — rastreabilidade das execuções
│
├── docs/
│   └── arquitetura.md        # Documento técnico da solução
│
├── tests/                    # Testes das automações
├── requirements.txt          # Dependências do projeto
├── docker-compose.yml        # Container da solução
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade | Documentação |
|---|---|---|
| `pdfplumber` | Extração de tabelas do PDF | https://github.com/jsvine/pdfplumber |
| `PyMuPDF` | Extração de texto corrido do PDF | https://pymupdf.readthedocs.io/en/latest/ |
| `pandas` | Transformação e normalização dos dados | https://pandas.pydata.org/docs/ |
| `re` | Limpeza de strings e caracteres especiais | https://docs.python.org/3/library/re.html |
| `unidecode` | Normalização de caracteres acentuados | https://pypi.org/project/Unidecode/ |

---

## ⚙️ Como Executar

### Pré-requisitos

- Python 3.10+
- Docker (recomendado)

### Instalação local

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
pip install -r requirements.txt
```

### Com Docker

```bash
docker-compose up --build
```

---

## 📦 Fonte de Dados

O catálogo técnico utilizado é o **WEG W22 Motor Elétrico Monofásico** — Catálogo Comercial Mercado Brasileiro.

O PDF contém:
- Dados elétricos: potência, corrente, rendimento, fator de potência, RPM
- Dados mecânicos: dimensões, rolamentos, flanges
- Segmentação por número de polos: II, IV e VI polos

> **Decisão técnica:** o cabeçalho da tabela de dados elétricos foi definido manualmente devido à estrutura hierárquica de 3 níveis com células mescladas no PDF original. A reconstrução automática introduziria risco de erro nos nomes das colunas, comprometendo a rastreabilidade dos dados de engenharia.

---

## 📊 Status da Sprint

| Requisito | Descrição | Status |
|---|---|---|
| RF01 | Ingestão de dados do PDF | 🔄 Em andamento |
| RF02 | Transformação e normalização | 🔄 Em andamento |
| RF03 | Registro em base estruturada | ⏳ Pendente |
| RF04 | Rotina de atualização | ⏳ Pendente |
| RF05 | Persistência histórica | ⏳ Pendente |
| RF06 | Logs de rastreabilidade | ⏳ Pendente |

---

## 👥 Equipe

> Preencher com os nomes do time

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e internos da empresa.
