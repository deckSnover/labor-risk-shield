import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

class GRCAnalytics90Days:
    def __init__(self):
        self.ASSETS_PATH = 'assets'
        if not os.path.exists(self.ASSETS_PATH):
            os.makedirs(self.ASSETS_PATH)
        plt.style.use('dark_background')

    def gerar_dados_recorrentes(self):
        base_date = datetime(2026, 1, 1)
        dates = [base_date + timedelta(days=x) for x in range(90)]
        violações = [np.random.randint(5, 15) if d.weekday() < 5 else np.random.randint(1, 5) for d in dates]
        atestados = [int(v * 0.4 + np.random.normal(2, 1)) for v in violações]
        return pd.DataFrame({'Data': dates, 'Violacoes': violações, 'Atestados': atestados})

    def plotar_dashboard_90dias(self):
        df = self.gerar_dados_recorrentes()
        df['Semana'] = df['Data'].dt.isocalendar().week
        df['Dia_Semana'] = df['Data'].dt.day_name()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12), gridspec_kw={'height_ratios': [1, 1.2]})
        fig.patch.set_facecolor('#0d1117')

        ax1.plot(df['Data'], df['Violacoes'].rolling(7).mean(), color='#BE123B', lw=4, label='Média Móvel Violações (Inter/Intra/HE > 2h)')
        ax1.fill_between(df['Data'], df['Violacoes'].rolling(7).mean(), color='#BE123B', alpha=0.1)
        ax1.bar(df['Data'], df['Atestados'], color='#434B56', alpha=0.5, label='Volume de Atestados')
        ax1.set_title('HISTÓRICO RECORRENTE (90 DIAS): FADIGA vs. ABSENTEÍSMO', fontsize=18, loc='left', pad=15)
        ax1.legend(frameon=False, loc='upper left')
        ax1.grid(axis='y', alpha=0.1)

        pivot_df = df.pivot_table(index='Dia_Semana', columns='Semana', values='Violacoes', aggfunc='sum')
        dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_df = pivot_df.reindex(dias)

        sns.heatmap(pivot_df, annot=True, cmap='YlOrRd', ax=ax2, cbar=False, linewidths=1, linecolor='#0d1117')
        ax2.set_title('MAPA DE CALOR (NR-1): CONCENTRAÇÃO DE VIOLAÇÕES POR DIA/SEMANA', fontsize=18, loc='left', pad=15)
        
        plt.tight_layout()
        plt.savefig(f'{self.ASSETS_PATH}/monitoramento_recorrente.png', dpi=300)
        print("📊 Dashboard de 90 dias gerado com sucesso em assets/monitoramento_recorrente.png")

if __name__ == "__main__":
    GRCAnalytics90Days().plotar_dashboard_90dias()
