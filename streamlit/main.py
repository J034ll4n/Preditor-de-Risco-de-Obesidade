import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Preditor de Risco de Obesidade",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- (CSS) ---
st.markdown("""
    <style>
    /* Configurações Gerais e Remoção de Bordas Brancas (Padding) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main {background-color: #F8F9FA;}
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    /* --- MENU LATERAL --- */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #E6E9EF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        font-weight: 600;
        color: #2C3E50;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #E8F8F5;
        border-color: #1ABC9C;
        color: #16A085;
        transform: translateX(5px);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1ABC9C !important;
        color: white !important;
        border-color: #1ABC9C !important;
        box-shadow: 0 4px 10px rgba(26, 188, 156, 0.3);
    }
    
    /* Formulários */
    div[data-testid="stForm"] div[role="radiogroup"] label > div:first-child {
        display: flex !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #BDC3C7;
        color: #2C3E50;
    }
    
    /* Cards Gráficos e Tabelas */
    div[data-testid="metric-container"], div.stPlotlyChart {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        width: 100% !important;
    }

    /* INSIGHT BOX (Estilo Nota Médica) */
    .insight-box {
        background-color: #E8F8F5;
        border-left: 5px solid #1ABC9C;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        font-size: 0.95em;
        color: #2C3E50;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .insight-title {
        font-weight: bold;
        color: #16A085;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.05em;
    }
    .insight-link {
        display: inline-block;
        margin-top: 8px;
        font-size: 0.85em;
        color: #16A085 !important;
        text-decoration: none;
        font-weight: 600;
        border: 1px solid #16A085;
        padding: 4px 12px;
        border-radius: 20px;
        transition: all 0.2s;
    }
    .insight-link:hover {
        background-color: #16A085;
        color: white !important;
    }
    
    /* Botões */
    div.stButton > button {
        background-color: #16A085;
        color: white;
        border-radius: 30px;
        border: none;
        padding: 15px 30px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    
    h1, h2, h3 { color: #2C3E50; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

API_URL = os.environ.get("API_URL", "http://api-service:5000")

# --- CORES ---
COLOR_MAP = {
    "Abaixo do Peso": "#3498DB", "Peso Normal": "#1ABC9C",
    "Sobrepeso G. I": "#F1C40F", "Sobrepeso G. II": "#F39C12",
    "Obesidade G. I": "#E67E22", "Obesidade G. II": "#FF6B6B",
    "Obesidade G. III": "#C0392B",
    "Sim": "#FF6B6B", "Não": "#1ABC9C", "Feminino": "#9B59B6", "Masculino": "#34495E"
}

with st.sidebar:
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=120)
    
    st.markdown("<h3 style='text-align: center; color: #2C3E50;'>Preditor de Risco de Obesidade</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    pagina = st.radio(
        "Navegação", 
        ["📈 Dashboard Analítico", "🩺 Diagnóstico Individual"], 
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #95a5a6; font-size: 0.8em;">
        Preditor de Risco v5.0<br>Ambiente Seguro SSL
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DAS PÁGINAS ---

if pagina == "📈 Dashboard Analítico":
    
    st.title("Visão Populacional")
    st.markdown("**Análise estratégica da base de dados com embasamento científico.**")
    st.markdown("---")

    try:
        @st.cache_data
        def load_data_v11():
            try: df = pd.read_csv('data/Obesity.csv')
            except: df = pd.read_csv('data/dados.csv')

            df.columns = df.columns.str.strip()
            
            rename_map = {
                'Historico_Familiar_Excesso_De_Peso': 'Hist_Familiar', 'Consumo_Frequente_Alta_Caloria': 'Hipercalorico',
                'Num_refeicoes': 'Num_Refeicoes', 'Comes_Entre_Refeicoes': 'Comer_Entre_Ref',
                'Consumo_Agua': 'Agua_Diaria', 'Monitora_Calorias': 'Monitora_Cal',
                'Freq_Atividade_Fisica': 'Freq_Exercicios', 'Tempo_uso_dispositivos_eletronicos': 'Tempo_Telas',
                'Consumo_Alcool': 'Alcool', 'Obesidade': 'Diagnostico',
                'Age': 'Idade', 'Gender': 'Genero', 'Height': 'Altura', 'Weight': 'Peso',
                'family_history': 'Hist_Familiar', 'FAVC': 'Hipercalorico',
                'FCVC': 'Freq_Vegetais', 'NCP': 'Num_Refeicoes', 'CH2O': 'Agua_Diaria',
                'FAF': 'Freq_Exercicios', 'TUE': 'Tempo_Telas', 'CALC': 'Alcool',
                'MTRANS': 'Transporte', 'Obesity': 'Diagnostico', 'NObeyesdad': 'Diagnostico'
            }
            df.rename(columns=rename_map, inplace=True)
            
            if 'Diagnostico' not in df.columns: return None

            val_map = {
                "Insufficient_Weight":"Abaixo do Peso", "Normal_Weight":"Peso Normal",
                "Overweight_Level_I":"Sobrepeso G. I", "Overweight_Level_II":"Sobrepeso G. II",
                "Obesity_Type_I":"Obesidade G. I", "Obesity_Type_II":"Obesidade G. II",
                "Obesity_Type_III":"Obesidade G. III",
                "Public_Transportation":"Transp. Público", "Walking":"Caminhada",
                "Automobile":"Carro", "Motorbike":"Moto", "Bike":"Bicicleta",
                "yes":"Sim", "no":"Não", "Female":"Feminino", "Male":"Masculino"
            }
            
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].map(lambda x: val_map.get(x, x))
            
            ordem = ["Abaixo do Peso", "Peso Normal", "Sobrepeso G. I", "Sobrepeso G. II", 
                     "Obesidade G. I", "Obesidade G. II", "Obesidade G. III"]
            df = df[df['Diagnostico'].isin(ordem)]
            df['Ordem'] = pd.Categorical(df['Diagnostico'], categories=ordem, ordered=True)
            df = df.sort_values('Ordem')
            return df

        df = load_data_v11()

        if df is not None:
            col_hist = 'Hist_Familiar' if 'Hist_Familiar' in df.columns else df.columns[4]
            col_telas = 'Tempo_Telas' if 'Tempo_Telas' in df.columns else df.columns[13]
            
            total_pacientes = len(df)
            obesos_total = len(df[df['Diagnostico'].str.contains("Obesidade")])
            perc_obesidade = (obesos_total / total_pacientes) * 100
            obesos_morbidos = len(df[df['Diagnostico'] == "Obesidade G. III"])

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Vidas Monitoradas", total_pacientes)
            k2.metric("Idade Média", f"{df['Idade'].mean():.0f} anos")
            k3.metric("IMC Médio Global", f"{(df['Peso']/(df['Altura']**2)).mean():.1f}")
            k4.metric("Taxa de Obesidade", f"{perc_obesidade:.1f}%", delta=f"{obesos_morbidos} casos graves", delta_color="inverse")
            
            st.markdown("---")

            # --- LINHA 1 ---
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📊 Distribuição de Risco")
                fig = px.pie(df, names='Diagnostico', color='Diagnostico', hole=0.6, color_discrete_map=COLOR_MAP)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.subheader("🔍 Análise de Clusters (Peso x Altura)")
                fig = px.scatter(df, x='Peso', y='Altura', color='Diagnostico', color_discrete_map=COLOR_MAP)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
                <div class="insight-title">📚 O Paradoxo do IMC e Gordura Visceral</div>
                Embora o IMC seja o padrão, a visualização de clusters revela sobreposições. 
                Estudos da <i>Nature</i> indicam que a gordura visceral e a circunferência abdominal são preditores de risco cardiovascular mais precisos que o peso isolado, 
                especialmente em indivíduos com alta massa muscular.
                <br>
                <a href="https://www.ncbi.nlm.nih.gov/books/NBK573068/" target="_blank" class="insight-link">🔗 Referência</a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("###")


            c3, c4 = st.columns(2)
            with c3:
                st.subheader("🧬 Fator Hereditário")
                fig = px.histogram(df, x='Diagnostico', color=col_hist, barmode='group', color_discrete_map=COLOR_MAP)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                st.subheader("📅 Idade vs Diagnóstico")
                fig = px.box(df, x='Diagnostico', y='Idade', color='Diagnostico', color_discrete_map=COLOR_MAP)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

 
            st.markdown("""
            <div class="insight-box">
                <div class="insight-title">🧬 Epigenética e Metabolismo</div>
                A forte correlação visual entre histórico familiar e obesidade (barras vermelhas) corrobora dados do CDC, 
                que atribuem à genética uma influência de 40-70% na predisposição. Além disso, o aumento de risco com a idade 
                reflete a queda natural da Taxa Metabólica Basal (TMB).
                <br>
                <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2880224/" target="_blank" class="insight-link">🔗 Referência</a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("###")


            st.markdown("---")
            c5, c6 = st.columns(2)
            with c5:
                st.subheader("🕸️ Radar de Hábitos (Normalizado)")
                cols_radar = ['Freq_Vegetais', 'Num_Refeicoes', 'Agua_Diaria', 'Freq_Exercicios', col_telas]
                valid_radar = [c for c in cols_radar if c in df.columns]
                
                if len(valid_radar) == 5:
                    
                    df_radar = df.groupby('Diagnostico')[valid_radar].mean().reset_index()
                    df_radar = df_radar[df_radar['Diagnostico'].isin(['Peso Normal', 'Obesidade G. III'])]
                    

                    max_values = {
                        'Freq_Vegetais': 3.0,   # Escala original 1-3
                        'Num_Refeicoes': 4.0,   # Escala original 1-4
                        'Agua_Diaria': 3.0,     # Escala original 1-3
                        'Freq_Exercicios': 3.0, # Escala original 0-3
                        col_telas: 2.0          # Escala original 0-2 
                    }
                    
                    # Aplica a normalização
                    for col in valid_radar:
                        df_radar[col] = df_radar[col] / max_values.get(col, 1)

                    fig = go.Figure()
                    colors_radar = {'Peso Normal': '#1ABC9C', 'Obesidade G. III': '#FF6B6B'}
                    
                    for i, row in df_radar.iterrows():
                        fig.add_trace(go.Scatterpolar(
                            r=row[valid_radar], 
                            theta=valid_radar, 
                            fill='toself', 
                            name=row['Diagnostico'], 
                            line_color=colors_radar.get(row['Diagnostico'], '#333'),
                            hoverinfo='text', 
                            text=[f"{val*100:.0f}% Intensidade" for val in row[valid_radar]]
                        ))
                    
                    # Ajusta o eixo para ir de 0 a 1 (0% a 100%)
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickformat=".0%")), 
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=20, b=20, l=40, r=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            with c6:
                st.subheader("🚌 Perfil de Risco por Transporte")
                if 'Transporte' in df.columns:
                    fig = px.histogram(
                        df, 
                        y="Transporte", 
                        color="Diagnostico", 
                        orientation='h', 
                        barnorm='percent', 
                        color_discrete_map=COLOR_MAP,
                        category_orders={"Diagnostico": ["Abaixo do Peso", "Peso Normal", "Sobrepeso G. I", "Sobrepeso G. II", "Obesidade G. I", "Obesidade G. II", "Obesidade G. III"]}
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', 
                        xaxis_title="Proporção (%)", 
                        yaxis_title=None,
                        legend_title=None
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            
            st.markdown("""
            <div class="insight-box">
                <div class="insight-title">🚶 Transporte Ativo e Saúde Pública</div>
                Estudos do <i>British Medical Journal</i> (BMJ) confirmam: o deslocamento ativo (bicicleta/caminhada) reduz significativamente o IMC e gordura corporal 
                comparado ao transporte privado. O gráfico de barras ilustra claramente como o ambiente obesogênico (uso de carros) domina os grupos de risco.
                <br>
                <a href="https://www.bmj.com/content/349/bmj.g4887" target="_blank" class="insight-link">🔗 Referência</a>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("Erro ao carregar dados. Verifique o arquivo .csv")

    except Exception as e:
        st.error(f"Erro no Dashboard: {e}")

elif pagina == "🩺 Diagnóstico Individual":
  
    st.title("Prontuário Digital")
    st.markdown("**Preencha os dados do paciente para obter a predição de risco via IA.**")
    st.markdown("---")
    
    with st.form("main_form"):
        st.subheader("👤 Dados Biométricos")
        col_bio1, col_bio2, col_bio3 = st.columns(3)
        with col_bio1: genero = st.radio("Gênero", ["Feminino", "Masculino"], horizontal=True)
        with col_bio2: idade = st.number_input("Idade", 10, 100, 25)
        with col_bio3: historico = st.selectbox("Histórico Familiar de Obesidade?", ["Sim", "Não"])
        
        col_bio4, col_bio5 = st.columns(2)
        with col_bio4: altura = st.number_input("Altura (m)", 1.00, 2.50, 1.70)
        with col_bio5: peso = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
        
        st.markdown("---")
        st.subheader("🍎 Hábitos Alimentares")
        col_food1, col_food2, col_food3 = st.columns(3)
        with col_food1: favc = st.selectbox("Dieta Hipercalórica?", ["Sim", "Não"])
        with col_food2: fcvc = st.slider("Vegetais (1=Nunca, 3=Sempre)", 1.0, 3.0, 2.0)
        with col_food3: ncp = st.slider("Refeições Principais/Dia", 1.0, 4.0, 3.0)
        
        col_food4, col_food5, col_food6 = st.columns(3)
        with col_food4: caec = st.selectbox("Comer entre refeições", ["Não", "Às vezes", "Freq.", "Sempre"])
        with col_food5: ch2o = st.slider("Água (Litros/dia)", 1.0, 3.0, 2.0)
        with col_food6: calc = st.selectbox("Consumo de Álcool", ["Não bebo", "Às vezes", "Freq.", "Sempre"])
        
        st.markdown("---")
        st.subheader("🏃 Estilo de Vida")
        
        col_life1, col_life2, col_life3 = st.columns(3)
        with col_life1: scc = st.selectbox("Monitora Calorias?", ["Sim", "Não"])
        with col_life2: smoke = st.selectbox("Fumante?", ["Sim", "Não"])
        with col_life3: transporte = st.selectbox("Transporte Principal", ["Transp. Público", "Automóvel", "Caminhada", "Bicicleta", "Moto"])
        
        col_life4, col_life5 = st.columns(2)
        with col_life4: faf = st.slider("Ativ. Física (dias/semana)", 0.0, 3.0, 1.0)
        with col_life5: tue = st.slider("Tempo em Telas (horas/dia)", 0.0, 24.0, 5.0)

        st.markdown("###")
        submit = st.form_submit_button("PROCESSAR ANÁLISE CLÍNICA")

    if submit:
        # Prepara dados
        map_gen = 1 if genero == "Masculino" else 0
        map_yn = lambda x: 1 if x == "Sim" else 0
        map_freq = {"Não":0, "Não bebo":0, "Às vezes":1, "Freq.":2, "Sempre":3}
        t_bike = 1 if transporte=="Bicicleta" else 0
        t_moto = 1 if transporte=="Moto" else 0
        t_pub = 1 if transporte=="Transp. Público" else 0
        t_walk = 1 if transporte=="Caminhada" else 0
        
        # Cálculos Extras
        imc_calc = peso / (altura ** 2)
        score_atletico = faf * 1.5 
        possivel_atleta = 1 if (faf >= 2 and imc_calc >= 25) else 0

        payload = {
            "Genero": map_gen, "Idade": idade, "Altura": altura, "Peso": peso,
            "Historico_Familiar_Excesso_De_Peso": map_yn(historico),
            "Consumo_Frequente_Alta_Caloria": map_yn(favc),
            "Freq_Vegetais": fcvc, "Num_refeicoes": ncp,
            "Comes_Entre_Refeicoes": map_freq.get(caec, 1),
            "Fumante": map_yn(smoke), "Consumo_Agua": ch2o, "Monitora_Calorias": map_yn(scc),
            "Freq_Atividade_Fisica": faf, "Tempo_uso_dispositivos_eletronicos": tue,
            "Consumo_Alcool": map_freq.get(calc, 0),
            "Transporte_Bike": t_bike, "Transporte_Motorbike": t_moto,
            "Transporte_Public_Transportation": t_pub, "Transporte_Walking": t_walk,
            
            "IMC": imc_calc,
            "Score_Atletico": score_atletico,
            "Possivel_Atleta": possivel_atleta
        }

        with st.spinner("Conectando à IA..."):
            try:
                resp = requests.post(f"{API_URL}/predict", json=payload)
                
                if resp.status_code == 200:
                    data = resp.json()
                    diag_raw = data['diagnostico']
                    
                    trad = {
                        "Insufficient_Weight": "Abaixo do Peso", "Normal_Weight": "Peso Normal",
                        "Overweight_Level_I": "Sobrepeso G. I", "Overweight_Level_II": "Sobrepeso G. II",
                        "Obesity_Type_I": "Obesidade G. I", "Obesity_Type_II": "Obesidade G. II",
                        "Obesity_Type_III": "Obesidade G. III"
                    }
                    diag_pt = trad.get(diag_raw, diag_raw)
                    cor_res = COLOR_MAP.get(diag_pt, "#777")

                    st.markdown("---")
                    c_res1, c_res2 = st.columns([2, 1])
                    with c_res1:
                        st.markdown(f"""
                        <div style="background-color: {cor_res}; padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                            <h3 style="color:white; margin:0;">Resultado da Análise</h3>
                            <h1 style="color:white; font-size: 3em; margin:0;">{diag_pt}</h1>
                            <p style="color: rgba(255,255,255,0.8);">Classificação Clínica Preditiva</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if data.get('atleta_detectado', False) or possivel_atleta == 1:
                            st.warning("💪 **Atenção Clínica:** Padrão de alta atividade física detectado. O IMC pode estar elevado devido à massa muscular.")
                    with c_res2:
                        st.metric("IMC Calculado", f"{imc_calc:.2f}")
                        st.metric("Grau de Confiança", f"{data.get('confianca', 0)*100:.1f}%")
                        st.progress(data.get('confianca', 0))
                else:
                    st.error(f"Erro na API (Status {resp.status_code})")
                    st.code(resp.text)
            except Exception as e:
                st.error(f"Erro de Conexão: {e}")