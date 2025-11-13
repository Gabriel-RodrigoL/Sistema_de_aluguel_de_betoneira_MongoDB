

<p align="center">
  <img src="./assets/banner.png" alt="Sistema de Aluguer de Betoneiras" height="500">
</p>

# 🧱 Sistema de Aluguer de Betoneiras

Repositório criado para o desenvolvimento do trabalho da disciplina de **Base de Dados** da **FAESA**.
O projeto consiste num **sistema em Python** para gerir o **aluguer de betoneiras**, controlando **clientes**, **equipamentos** e os **respetivos alugueres**.

---

## 💻 Tecnologias Utilizadas

**Linguagem:**

<img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" alt="Python">

**SGBD:**

<img src="https://img.shields.io/badge/MongoDB-Atlas-blue?logo=mongodb&logoColor=white" alt="MongoDB">

**Bibliotecas Python:**

* `pymongo` → Driver de ligação com MongoDB
* `dnspython` → Suporte para conexões mongodb+srv
* `python-dotenv` → Gestão de variáveis de ambiente
* `pandas` → Exibição de relatórios formatados

**Containerização:**

<img src="https://img.shields.io/badge/Docker-Suportado-2496ED?logo=docker&logoColor=white" alt="Docker">

---

## 📂 Estrutura do Projeto

```
Sistema_de_aluguel_de_betoneira/
├── .env                  # Ficheiro local com as credenciais
├── conexion/
│   └── database.py       # Módulo de ligação com MongoDB
├── controller/
│   ├── alugueis_controller.py
│   ├── betoneira_controller.py
│   └── cliente_controller.py
├── diagrams/
│   └── diagrama.mmd
├── pesquisa/
│   └── pesquisa.py       # Módulo para consultas e relatórios
├── model/
│   ├── Alugueis.py
│   ├── Betoneiras.py
│   └── Cliente.py
├── utils/
│   ├── inputs_tratados.py
│   └── menu.py
├── Dockerfile            # Ficheiro para criar a imagem Docker
├── main.py               # Ponto de entrada da aplicação
└── requirements.txt      # Lista de dependências Python
```

---

## 🚀 Começando

### 🧩 Pré-requisitos

* Python **3.9+**
* Git
* Credenciais do MongoDB Atlas
* Docker *(opcional, para execução em container)*

---

### ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/VVagner2077/Sistema_de_aluguel_de_betoneira.git
cd Sistema_de_aluguel_de_betoneira
```

Crie e ative um ambiente virtual:

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Crie um ficheiro `.env` na raiz do projeto:

```properties
MONGODB_URI="mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/<database>"
DB_NAME="aluguel_db"
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rodar a aplicação:

```bash
python main.py
```

---

## 🔌 Estrutura do MongoDB

### Coleções

#### `clientes`
```json
{
  "_id": ObjectId,
  "nome": "string",
  "telefone": "string (único)",
  "cpf": "string (único)"
}
```

#### `betoneiras`
```json
{
  "_id": ObjectId,
  "modelo": "string",
  "valor": "float (valor da diária)",
  "status": "string (disponivel|alugada|manutencao)"
}
```

#### `alugueis`
```json
{
  "_id": ObjectId,
  "id_cliente": "string (referência)",
  "id_betoneira": "string (referência)",
  "data_inicio": "string",
  "data_prevista_termino": "string",
  "data_termino_real": "string (opcional)",
  "status": "string (ativo|finalizado)"
}
```

---

## 🐳 Execução com Docker

**Construir a imagem:**

```bash
docker build -t aluguer-betoneiras .
```

**Executar o container:**

```bash
docker run -it --rm --env-file .env aluguer-betoneiras
```

---

## 📝 Migração (PostgreSQL → MongoDB)

Este projeto foi **migrado de PostgreSQL para MongoDB**:

- ✅ Conexão adaptada para usar PyMongo
- ✅ Controllers refatorados para CRUD em documentos
- ✅ Validações de unicidade usando queries MongoDB
- ✅ IDs agora usam MongoDB `ObjectId`

---

## 👨‍🏫 Orientador

**Professor:** Howard — FAESA

---

## 👥 Autores

* **Gabriel Rodrigo Lapa Rocha**
* **Micael Ribeiro dos Santos**
* **Wagner dos Santos Cristo**

