# 🧬 Preditor de Risco de Obesidade

## 📋 Sobre o Projeto
Este projeto foi desenvolvido como parte do **Tech Challenge da Fase 4** (FIAP). O objetivo é auxiliar profissionais de saúde no diagnóstico preditivo de obesidade utilizando **Machine Learning** e visualização de dados interativa.

A aplicação resolve o problema da triagem médica, oferecendo:
1.  **Dashboard Analítico:** Visão populacional estratégica com insights científicos sobre fatores de risco, mobilidade e genética.
2.  **Prontuário Digital (IA):** Um sistema especialista que prevê o grau de obesidade de um paciente específico com base em seus hábitos e biometria.

---

##  Arquitetura da Solução
A solução utiliza uma arquitetura containerizada, separando o Frontend (Streamlit) da lógica de Machine Learning.

![Arquitetura do Projeto](img/arquitetura.jpg)

---

##  Interface e Funcionalidades

### 1. Dashboard Executivo
Visão macro da população monitorada, com KPIs de saúde e alertas para casos graves.
![Visão Geral](img/1.png)

### 2. Análise de Clusters e Distribuição
Correlação entre Peso x Altura e a distribuição das classes de obesidade na base de dados.
![Clusters](img/2.png)

### 3. Fatores Clínicos
Análise do impacto do histórico familiar (genética) e da idade no agravamento do quadro clínico.
![Fatores](img/3.png)

### 4. Estilo de Vida e Mobilidade
Radar de hábitos comparativo (Saudável vs Obesidade G.III) e impacto do transporte no IMC.
![Lifestyle](img/4.png)

### 5. Prontuário Digital (Input)
Formulário intuitivo para inserção de dados biométricos e comportamentais do paciente.
![Formulário](img/5.png)

### 6. Diagnóstico com IA
Resultado em tempo real com a classificação de risco, cálculo de IMC e grau de confiança do modelo.
![Resultado](img/6.png)

---

##  Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Frontend:** [Streamlit](https://streamlit.io/) (Interface Web Interativa)
* **Visualização:** Plotly Express & Graph Objects
* **Machine Learning:** Scikit-learn (Random Forest/Gradient Boosting)
* **Infraestrutura:** Docker & Docker Compose

---

##  Como Rodar o Projeto

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.
* Git instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/J034ll4n/Preditor-de-Risco-de-Obesidade.git](https://github.com/J034ll4n/Preditor-de-Risco-de-Obesidade.git)
    ```

2.  **Acesse a pasta do projeto:**
    ```bash
    cd Preditor-de-Risco-de-Obesidade
    ```

3.  **Suba a aplicação com Docker:**
    Este comando irá baixar as dependências, construir a imagem e iniciar o servidor.
    ```bash
    docker-compose up --build
    ```

4.  **Acesse no Navegador:**
    * Abra: [http://localhost:8501](http://localhost:8501)

---

##  Estrutura de Pastas

```text
/
├── api/             # API Backend (se houver separação)
├── data/            # Dataset (Obesity.csv)
├── img/             # Imagens da documentação
├── streamlit/       # Código da Aplicação Frontend
│   └── main.py      # Ponto de entrada
├── docker-compose.yml
├── requirements.txt
└── README.md
