import geopandas as gpd
import ee
import geemap
import os

print("--- Inicializando Google Earth Engine ---")
# Inicializa passando o ID do seu projeto Cloud ativo
ee.Initialize(project='global-standard-431317-t5')

# 1. Carrega o limite vetorial de Pelotas criado no passo 01
gdf_pelotas = gpd.read_file("dados_processados/pelotas_limite.gpkg")

# Converte o limite de Pelotas para um objeto de geometria do Earth Engine
bounds = geemap.gdf_to_ee(gdf_pelotas).geometry()

# 2. Carrega a coleção do MapBiomas Brasil (Coleção 9 / 30m)
mapbiomas_asset = "projects/mapbiomas-workspace/public/initiative/mapbiomas/collection9/coverage/brazil"
mapbiomas_img = ee.Image(mapbiomas_asset)

# Garantir pasta de destino
os.makedirs("dados_brutos", exist_ok=True)

anos = [2010, 2023]

for ano in anos:
    print(f"Baixando e recortando o ano {ano} para Pelotas...")
    
    # Seleciona a banda do ano correspondente
    raster_ano = mapbiomas_img.select(f"classification_{ano}").clip(bounds)
    
    output_tif = f"dados_brutos/pelotas_{ano}.tif"
    
    # Exporta localmente como GeoTIFF
    geemap.ee_export_image(
        raster_ano,
        filename=output_tif,
        scale=30,  # Resolução espacial nativa de 30 metros
        region=bounds,
        file_per_band=False
    )
    print(f"-> Salvo em: {output_tif}")

print("--- Download Concluído com Sucesso! ---")
