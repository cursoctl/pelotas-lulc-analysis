import geopandas as gpd
import rasterio
from rasterio.mask import mask
import os

# Caminhos dos ficheiros
limite_path = "dados_processados/pelotas_limite.gpkg"
raster_brasil = "dados_brutos/brazil_coverage-col11_2025.tif"
raster_out = "dados_brutos/pelotas_2025_teste.tif"

print("--- A carregar limite de Pelotas e Raster ---")
pelotas = gpd.read_file(limite_path)

with rasterio.open(raster_brasil) as src:
    # Garante que ambos estão no mesmo sistema de coordenadas (CRS)
    if pelotas.crs != src.crs:
        pelotas = pelotas.to_crs(src.crs)
        
    geometries = pelotas.geometry.values
    
    print("A recortar o raster para o limite do município...")
    out_image, out_transform = mask(src, geometries, crop=True)
    out_meta = src.meta.copy()
    
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })
    
    with rasterio.open(raster_out, "w", **out_meta) as dest:
        dest.write(out_image)

print(f"-> Recorte concluído com sucesso: {raster_out}")
