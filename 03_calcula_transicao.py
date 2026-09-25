import rasterio
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Caminhos dos ficheiros recortados
f_2010 = "dados_brutos/pelotas_2010.tif"
f_2023 = "dados_brutos/pelotas_2023.tif"

# Legenda Completa e Oficial do MapBiomas para a Região
MAPBIOMAS_CLASSES = {
    3: "Formação Florestal",
    4: "Formação Savânica",
    9: "Silvicultura",
    11: "Campo Alagável",
    12: "Formação Campestre",
    15: "Pastagem",
    19: "Lavoura Temporária",
    20: "Cana-de-Açúcar",
    21: "Mosaico de Usos",
    23: "Praia e Duna",
    24: "Infraestrutura Urbana",
    25: "Área Não Vegetada",
    33: "Corpo d'Água",
    39: "Soja",
    40: "Arroz",
    41: "Outras Lavoras",
    49: "Cultura Perene",
    50: "Restinga Florestal"
}

print("--- A carregar e cruzar os dados de 2010 e 2023 ---")

with rasterio.open(f_2010) as src10, rasterio.open(f_2023) as src23:
    arr10 = src10.read(1)
    arr23 = src23.read(1)
    
    # Tamanho do pixel em metros (30m x 30m = 900m² = 0.09 hectares)
    res_x, res_y = src10.res
    pixel_area_ha = (res_x * res_y) / 10000.0

# Aplica máscara ignorando pixels sem dados ou valor zero
mask = (arr10 > 0) & (arr23 > 0)
v10 = arr10[mask]
v23 = arr23[mask]

# 2. Criação da Matriz de Transição (em Hectares)
df = pd.DataFrame({"2010": v10, "2023": v23})
matriz_counts = pd.crosstab(df["2010"], df["2023"])

# Converte contagem de pixels para Hectares
matriz_ha = matriz_counts * pixel_area_ha

# Mapeia os códigos numéricos para os nomes das classes
matriz_ha.index = [MAPBIOMAS_CLASSES.get(c, f"Outros ({c})") for c in matriz_ha.index]
matriz_ha.columns = [MAPBIOMAS_CLASSES.get(c, f"Outros ({c})") for c in matriz_ha.columns]

# Guarda a matriz em CSV
matriz_ha.to_csv("dados_processados/matriz_transicao_pelotas_ha.csv")
print("-> Matriz guardada em: dados_processados/matriz_transicao_pelotas_ha.csv")

# 3. Gerar Heatmap para o Portfólio
plt.figure(figsize=(14, 9))
sns.heatmap(matriz_ha, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Área (Hectares)'})
plt.title("Matriz de Transição do Uso do Solo - Pelotas/RS (2010 vs 2023)", fontsize=14, fontweight='bold')
plt.xlabel("Classe em 2023", fontsize=12)
plt.ylabel("Classe em 2010", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

# Guarda o gráfico em alta resolução
plt.savefig("dados_processados/matriz_transicao_pelotas.png", dpi=300)
print("-> Gráfico atualizado guardado em: dados_processados/matriz_transicao_pelotas.png")
print("--- Análise concluída com sucesso! ---")
