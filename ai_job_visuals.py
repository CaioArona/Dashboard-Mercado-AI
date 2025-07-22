import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

class AIJobVisualizations:
    def __init__(self, df):
        self.df = df

    def _adicionar_labels_verticais(self, barras, ax):
        total = sum(barra.get_height() for barra in barras)
        for barra in barras:
            altura = barra.get_height()
            pct = 100 * altura / total if total > 0 else 0
            xpos = barra.get_x() + barra.get_width() / 2
            ypos = altura / 2
            ax.text(xpos, ypos, f'{int(altura)}\n({pct:.1f}%)', ha='center', va='center', fontsize=9, color='white')

    def _adicionar_labels_horizontais(self, barras, ax):
        total = sum(barra.get_width() for barra in barras)
        for barra in barras:
            largura = barra.get_width()
            pct = 100 * largura / total if total > 0 else 0
            xpos = largura / 2
            ypos = barra.get_y() + barra.get_height() / 2
            ax.text(xpos, ypos, f'{int(largura)} ({pct:.1f}%)', va='center', ha='center', fontsize=9, color='white')

    def _adicionar_labels_horizontais_sem_porcentagem(self, barras, ax):
        for barra in barras:
            largura = barra.get_width()
            xpos = largura / 2
            ypos = barra.get_y() + barra.get_height() / 2
            ax.text(xpos, ypos, f'{int(largura)}', va='center', ha='center', fontsize=9, color='white')

    def _abreviar_texto(self, texto, max_len=15):
        return texto if len(texto) <= max_len else texto[:max_len-3] + '...'

    def grafico_nivel_experiencia(self, pais_nome):
        fig, ax = plt.subplots(figsize=(8,4))
        ordem = ['Trainee', 'Júnior', 'Pleno', 'Sênior']
        contagens = self.df['nivel_brasil'].value_counts().reindex(ordem)
        barras = ax.bar(contagens.index, contagens.values, color=sns.color_palette("viridis", len(contagens)))
        ax.set_title(f"Nível de Experiência ({pais_nome})")
        ax.set_ylabel("Número de vagas")
        ax.set_xlabel("Nível")
        self._adicionar_labels_verticais(barras, ax)
        return fig

    def grafico_tipo_contrato(self, pais_nome):
        fig, ax = plt.subplots(figsize=(8,4))
        contagens = self.df['tipo_contrato_desc'].value_counts()
        barras = ax.barh(contagens.index, contagens.values, height=0.5, color=sns.color_palette("coolwarm", len(contagens)))
        ax.set_title(f"Tipos de Contrato ({pais_nome})")
        ax.set_xlabel("Número de vagas")
        ax.set_ylabel("Contrato")
        self._adicionar_labels_horizontais(barras, ax)
        return fig

    def grafico_top_skills(self, pais_nome):
        fig, ax = plt.subplots(figsize=(8,4))
        skills = self.df['required_skills'].dropna().str.split(', ')
        todas_skills = [skill for sublista in skills for skill in sublista]
        contagem_skills = Counter(todas_skills)
        top_skills = contagem_skills.most_common(10)
        skills_abrev = [self._abreviar_texto(x[0], max_len=15) for x in top_skills]
        valores = [x[1] for x in top_skills]
        barras = ax.barh(skills_abrev, valores, height=0.5, color=sns.color_palette("mako", 10))
        ax.set_title(f"Top 10 Habilidades ({pais_nome})")
        ax.set_xlabel("Quantidade")
        ax.set_ylabel("Skill")
        self._adicionar_labels_horizontais(barras, ax)
        return fig

    def grafico_top_industrias(self, pais_nome):
        fig, ax = plt.subplots(figsize=(8,4))
        top_industrias = self.df['industry'].value_counts().head(10)
        industrias_abrev = [self._abreviar_texto(x, max_len=15) for x in top_industrias.index]
        barras = ax.barh(industrias_abrev, top_industrias.values, height=0.5, color=sns.color_palette("pastel", 10))
        ax.set_title(f"Top 10 Indústrias ({pais_nome})")
        ax.set_xlabel("Número de vagas")
        ax.set_ylabel("Indústria")
        self._adicionar_labels_horizontais(barras, ax)
        return fig

    def grafico_vagas_por_mes(self, pais_nome):
        df_mes = self.df.groupby(self.df['posting_date'].dt.to_period('M')).size().reset_index(name='vagas')
        df_mes['posting_date'] = df_mes['posting_date'].dt.to_timestamp()
        fig, ax = plt.subplots(figsize=(10,4))
        sns.lineplot(data=df_mes, x='posting_date', y='vagas', marker='o', ax=ax)
        ax.set_title(f"Vagas publicadas por mês ({pais_nome})")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Número de vagas")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def grafico_salario_por_industria(self, pais_nome):
        df_sal = self.df.groupby('industry')['salary_usd_converted'].mean().sort_values(ascending=False).reset_index()
        industrias_abrev = [self._abreviar_texto(x, max_len=15) for x in df_sal['industry']]
        fig, ax = plt.subplots(figsize=(10,6))
        barras = ax.barh(industrias_abrev, df_sal['salary_usd_converted'], height=0.5, color=sns.color_palette("viridis", len(df_sal)))
        ax.set_title(f"Salário médio anual por indústria ({pais_nome})")
        ax.set_xlabel("Salário médio anual (USD)")
        ax.set_ylabel("Indústria")
        self._adicionar_labels_horizontais(barras, ax)
        plt.tight_layout()
        return fig

    def grafico_skills_clusters(self, pais_nome):
        df_clusters = self.df['clusters_skills'].value_counts().reset_index()
        df_clusters.columns = ['cluster', 'qtd']
        clusters_abrev = [self._abreviar_texto(x, max_len=15) for x in df_clusters['cluster']]
        fig, ax = plt.subplots(figsize=(10,6))
        barras = ax.barh(clusters_abrev, df_clusters['qtd'], height=0.5, color=sns.color_palette("mako", len(df_clusters)))
        ax.set_title(f"Demandas por Cluster de Skills ({pais_nome})")
        ax.set_xlabel("Quantidade de vagas")
        ax.set_ylabel("Cluster de Skills")
       
        plt.tight_layout()
        return fig
