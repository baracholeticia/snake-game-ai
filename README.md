# SNAKE AI

<div align="center">
  
  <p>
    Projeto desenvolvido para a disciplina de <b>Inteligência Artificial</b> do curso de Ciência da Computação da 
    <b>Universidade Federal do Agreste de Pernambuco (UFAPE)</b>.
  </p>

  ![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
  ![Next.js](https://img.shields.io/badge/next.js-%23000000.svg?style=for-the-badge&logo=next.js&logoColor=white)
  ![TypeScript](https://img.shields.io/badge/typescript-%233178C6.svg?style=for-the-badge&logo=typescript&logoColor=white)
  ![WebSocket](https://img.shields.io/badge/websocket-%23000000.svg?style=for-the-badge&logo=websocket&logoColor=white)
  
</div>

---

## Sobre o projeto
 
Este projeto consiste no desenvolvimento de um ambiente próprio do jogo da cobrinha (**Snake**), como parte do Estudo Dirigido da disciplina Inteligência Artificial, ministrado pelo professor **Luis Filipe**, na Universidade Federal do Agreste de Pernambuco - UFAPE, durante o semestre de 2026.1.
 
O objetivo é implementar, treinar e comparar diferentes agentes inteligentes atuando sobre o mesmo ambiente: um agente de **busca heurística**, um agente de **aprendizado por reforço** e um agente de **algoritmo genético**.
##  Equipe de Desenvolvimento

<table align="center">
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/152096427?v=4" width="100px;" alt="Foto de Letícia Baracho"/><br>
        <sub>
          <b>Letícia Baracho</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/198010597?v=4" width="100px;" alt="Foto de Matheus Leal"/><br>
        <sub>
          <b>José Matheus Leal</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

### Ambiente e Backend
* ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python** — modelagem do ambiente (regras, estado, recompensa)
* ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** — servidor e comunicação em tempo real
* **WebSocket** — transmissão do estado do ambiente entre backend e frontend
### Frontend
* ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white) **Next.js** (React)
* ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white) **TypeScript**
* **Tailwind CSS** — estilização

## Como Executar
 
### 1. Backend 
 
```bash
# Acesse a pasta do backend
cd backend
 
# Instale as dependências
pip install -r requirements.txt
 
# Execute o servidor
uvicorn main:app --reload
```
 
### 2. Frontend
 
```bash
# Em um novo terminal, acesse a pasta do frontend
cd frontend
 
# Instale as dependências
npm install
 
# Inicie o servidor de desenvolvimento
npm run dev
```
 
O frontend estará acessível em: [http://localhost:3000](http://localhost:3000)
