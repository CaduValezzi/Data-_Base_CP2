import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def analyze_dataframe(df):
    # Análise descritiva
    desc = df.describe()

    # Gráfico de correlação
    corr = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Gráfico de Correlações')
    plt.savefig('correlation.png')
    plt.close()

    # Regressão linear entre as colunas (exemplo)
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            for col2 in df.columns:
                if col != col2 and df[col2].dtype in ['int64', 'float64']:
                    plt.figure(figsize=(8, 6))
                    sns.regplot(x=df[col], y=df[col2])
                    plt.title(f'Regressão Linear entre {col} e {col2}')
                    plt.savefig(f'{col}_vs_{col2}.png')
                    plt.close()
    
    # Histogramas e distribuições
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            plt.figure(figsize=(8, 6))
            sns.histplot(df[col], kde=True)
            plt.title(f'Histograma de {col}')
            plt.savefig(f'hist_{col}.png')
            plt.close()

    # Criação do HTML
    html_content = f"""
    <html>
    <head>
        <title>Análise Automatizada</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5">Análise Descritiva</h1>
            <pre>{desc.to_html()}</pre>
            <h2 class="mt-5">Gráfico de Correlações</h2>
            <img src="data:image/png;base64,{convert_image_to_base64('correlation.png')}" alt="Correlation Graph">
            <h2 class="mt-5">Regressões Lineares</h2>
    """
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            for col2 in df.columns:
                if col != col2 and df[col2].dtype in ['int64', 'float64']:
                    html_content += f'<h3>{col} vs {col2}</h3>'
                    html_content += f'<img src="data:image/png;base64,{convert_image_to_base64(f"{col}_vs_{col2}.png")}" alt="Regression {col} vs {col2}">'
    
    html_content += """
            <h2 class="mt-5">Histogramas e Distribuições</h2>
    """
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            html_content += f'<h3>{col}</h3>'
            html_content += f'<img src="data:image/png;base64,{convert_image_to_base64(f"hist_{col}.png")}" alt="Histogram {col}">'
    
    html_content += """
        </div>
    </body>
    </html>
    """
    with open("analysis.html", "w") as file:
        file.write(html_content)

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Exemplo de uso
df = pd.read_csv('seu_arquivo.csv')
analyze_dataframe(df)
