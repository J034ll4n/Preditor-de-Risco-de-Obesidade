import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import joblib
import numpy as np

# CONFIGURAÇÃO DA PÁGINA 
st.set_page_config(
    page_title="Preditor de Risco de Obesidade",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. CARREGAMENTO DOS MODELOS DE IA (INTEGRADO) ---
@st.cache_resource
def load_ml_models():
    model, scaler = None, None
    # Procura na pasta api ou na raiz (Streamlit Cloud)
    paths_model = ['api/modelo.pkl', 'modelo.pkl']
    paths_scaler = ['api/scaler.pkl', 'scaler.pkl']
    
    for p in paths_model:
        if os.path.exists(p):
            model = joblib.load(p)
            break
    for p in paths_scaler:
        if os.path.exists(p):
            scaler = joblib.load(p)
            break
    return model, scaler

model, scaler = load_ml_models()

# --- 2. CSS PROFISSIONAL (INTEGRAL) ---
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

COLOR_MAP = {
    "Abaixo do Peso": "#3498DB", "Peso Normal": "#1ABC9C",
    "Sobrepeso G. I": "#F1C40F", "Sobrepeso G. II": "#F39C12",
    "Obesidade G. I": "#E67E22", "Obesidade G. II": "#FF6B6B",
    "Obesidade G. III": "#C0392B",
    "Sim": "#C0392B", "Não": "#1ABC9C"
}

# --- 3. CARREGAMENTO DE DADOS (REFREÇADO) ---
@st.cache_data
def load_data():
    caminhos = ['Obesity.csv', 'data/Obesity.csv', 'streamlit/data/Obesity.csv', '/mount/src/preditor-de-risco-de-obesidade/data/Obesity.csv']
    df = None
    for p in caminhos:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is not None:
        df.columns = [str(c).strip() for c in df.columns]
        # Rename Map Robusto
        m = {
            'NObeyesdad': 'Diagnostico', 'family_history_with_overweight': 'Hist_Familiar',
            'Age': 'Idade', 'Weight': 'Peso', 'Height': 'Altura', 'Gender': 'Genero',
            'FCVC': 'Consumo_Vegetais', 'NCP': 'Refeicoes_Diarias', 'CH2O': 'Ingestao_Agua',
            'FAF': 'Atividade_Fisica', 'TUE': 'Tempo_Telas', 'MTRANS': 'Transporte'
        }
        df.rename(columns=m, inplace=True)
        
        val_map = {
            "Insufficient_Weight":"Abaixo do Peso", "Normal_Weight":"Peso Normal",
            "Overweight_Level_I":"Sobrepeso G. I", "Overweight_Level_II":"Sobrepeso G. II",
            "Obesity_Type_I":"Obesidade G. I", "Obesity_Type_II":"Obesidade G. II",
            "Obesity_Type_III":"Obesidade G. III", "yes":"Sim", "no":"Não",
            "Public_Transportation": "Transp. Público", "Walking": "Caminhada",
            "Automobile": "Automóvel", "Motorbike": "Moto", "Bike": "Bicicleta",
            "Male": "Masculino", "Female": "Feminino"
        }
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].map(lambda x: val_map.get(x, x))
        
        ordem = ["Abaixo do Peso", "Peso Normal", "Sobrepeso G. I", "Sobrepeso G. II", "Obesidade G. I", "Obesidade G. II", "Obesidade G. III"]
        if 'Diagnostico' in df.columns:
            df['Ordem'] = pd.Categorical(df['Diagnostico'], categories=ordem, ordered=True)
            return df.sort_values('Ordem')
    return df

# --- SIDEBAR ---
with st.sidebar:
    c_l1, c_l2, c_l3 = st.columns([1, 2, 1])
    with c_l2: st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=120)
    st.markdown("<h3 style='text-align: center;'>Gestão de Saúde IA</h3>", unsafe_allow_html=True)
    pagina = st.radio("Navegação", ["📈 Dashboard Analítico", "🩺 Diagnóstico Individual"], index=0)
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #95a5a6; font-size: 0.8em;'>Engenharia de Dados Joe</div>", unsafe_allow_html=True)

