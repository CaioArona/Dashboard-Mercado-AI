🚀 Dashboard de Vagas em Inteligência Artificial

Dashboard interativo para análise do mercado de trabalho em Inteligência Artificial.

📊 Descrição do Projeto
Este dashboard foi criado com Python e Streamlit para explorar o mercado global de vagas em Inteligência Artificial.

Principais análises:

Média salarial mensal por nível de experiência 💰

Distribuição de vagas por tipo de contrato 📄

Clusterização das habilidades mais requisitadas 🛠️

Indústrias que mais contratam profissionais de IA 🏢

Filtros interativos por país 🌍

🛠️ Tecnologias Utilizadas
Python 3.10+

Streamlit

Pandas

Seaborn

Matplotlib

📁 Estrutura do Projeto
bash
Copiar
Editar
├── app.py                   # Dashboard principal
├── ai_job_data.py           # Classe de processamento dos dados
├── ai_job_visuals.py        # Classe para visualizações gráficas
├── ai_job_dataset.csv       # Base de dados utilizada
├── README.md                 # Documentação do projeto
💾 Base de Dados
Dados obtidos do Open Data Bay - AI Jobs Dataset

Contém informações sobre:

Salário anual em diferentes moedas

Nível de experiência (Trainee, Júnior, Pleno, Sênior)

Tipo de contrato (Integral, Freelancer, Temporário, Meio Período)

Skills exigidas

Indústria contratante

Trabalho remoto

🔧 Como Rodar Localmente
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/CaioArona/dashboard-vagas-ia.git
cd dashboard-vagas-ia
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o dashboard:

bash
Copiar
Editar
streamlit run app.py
✨ Funcionalidades
Gráficos dinâmicos com valores e proporções (exceto para o cluster de skills, por escolha visual)

Filtro de país interativo

Conversão automática de moedas para dólar

Análise temporal e setorial

📄 Licença
Uso livre para fins educacionais e de análise de dados.

👨‍💻 Autor
Desenvolvido por Caio Arona

GitHub

LinkedIn