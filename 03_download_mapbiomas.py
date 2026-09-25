import geopandas as gpd
import rasterio
from rasterio.mask import mask
import requests
import os

print("--- Iniciando Download Direto dos Rasters do MapBiomas ---")

# 1. Carregar o limite vetorial de Pelotas
gdf = gpd.read_file("dados_processados/pelotas_limite.gpkg")

# Garantir que o diretório de destino existe
os.makedirs("dados_brutos", exist_ok=True)

# Coordenadas do Bounding Box de Pelotas
minx, miny, maxx, maxy = gdf.total_bounds

# Anos desejados para a análise de transição
anos = [2010, 2023]

# Loop para baixar o mapa do RS / Brasil ou extrair recorte
for ano in anos:
    print(f"Baixando e recortando dado do MapBiomas para o ano {ano}...")
    
    # URL do raster do MapBiomas Brasil (Coleção 9 / AEZ ou Geral)
    # Baixando arquivo GeoTIFF do estado ou via Web Service do MapBiomas
    url = f"https://storage.googleapis.com/mapbiomas-public/initiative/mapbiomas/collection_9/coverage/mapbiomas_coverage_collection90_{ano}.tif"
    
    output_path = f"dados_brutos/pelotas_{ano}.tif"
    
    try:
        # Abre o raster direto da nuvem via Rasterio (VSICURL)
        with rasterio.open(f"/vsicurl/{url}") as src:
            # Rejeta para o CRS do raster
            gdf_projected = gdf.to_crs(src.crs)
            shapes = [geom for geom in gdf_projected.geometry]
            
            # Recorta a imagem para o contorno exato de Pelotas
            out_image, out_transform = mask(src, shapes, crop=True)
            out_meta = src.meta.copy()
            
            # Atualiza metadados para a nova dimensão recortada
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })
            
            # Salva o arquivo final recortado
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)
                
        print(f"-> Pelotas {ano} salvo com sucesso em: {output_path}")
        
    except Exception as e:
        print(f"Erro ao processar ano {ano}: {e}")

print("--- Processamento Concluído! ---")
