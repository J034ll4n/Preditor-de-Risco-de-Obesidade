import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Preditor de Risco de Obesidade",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F8F9FA !important; }
    h1, h2, h3, p, label, .stMetric, span { color: #2C3E50 !important; }
    
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E6E9EF; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label { 
        background-color: #F1F3F6; padding: 15px 20px; border-radius: 12px; 
        margin-bottom: 12px; border: 1px solid #E6E9EF; font-weight: 600; color: #2C3E50; 
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] { 
        background-color: #1ABC9C !important; color: white !important; 
    }
    
    .insight-box { background-color: #E8F8F5; border-left: 5px solid #1ABC9C; padding: 20px; border-radius: 8px; margin: 20px 0; color: #2C3E50; }
    .insight-title { font-weight: bold; color: #16A085; margin-bottom: 8px; font-size: 1.1em; }
    .insight-link { color: #16A085; text-decoration: none; font-weight: bold; }

    .result-card { padding: 30px; border-radius: 20px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 25px; }
    
    div.stButton > button { background-color: #16A085; color: white; border-radius: 30px; padding: 18px; width: 100%; border: none; font-weight: bold; font-size: 1.2em; }
    div.stButton > button:hover { background-color: #1ABC9C; color: white; }
    </style>
    """, unsafe_allow_html=True)

API_URL = os.environ.get("API_URL", "http://api-service:5000")

COLOR_MAP = {
    "Abaixo do Peso": "#3498DB", 
    "Peso Normal": "#1ABC9C",
    "Sobrepeso G. I": "#F1C40F", 
    "Sobrepeso G. II": "#F39C12",
    "Obesidade G. I": "#E67E22", 
    "Obesidade G. II": "#FF6B6B",
    "Obesidade G. III": "#C0392B",
    "Sim": "#C0392B", 
    "Não": "#1ABC9C"
}

@st.cache_data
def load_data():
    caminho = 'data/Obesity.csv' 
    if not os.path.exists(caminho): return None
    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()
    
    rename_map = {
        'Obesidade': 'Diagnostico',
        'Historico_Familiar_Excesso_De_Peso': 'Hist_Familiar',
        'Num_refeicoes': 'Refeicoes_Diarias',
        'Consumo_Agua': 'Ingestao_Agua',
        'Freq_Atividade_Fisica': 'Atividade_Fisica',
        'Tempo_uso_dispositivos_eletronicos': 'Tempo_Telas',
        'Freq_Vegetais': 'Consumo_Vegetais'
    }
    df.rename(columns=rename_map, inplace=True)
    
    val_map = {
        "Insufficient_Weight":"Abaixo do Peso", "Normal_Weight":"Peso Normal",
        "Overweight_Level_I":"Sobrepeso G. I", "Overweight_Level_II":"Sobrepeso G. II",
        "Obesity_Type_I":"Obesidade G. I", "Obesity_Type_II":"Obesidade G. II",
        "Obesity_Type_III":"Obesidade G. III", "yes":"Sim", "no":"Não",
        "Public_Transportation": "Transp. Público", "Walking": "Caminhada",
        "Automobile": "Automóvel", "Motorbike": "Moto", "Bike": "Bicicleta"
    }
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].map(lambda x: val_map.get(x, x))
    
    ordem = ["Abaixo do Peso", "Peso Normal", "Sobrepeso G. I", "Sobrepeso G. II", "Obesidade G. I", "Obesidade G. II", "Obesidade G. III"]
    df['Ordem'] = pd.Categorical(df['Diagnostico'], categories=ordem, ordered=True)
    return df.sort_values('Ordem')

with st.sidebar:
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2: st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=120)
    st.markdown("<h3 style='text-align: center;'>Gestão de Saúde IA</h3>", unsafe_allow_html=True)
    pagina = st.radio("Navegação", ["📈 Dashboard Analítico", "🩺 Diagnóstico Individual"], index=0)
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #95a5a6; font-size: 0.8em;'>Engenharia de Dados Joe</div>", unsafe_allow_html=True)

if pagina == "📈 Dashboard Analítico":
    st.title("Visão Populacional")
    st.markdown("**Análise estratégica baseada em evidências científicas e cruzamento de dados biométricos.**")
    
    df = load_data()
    if df is not None:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Vidas Monitoradas", len(df))
        k2.metric("Idade Média", f"{df['Idade'].mean():.0f} anos")
        k3.metric("IMC Médio Global", f"{(df['Peso']/(df['Altura']**2)).mean():.1f}")
        k4.metric("Taxa de Obesidade", f"{(len(df[df['Diagnostico'].str.contains('Obesidade')]) / len(df)) * 100:.1f}%")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📊 Distribuição de Risco")
            fig = px.pie(df, names='Diagnostico', color='Diagnostico', hole=0.5, color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, width="stretch")
        with c2:
            st.subheader("🔍 Clusters: Peso x Altura")
            fig = px.scatter(df, x='Peso', y='Altura', color='Diagnostico', color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, width="stretch")

        st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">📚 O Paradoxo do IMC e Gordura Visceral</div>
                A análise de dispersão (Peso x Altura) demonstra a aplicação prática do IMC, porém, as sobreposições observadas nos clusters evidenciam que o peso isolado não diferencia massa magra de adiposidade. Segundo a <b>Nature</b>, a gordura visceral é um preditor de risco cardiovascular e metabólico muito mais preciso do que a antropometria simples, especialmente em perfis com alta densidade muscular.
                <br><a href="https://www.ncbi.nlm.nih.gov/books/NBK573068/" target="_blank" class="insight-link">🔗 Referência Nature Portfolio</a>
            </div>
        """, unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("🧬 Fator Hereditário")
            fig = px.histogram(df, x='Diagnostico', color='Hist_Familiar', barmode='group', 
                               color_discrete_map=COLOR_MAP,
                               labels={'Hist_Familiar': 'Histórico Familiar'})
            fig.update_layout(yaxis_title="Pacientes", xaxis_title="Diagnóstico")
            st.plotly_chart(fig, width="stretch")
        with c4:
            st.subheader("📅 Idade vs Diagnóstico")
            fig = px.box(df, x='Diagnostico', y='Idade', color='Diagnostico', color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, width="stretch")

        st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">🧬 Epigenética e Metabolismo</div>
                A correlação visual entre histórico familiar e obesidade (barras vermelhas) valida a forte influência epigenética, que pode representar de 40% a 70% da predisposição fenotípica. Paralelamente, o gráfico de idade ilustra como a progressão do diagnóstico se intensifica com a maturidade, refletindo a queda fisiológica da Taxa Metabólica Basal (TMB).
                <br><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2880224/" target="_blank" class="insight-link">🔗 Referência CDC / PMC</a>
            </div>
        """, unsafe_allow_html=True)

        c5, c6 = st.columns(2)
        with c5:
            st.subheader("🕸️ Radar de Hábitos Saudáveis")
            radar_map = {'Consumo_Vegetais': 'Vegetais', 'Refeicoes_Diarias': 'Refeições', 'Ingestao_Agua': 'Água', 'Atividade_Fisica': 'Exercício'}
            df_radar = df.groupby('Diagnostico')[list(radar_map.keys())].mean().reset_index()
            df_radar = df_radar[df_radar['Diagnostico'].isin(['Peso Normal', 'Obesidade G. III'])]
            fig_radar = go.Figure()
            for i, row in df_radar.iterrows():
                fig_radar.add_trace(go.Scatterpolar(r=row[list(radar_map.keys())], theta=list(radar_map.values()), fill='toself', name=row['Diagnostico'], line_color=COLOR_MAP.get(row['Diagnostico'])))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 4])), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_radar, width="stretch")
        with c6:
            st.subheader("🚌 Impacto do Transporte no Risco")
            fig = px.histogram(df, y="Transporte", color="Diagnostico", orientation='h', barnorm='percent', color_discrete_map=COLOR_MAP)
            fig.update_layout(xaxis_title="Proporção Populacional (%)", yaxis_title="Tipo de Transporte")
            st.plotly_chart(fig, width="stretch")

        st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">🚶 Transporte Ativo e Saúde Pública</div>
                O perfil por meio de transporte revela o impacto do ambiente obesogênico: o uso de automóveis domina os grupos de risco elevado. Estudos do <b>British Medical Journal (BMJ)</b> confirmam que o deslocamento ativo (bicicleta ou caminhada) promove uma redução sustentável do IMC e melhora significativamente o perfil inflamatório sistêmico em comparação ao transporte passivo.
                <br><a href="https://www.bmj.com/content/349/bmj.g4887" target="_blank" class="insight-link">🔗 Referência BMJ Journal</a>
            </div>
        """, unsafe_allow_html=True)

elif pagina == "🩺 Diagnóstico Individual":
    st.title("Prontuário Digital Inteligente")
    st.markdown("**Análise preditiva baseada em comportamento metabólico.**")
    
    with st.form("main_form"):
        st.subheader("👤 Biometria")
        cb1, cb2, cb3 = st.columns(3)
        with cb1: genero = st.radio("Gênero", ["Feminino", "Masculino"], horizontal=True)
        with cb2: idade = st.number_input("Idade", 10, 100, 25)
        with cb3: historico = st.selectbox("Histórico Familiar de Obesidade?", ["Sim", "Não"])
        cb4, cb5 = st.columns(2)
        with cb4: altura = st.number_input("Altura (m)", 1.00, 2.50, 1.70, step=0.01)
        with cb5: peso = st.number_input("Peso (kg)", 30.0, 250.0, 70.0, step=0.1)
        
        st.subheader("🍎 Hábitos de Consumo")
        f1, f2, f3 = st.columns(3)
        with f1: favc = st.selectbox("Dieta Hipercalórica?", ["Sim", "Não"])
        with f2: fcvc = st.slider("Frequência de Vegetais", 1.0, 3.0, 2.0)
        with f3: ncp = st.slider("Refeições por Dia", 1.0, 4.0, 3.0)
        f4, f5, f6 = st.columns(3)
        with f4: caec = st.selectbox("Comer entre refeições", ["Não", "Às vezes", "Freq.", "Sempre"])
        with f5: ch2o = st.slider("Ingestão de Água (L/dia)", 1.0, 3.0, 2.0)
        with f6: calc = st.selectbox("Consumo de Álcool", ["Não bebo", "Às vezes", "Freq.", "Sempre"])
        
        l1, l2, l3, l4, l5 = st.columns(5)
        with l1: scc = st.selectbox("Monitora Cal.?", ["Sim", "Não"])
        with l2: smoke = st.selectbox("Fumante?", ["Sim", "Não"])
        with l3: transporte = st.selectbox("Transporte", ["Transp. Público", "Caminhada", "Bicicleta", "Moto", "Automóvel"])
        with l4: faf = st.slider("Exercício", 0.0, 3.0, 1.0)
        with l5: tue = st.slider("Telas (h/dia)", 0.0, 24.0, 5.0)
        submit = st.form_submit_button("PROCESSAR ANÁLISE CLÍNICA")

    if submit:
        map_freq = {"Não":0, "Não bebo":0, "Às vezes":1, "Freq.":2, "Sempre":3}
        imc_calc = peso / (altura ** 2)
        score_atl = faf * 1.5 
        poss_atl = 1 if (faf >= 2 and imc_calc >= 25) else 0
        
        payload = {
            "Genero": 1 if genero == "Masculino" else 0, "Idade": idade,
            "Historico_Familiar_Excesso_De_Peso": 1 if historico == "Sim" else 0,
            "Consumo_Frequente_Alta_Caloria": 1 if favc == "Sim" else 0,
            "Freq_Vegetais": fcvc, "Num_refeicoes": ncp, "Comes_Entre_Refeicoes": map_freq.get(caec, 1),
            "Fumante": 1 if smoke == "Sim" else 0, "Consumo_Agua": ch2o, "Monitora_Calorias": 1 if scc == "Sim" else 0,
            "Freq_Atividade_Fisica": faf, "Tempo_uso_dispositivos_eletronicos": tue, "Consumo_Alcool": map_freq.get(calc, 0),
            "Transporte_Bike": 1 if transporte=="Bicicleta" else 0, "Transporte_Motorbike": 1 if transporte=="Moto" else 0,
            "Transporte_Public_Transportation": 1 if transporte=="Transp. Público" else 0,
            "Transporte_Walking": 1 if transporte=="Caminhada" else 0, "Score_Atletico": score_atl, "Possivel_Atleta": poss_atl
        }

        with st.spinner("IA Analisando..."):
            try:
                resp = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    diag = data['diagnostico']
                    risco_total = data.get('risco_total', 0)

                    st.markdown("---")
                    if imc_calc < 25 and "Obesidade" in diag:
                        t_card, c_card, sub = "Alerta de Risco Futuro", "#E67E22", f"Seu IMC ({imc_calc:.1f}) é saudável, mas seus hábitos sinalizam tendência a <b>{diag}</b>."
                    else:
                        t_card, c_card, sub = "Diagnóstico IA", COLOR_MAP.get(diag, "#16A085"), "Classificação baseada em comportamento e biometria."

                    st.markdown(f"""
                        <div class="result-card" style="background-color: {c_card};">
                            <h3 style="color:white; margin:0;">{t_card}</h3>
                            <h1 style="color:white; font-size: 3em; margin:0;">{diag}</h1>
                            <p style="color: rgba(255,255,255,0.9); font-size: 1.1em; margin-top:10px;">{sub}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    r1, r2, r3 = st.columns(3)
                    with r1: st.metric("IMC Atual", f"{imc_calc:.2f}"); st.caption("Referência ideal: 18.5 a 24.9")
                    with r2: st.metric("Tendência de Risco", f"{risco_total*100:.1f}%")
                    with r3: 
                        st.write("**Nível de Risco Geral:**")
                        st.progress(risco_total)
                    
                    st.markdown(f"""
                    <div style='font-size: 1.1em; margin: 15px 0;'>
                        <b>Resumo Clínico:</b><br>
                        O modelo detectou hábitos <b>{risco_total*100:.1f}%</b> compatíveis com quadros de ganho de peso severo.
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("### 📋 Plano de Intervenção Sugerido")
                    recs = []
                    if ch2o < 2.0:
                        recs.append(["💧 Hidratação", f"{ch2o:.1f} L/dia", "Aumentar a ingestão para 35ml/kg. A água é essencial para otimizar o metabolismo basal."])
                    if faf < 2.0:
                        recs.append(["🏃 Atividade Física", f"{faf:.1f} dia(s)/sem", "Aumentar a frequência semanal. A meta mínima da OMS é de 150 min de atividade moderada."])
                    if tue > 4.0:
                        recs.append(["📱 Fadiga Digital", f"{tue:.1f} h/dia", "Reduzir o tempo de tela contínuo para evitar comportamento sedentário e inflamação sistêmica."])
                    if favc == "Sim":
                        recs.append(["🍔 Padrão Dietético", "Alta caloria", "Priorizar alimentos in natura. O consumo frequente de alta caloria desregula a saciedade."])
                    if fcvc < 2.5:
                        recs.append(["🥗 Micronutrientes", "Baixo consumo", "Aumentar vegetais nas refeições principais para garantir o aporte necessário de fibras e vitaminas."])
                    if smoke == "Sim":
                        recs.append(["🚭 Tabagismo", "Fumante", "O hábito tabágico eleva o estresse oxidativo e prejudica a recuperação metabólica."])
                    if calc in ["Freq.", "Sempre"]:
                        recs.append(["🍺 Consumo Alcoólico", "Elevado", "O álcool fornece calorias vazias e reduz a oxidação de gorduras pelo fígado."])
                    
                    if recs:
                        df_recs = pd.DataFrame(recs, columns=["Fator", "Situação Atual", "Conduta Recomendada"])
                        st.dataframe(df_recs, hide_index=True, width="stretch")

                else: st.error("Erro na API.")
            except Exception as e: st.error(f"Erro: {e}")