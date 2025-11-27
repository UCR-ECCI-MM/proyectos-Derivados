# Proyecto 2

Este proyecto implementa un sistema de análisis de **Simulated Annealing (SA)**, **Tabu Search (TS)** y **Genetic Algorithm (GA)** para abordar un problema de **selección óptima de manifestaciones geotérmicas**.  

El objetivo central es identificar subconjuntos de manifestaciones con **máximo potencial energético o de uso directo**, utilizando datos **térmicos, geoquímicos y espaciales**.  

---

## Requisitos

Instalar dependencias necesarias:

```bash
pip install matplotlib
```
## Cómo ejecutar

Para correr el proyecto, usa el siguiente comando desde la carpeta src:

```bash
python main.py
```

## Dataset

El programa utiliza un archivo CSV ubicado en:

``
dataset/dataset_300.csv
``


Este archivo contiene las manifestaciones geotérmicas con sus propiedades medidas en campo.  
Las columnas esperadas son:

- `id`  
- `coord_x`, `coord_y` (coordenadas espaciales)  
- `temp` (temperatura)  
- `cond` (conductividad)  
- `Cl`, `Ca`, `Si`, `Na`, `K` (iones geoquímicos)

Asegúrate de que el archivo exista y mantenga esta estructura para que el programa pueda procesarlo correctamente.
