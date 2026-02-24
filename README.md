# 🧬 Preditor de Risco de Obesidade

Este projeto é a entrega da **Fase 4 do Tech Challenge (FIAP)**. visão clínica para oferecer uma ferramenta robusta de suporte à decisão médica no monitoramento da obesidade.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://preditor-de-risco-de-obesidade-adb5lkuptneqh6hkq83d9f.streamlit.app/)

---

## 🔬 Diferenciais da Solução

Diferente de preditores comuns, esta aplicação foca na **Prevenção Ativa**:
* **Risco Metabólico Acumulado:** O algoritmo calcula a soma das probabilidades de todas as faixas de sobrepeso e obesidade, gerando um alerta precoce mesmo para pacientes que ainda apresentam IMC dentro da normalidade.
* **Fundamentação Científica:** Dashboards integrados com correlações baseadas em evidências de estudos da *Nature Portfolio*, *CDC* e *British Medical Journal (BMJ)*.
* **Detecção de Perfil Atlético:** Lógica implementada para mitigar falsos positivos em indivíduos com alta massa muscular, onde o IMC isolado não reflete o real risco metabólico.

---

## 🏗️ Arquitetura e Fluxo de Dados

A aplicação opera em uma arquitetura de microsserviços containerizada para garantir escalabilidade e separação de responsabilidades:

1.  **Frontend (Streamlit):** Interface interativa para visualização de tendências populacionais e entrada de dados individuais.
2.  **API de Predição (Flask):** Engine de Machine Learning que processa o modelo `Random Forest` e retorna a análise de risco e predição.
3.  **Processamento:** Normalização de dados via `StandardScaler` aplicada em tempo real sobre os inputs do usuário.

---

## 📊 Módulos do Sistema

### 📈 Dashboard Analítico
Visão estratégica da base de dados monitorada:
* **Distribuição de Risco:** Visão macro das categorias de peso na população.
* **Análise de Clusters:** Correlação visual entre Peso x Altura para identificação de padrões.
* **Fatores Determinantes:** Impacto do histórico familiar e da idade no agravamento do quadro clínico.
* **Radar de Hábitos:** Comparativo direto entre perfis saudáveis e de alto risco.

### 🩺 Prontuário Digital Inteligente
Interface para diagnóstico individualizado:
* **Classificação Clínica:** Resultado em tempo real baseado em 17 biomarcadores comportamentais.
* **Tendência de Risco:** Métrica de compatibilidade com quadros de ganho de peso severo.
* **Plano de Intervenção:** Recomendações personalizadas e automáticas para correção de hábitos.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9
* **Data Science:** Pandas, Numpy, Scikit-learn, Joblib
* **Visualização:** Plotly Express & Graph Objects
* **Backend:** Flask (REST API)
* **Frontend:** Streamlit
* **DevOps:** Docker & Docker Compose

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/J034ll4n/Preditor-de-Risco-de-Obesidade.git](https://github.com/J034ll4n/Preditor-de-Risco-de-Obesidade.git)
    cd Preditor-de-Risco-de-Obesidade
    ```

2.  **Suba a aplicação:**
    Este comando irá construir as imagens e iniciar os serviços da API e do Frontend.
    ```bash
    docker-compose up --build
    ```

3.  **Acesse no seu navegador:**
    * **App Streamlit:** [http://localhost:8501](http://localhost:8501)
    * **API Flask:** [http://localhost:5000](http://localhost:5000)

---

## 📂 Estrutura de Pastas

```text
├── api/                # Backend Flask e Motor de IA
│   ├── app.py          # Lógica da API e cálculo de Risco Acumulado
│   ├── modelo.pkl      # Modelo Random Forest treinado (98% acurácia)
│   └── scaler.pkl      # Normalizador de dados (StandardScaler)
├── data/               # Base de dados (Obesity.csv)
├── img/                # Assets para documentação
├── main.py             # Interface Frontend Streamlit
├── docker-compose.yml  # Orquestração dos containers
├── Dockerfile          # Definição das imagens Docker
└── requirements.txt    # Dependências do ecossistema Python