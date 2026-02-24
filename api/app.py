# api/app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Certifique-se de que os arquivos .pkl estão na mesma pasta que este arquivo
modelo = joblib.load('modelo.pkl')
scaler = joblib.load('scaler.pkl')

# Dicionário de mapeamento para tradução clínica
target_map_real = {
    0: "Abaixo do Peso",
    1: "Peso Normal",
    2: "Sobrepeso G. I",
    3: "Sobrepeso G. II",
    4: "Obesidade G. I",
    5: "Obesidade G. II",
    6: "Obesidade G. III"
}

# Lista exata de colunas que o modelo espera
COLUNAS_MODELO = [
    'Genero', 'Idade', 'Historico_Familiar_Excesso_De_Peso', 
    'Consumo_Frequente_Alta_Caloria', 'Freq_Vegetais', 'Num_refeicoes', 
    'Comes_Entre_Refeicoes', 'Fumante', 'Consumo_Agua', 'Monitora_Calorias', 
    'Freq_Atividade_Fisica', 'Tempo_uso_dispositivos_eletronicos', 
    'Consumo_Alcool', 'Transporte_Bike', 'Transporte_Motorbike', 
    'Transporte_Public_Transportation', 'Transporte_Walking', 
    'Score_Atletico', 'Possivel_Atleta'
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recebe os dados do formulário do Streamlit
        data = request.json 
        input_df = pd.DataFrame([data])
        
        # Garante a ordem correta das features e preenche vazios com 0
        df_model = input_df.reindex(columns=COLUNAS_MODELO, fill_value=0)
        
        # Aplica a normalização (Scaler)
        X_scaled = scaler.transform(df_model)
        
        # Realiza a predição da classe (o que a pessoa "é" agora)
        predicao_bruta = modelo.predict(X_scaled)[0]
        predicao_num = int(predicao_bruta) 
        
        # --- LÓGICA DE RISCO ACUMULADO ---
        # Obtemos as probabilidades para cada uma das 7 categorias
        probabilidades = modelo.predict_proba(X_scaled)[0] 
        
        # Mapeamento dos índices das probabilidades:
        # [0: Abaixo, 1: Normal, 2: Sobrepeso I, 3: Sobrepeso II, 4: Obeso I, 5: Obeso II, 6: Obeso III]
        
        # Somamos as probabilidades de todos os estados acima do "Peso Normal" 
        # Isso dá o "Risco Total" de não estar no peso ideal
        risco_total = float(np.sum(probabilidades[2:])) 
        
        # Pegamos a confiança específica da classe que o modelo escolheu
        confianca_classe = float(np.max(probabilidades))
        
        # Busca o nome clínico da categoria
        resultado_texto = target_map_real.get(predicao_num, f"Classe {predicao_num}")
        
        print(f"✅ Predição: {resultado_texto} | Risco Total: {risco_total*100:.1f}%")

        return jsonify({
            "diagnostico": str(resultado_texto),
            "confianca": confianca_classe,
            "risco_total": risco_total,
            "status": "sucesso"
        })

    except Exception as e:
        print(f"🛑 ERRO NA API: {str(e)}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' permite que o Docker acesse a porta
    app.run(host='0.0.0.0', port=5000, debug=True)