# api/app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

modelo = joblib.load('modelo.pkl')
scaler = joblib.load('scaler.pkl')
target_map = joblib.load('target_map.pkl')
target_map_inv = {v: k for k, v in target_map.items()}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json 
    
    input_df = pd.DataFrame([data])
    
    colunas_normalizar = [
        'Idade', 'Altura', 'Peso', 'IMC', 'Freq_Vegetais', 'Num_refeicoes', 
        'Consumo_Agua', 'Freq_Atividade_Fisica', 'Tempo_uso_dispositivos_eletronicos',
        'Comes_Entre_Refeicoes', 'Consumo_Alcool'
    ]
    input_df[colunas_normalizar] = scaler.transform(input_df[colunas_normalizar])
    
    input_df['Score_Atletico'] = input_df['Freq_Atividade_Fisica'] * (input_df['IMC'] + 3)
    input_df['Possivel_Atleta'] = (input_df['Score_Atletico'] > 5).astype(int)
    
    predicao = modelo.predict(input_df)[0]
    resultado_texto = target_map_inv[predicao]
    probabilidade = float(modelo.predict_proba(input_df).max())
    
    return jsonify({
        "diagnostico": resultado_texto,
        "confianca": probabilidade,
        "imc": float(data['IMC']), # Retornamos o IMC original
        "atleta_detectado": bool(input_df['Possivel_Atleta'].iloc[0])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)