# Gerenciamento de Eventos

Um projeto em Python para o gerenciamento de eventos, utilizando o framework Django.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework:** Django
- **Banco de Dados:** SQLite

## 📂 Estrutura do Projeto

- `eventos/` - Aplicação principal com funcionalidades de eventos.
- `usuarios/` - Aplicação para gerenciamento de usuários.
- `gerenciamento_eventos/` - Configuração do projeto Django.
- `requirements.txt` - Dependências do projeto.
- Diagrama UML - Representação visual da estrutura do sistema.

## 📋 Pré-requisitos

- Python 3.x instalado.

## ▶️ Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
3. Inicie o servidor local:
   ```bash
   python manage.py runserver
   ```

Acesse [localhost:8000](http://localhost:8000) no navegador.
