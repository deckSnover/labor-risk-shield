import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

class GRCAnalytics90Days:
    def __init__(self):
        # Define caminhos e garante que as pastas existam
        self.ASSETS_PATH = 'assets'
        self.LOG_PATH = 'logs'
        for path in [self.ASSETS_PATH, self.LOG_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)
        
        # Estilo visual para o GitHub (Dark Mode)
        plt.style.use('dark_background')

    def gerar_colaboradores(self):
        """Simula um cadastro master de RH (ERP)"""
        setores = ['Logística', 'Operacional', 'Transporte', 'Administrativo']
        colaboradores = []
        for i in range(1, 151): # 150 colaboradores simulados
            colaboradores.append({
                'Matricula': f'MAT{i:04d}',
                'Nome': f'Colaborador {i}',
                'Setor': np.random.choice(setores)
            })
        return pd.DataFrame(colaboradores)

    def gerar_dados_recorrentes(self):
        """Gera 90 dias de registros de ponto com lógica de risco"""
        df_rh = self.gerar_colaboradores()
        base_date = datetime(2026, 1, 1)
        dates = [base_date + timedelta(days=x) for x in range(90)]
        registros_ponto = []
        
        for data in dates:
            # Maior risco em dias úteis (fadiga operacional)
            taxa_risco = 0.15 if data.weekday() < 5 else 0.05
            
            for _, funcionario in df_rh.iterrows():
                # Lógica de fadiga: Minutos de violação CLT
                if np.random.random() < taxa_risco:
                    violação = np.random.randint(30, 150)
                    # Nexo causal: 25% de chance de atestado se houver fadiga
                    atestado = 1 if np.random.random() < 0.25 else 0
                else:
                    violação = 0
                    atestado = 1 if np.random.random() < 0.02 else 0 # Ruído aleatório
                
                registros_ponto.append({
                    'Data': data,
                    'Matricula': funcionario['Matricula'],
                    'Setor': funcionario['Setor'],
                    'Violacao_Minutos': violação,
                    'Atestado': atestado
                })
        
        return pd.DataFrame(registros_ponto)

    def plotar_dashboard_90dias(self):
        """Processa os dados, gera evidência CSV e o Dashboard Visual"""
        df = self.gerar_dados_recorrentes()
        
        # 1. Gravação da Evidência de Auditoria (CSV)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f'{self.LOG_PATH}/evidencia_auditoria_{timestamp}.csv'
        df.to_csv(log_file, index=False)
        
        # 2. Preparação para os Gráficos
        df_daily = df.groupby('Data').agg({
            'Violacao_Minutos': 'sum',
            'Atestado': 'sum'
        }).reset_index()
        
        df_daily['Semana'] = df_daily['Data'].dt.isocalendar().week
        df_daily['Dia_Semana'] = df_daily['Data'].dt.day_name()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12), gridspec_kw={'height_ratios': [1, 1.2]})
        fig.patch.set_facecolor('#0d1117')

        # --- GRÁFICO 1: TENDÊNCIA DE FADIGA vs ABSENTEÍSMO ---
        ax1.plot(df_daily['Data'], df_daily['Violacao_Minutos'].rolling(7).mean(), 
                 color='#1F6FEB', lw=4, label='Índice de Fadiga (Média Móvel 7d)')
        
        ax_atestado = ax1.twinx() # Eixo secundário para atestados
        ax_atestado.bar(df_daily['Data'], df_daily['Atestado'], 
                        color='#BE123B', alpha=0.3, label='Volume de Atestados')
        
        ax1.set_title('EVIDÊNCIA DE AUDITORIA GRC: NEXO CAUSAL FADIGA vs. ATESTADOS', fontsize=18, loc='left', pad=15)
        ax1.legend(frameon=False, loc='upper left')
        ax1.grid(False)

        # --- GRÁFICO 2: MAPA DE CALOR (ONDE O CONTROLE "FURA") ---
        pivot_df = df_daily.pivot_table(index='Dia_Semana', columns='Semana', values='Violacao_Minutos', aggfunc='sum')
        dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_df = pivot_df.reindex(dias)

        sns.heatmap(pivot_df, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax2, cbar=False, linewidths=1, linecolor='#0d1117')
        ax2.set_title('MAPA DE CALOR: CONCENTRAÇÃO DE VIOLAÇÕES CLT (MINUTOS)', fontsize=18, loc='left', pad=15)
        ax2.set_ylabel('')
        ax2.set_xlabel('Semanas do Trimestre')

        plt.tight_layout()
        
        # Salva o arquivo final para o GitHub
        output_image = f'{self.ASSETS_PATH}/monitoramento_recorrente.png'
        plt.savefig(output_image, dpi=300)
        
        print("-" * 50)
        print(f"✅ SUCESSO NA EXECUÇÃO")
        print(f"📄 EVIDÊNCIA GERADA: {log_file}")
        print(f"📊 DASHBOARD ATUALIZADO: {output_image}")
        print("-" * 50)

if __name__ == "__main__":
    GRCAnalytics90Days().plotar_dashboard_90dias()