df = load_data()

# --- PÁGINA 1: DASHBOARD ---
if pagina == "📈 Dashboard Analítico":
    st.title("Visão Populacional")
    st.markdown("**Análise estratégica baseada em evidências científicas e cruzamento de dados biométricos.**")
    
    if df is not None:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Vidas Monitoradas", len(df))
        k2.metric("Idade Média", f"{df['Idade'].mean():.0f} anos")
        k3.metric("IMC Médio Global", f"{(df['Peso']/(df['Altura']**2)).mean():.1f}")
        taxa = (len(df[df['Diagnostico'].astype(str).str.contains('Obesidade')]) / len(df)) * 100
        k4.metric("Taxa de Obesidade", f"{taxa:.1f}%")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📊 Distribuição de Risco")
            fig = px.pie(df, names='Diagnostico', color='Diagnostico', hole=0.5, color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("🔍 Clusters: Peso x Altura")
            fig = px.scatter(df, x='Peso', y='Altura', color='Diagnostico', color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, use_container_width=True)

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
            if 'Hist_Familiar' in df.columns:
                fig = px.histogram(df, x='Diagnostico', color='Hist_Familiar', barmode='group', color_discrete_map=COLOR_MAP, labels={'Hist_Familiar': 'Histórico Familiar'})
                fig.update_layout(yaxis_title="Pacientes", xaxis_title="Diagnóstico")
                st.plotly_chart(fig, use_container_width=True)
            else: st.warning("Coluna 'Hist_Familiar' não encontrada.")
        with c4:
            st.subheader("📅 Idade vs Diagnóstico")
            fig = px.box(df, x='Diagnostico', y='Idade', color='Diagnostico', color_discrete_map=COLOR_MAP)
            st.plotly_chart(fig, use_container_width=True)

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
            cols_r = [c for c in radar_map.keys() if c in df.columns]
            if cols_r:
                df_radar = df.groupby('Diagnostico')[cols_r].mean().reset_index()
                df_radar = df_radar[df_radar['Diagnostico'].isin(['Peso Normal', 'Obesidade G. III'])]
                fig_radar = go.Figure()
                for i, row in df_radar.iterrows():
                    fig_radar.add_trace(go.Scatterpolar(r=row[cols_r], theta=[radar_map[c] for c in cols_r], fill='toself', name=row['Diagnostico'], line_color=COLOR_MAP.get(row['Diagnostico'])))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 4])), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_radar, use_container_width=True)
        with c6:
            st.subheader("🚌 Impacto do Transporte no Risco")
            fig = px.histogram(df, y="Transporte", color="Diagnostico", orientation='h', barnorm='percent', color_discrete_map=COLOR_MAP)
            fig.update_layout(xaxis_title="Proporção Populacional (%)", yaxis_title="Tipo de Transporte")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">🚶 Transporte Ativo e Saúde Pública</div>
                O perfil por meio de transporte revela o impacto do ambiente obesogênico: o uso de automóveis domina os grupos de risco elevado. Estudos do <b>British Medical Journal (BMJ)</b> confirmam que o deslocamento ativo (bicicleta ou caminhada) promove uma redução sustentável do IMC e melhora significativamente o perfil inflamatório sistêmico em comparação ao transporte passivo.
                <br><a href="https://www.bmj.com/content/349/bmj.g4887" target="_blank" class="insight-link">🔗 Referência BMJ Journal</a>
            </div>
        """, unsafe_allow_html=True)

# --- PÁGINA 2: DIAGNÓSTICO ---
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
        if model and scaler:
            map_freq = {"Não":0, "Não bebo":0, "Às vezes":1, "Freq.":2, "Sempre":3}
            imc_calc = peso / (altura ** 2)
            
            # Array de 19 variáveis
            arr = np.array([[
                1 if genero == "Masculino" else 0, idade, 1 if historico == "Sim" else 0,
                1 if favc == "Sim" else 0, fcvc, ncp, map_freq.get(caec, 1), 
                1 if smoke == "Sim" else 0, ch2o, 1 if scc == "Sim" else 0,
                faf, tue, map_freq.get(calc, 0),
                1 if transporte=="Bicicleta" else 0, 1 if transporte=="Moto" else 0,
                1 if transporte=="Transp. Público" else 0, 1 if transporte=="Caminhada" else 0,
                faf * 1.5, 1 if (faf >= 2 and imc_calc >= 25) else 0
            ]])
            
            with st.spinner("IA Analisando..."):
                scaled = scaler.transform(arr)
                pred = model.predict(scaled)[0]
                probs = model.predict_proba(scaled)[0]
                risco_total = np.sum(probs[2:])
                names = ["Abaixo do Peso", "Peso Normal", "Sobrepeso G. I", "Sobrepeso G. II", "Obesidade G. I", "Obesidade G. II", "Obesidade G. III"]
                diag = names[pred]

                st.markdown("---")
                t_card, c_card = "Diagnóstico IA", COLOR_MAP.get(diag, "#16A085")
                sub = f"Seu IMC ({imc_calc:.1f}) é saudável, mas seus hábitos sinalizam tendência a ganho de peso." if (imc_calc < 25 and "Obesidade" in diag) else "Classificação baseada em comportamento e biometria."

                st.markdown(f"""<div class="result-card" style="background-color: {c_card};"><h3>{t_card}</h3><h1 style="color:white; font-size: 3em; margin:0;">{diag}</h1><p>{sub}</p></div>""", unsafe_allow_html=True)

                r1, r2, r3 = st.columns(3)
                with r1: st.metric("IMC Atual", f"{imc_calc:.2f}"); st.caption("Referência ideal: 18.5 a 24.9")
                with r2: st.metric("Tendência de Risco", f"{risco_total*100:.1f}%")
                with r3: st.write("**Nível de Risco Geral:**"); st.progress(float(risco_total))
                
                st.markdown(f"""<div style='font-size: 1.1em; margin: 15px 0;'><b>Resumo Clínico:</b><br>O modelo detectou hábitos <b>{risco_total*100:.1f}%</b> compatíveis com quadros de ganho de peso severo.</div>""", unsafe_allow_html=True)

                st.markdown("### 📋 Plano de Intervenção Sugerido")
                recs = []
                if ch2o < 2.0: recs.append(["💧 Hidratação", f"{ch2o:.1f} L/dia", "Aumentar a ingestão para 35ml/kg. A água é essencial para otimizar o metabolismo basal."])
                if faf < 2.0: recs.append(["🏃 Atividade Física", "Insuficientemente Ativo", "Aumentar a frequência semanal. A meta mínima da OMS é de 150 min de atividade moderada."])
                if tue > 4.0: recs.append(["📱 Fadiga Digital", f"{int(tue)} h/dia", "Reduzir o tempo de tela contínuo para evitar comportamento sedentário e inflamação sistêmica."])
                if favc == "Sim": recs.append(["🍔 Padrão Dietético", "Alta caloria", "Priorizar alimentos in natura. O consumo frequente de alta caloria desregula a saciedade."])
                if fcvc < 2.5: recs.append(["🥗 Micronutrientes", "Baixo consumo", "Aumentar vegetais nas refeições principais para garantir o aporte necessário de fibras e vitaminas."])
                if smoke == "Sim": recs.append(["🚭 Tabagismo", "Fumante", "O hábito tabágico eleva o estresse oxidativo e prejudica a recuperação metabólica."])
                if calc in ["Freq.", "Sempre"]: recs.append(["🍺 Consumo Alcoólico", "Elevado", "O álcool fornece calorias vazias e reduz a oxidação de gorduras pelo fígado."])
                
                if recs:
                    st.dataframe(pd.DataFrame(recs, columns=["Fator", "Situação Atual", "Conduta Recomendada"]), hide_index=True, use_container_width=True)
        else: st.error("Arquivos de IA não encontrados.")