import geopandas as gpd
import requests
import json
import os

print("--- Iniciando Download do Limite de Pelotas ---")

# Endpoint oficial atualizado da Malha do IBGE para o município de Pelotas (ID 4314407)
url_ibge = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/4314407?formato=application/vnd.geo+json"

# Faz o download do GeoJSON via requests (evita erros do urllib no WSL)
response = requests.get(url_ibge)

if response.status_code == 200:
    geojson_data = response.json()
    
    # Carrega no GeoPandas a partir do dicionario GeoJSON
    pelotas = gpd.GeoDataFrame.from_features(geojson_data["features"], crs="EPSG:4674")
    
    # Reprojeta para EPSG:4326 (padrão geográfico WGS84 do MapBiomas)
    pelotas = pelotas.to_crs(epsg=4326)
    
    # Cria pasta se nao existir
    os.makedirs("dados_processados", exist_ok=True)
    
    # Salva o arquivo em GeoPackage
    output_gpkg = os.path.join("dados_processados", "pelotas_limite.gpkg")
    pelotas.to_file(output_gpkg, driver="GPKG")
    
    print(f"Sucesso! Limite vetorial salvo em: {output_gpkg}")
else:
    print(f"Erro ao acessar API do IBGE. Código HTTP: {response.status_code}")
