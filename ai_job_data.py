import pandas as pd

class AIJobData:
    TAXAS_CONVERSAO = {
        'USD': 1.0,
        'EUR': 1.17,
        'GBP': 1.35
    }

    CLUSTERS_SKILLS = {
        'Machine Learning Frameworks': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'keras'],
        'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'mlops'],
        'Data & Analytics': ['sql', 'tableau', 'hadoop', 'spark', 'data visualization', 'mathematics', 'statistics'],
        'Programming Languages': ['java', 'scala', 'r', 'c++', 'python', 'scala'],
        'NLP & Computer Vision': ['nlp', 'computer vision', 'opencv', 'tensorflow', 'pytorch']
        
    }

    def __init__(self, caminho_csv):
        self.df = pd.read_csv(caminho_csv)
        self.preparar_dados()

    def preparar_dados(self):
        self.converte_moeda()
        self.df['salario_usd_mensal'] = self.df['salary_usd_converted'] / 12

        mapa_nivel = {'EN': 'Trainee', 'MI': 'Júnior', 'SE': 'Pleno', 'EX': 'Sênior'}
        self.df['nivel_brasil'] = self.df['experience_level'].map(mapa_nivel)

        mapa_contrato = {'FT': 'Tempo Integral', 'FL': 'Freelancer', 'CT': 'Contrato Temporário', 'PT': 'Meio Período'}
        self.df['tipo_contrato_desc'] = self.df['employment_type'].map(mapa_contrato)

        self.df['posting_date'] = pd.to_datetime(self.df['posting_date'])
        self.df['application_deadline'] = pd.to_datetime(self.df['application_deadline'])

        
        self.df['clusters_skills'] = self.df['required_skills'].apply(self.classificar_skills)

    def converte_moeda(self):
        def aplicar_conversao(row):
            taxa = self.TAXAS_CONVERSAO.get(row['salary_currency'], 1)
            return row['salary_usd'] * taxa
        self.df['salary_usd_converted'] = self.df.apply(aplicar_conversao, axis=1)

    def classificar_skills(self, skills_str):
        skills = [s.strip().lower() for s in skills_str.split(',')]
        clusters_encontrados = set()
        for cluster, keywords in self.CLUSTERS_SKILLS.items():
            for kw in keywords:
                if kw in skills:
                    clusters_encontrados.add(cluster)
        if clusters_encontrados:
            return ', '.join(sorted(clusters_encontrados))
        else:
            return 'Outros'

    def filtrar_por_pais(self, pais):
        if pais == 'Todos':
            return self.df.copy()
        else:
            return self.df[
                (self.df['company_location'] == pais) |
                (self.df['employee_residence'] == pais)
            ]
