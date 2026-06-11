# Meshor 3D — Real 3D Mesh Generator

🔮 Convierte imágenes 2D a modelos 3D reales directamente en tu navegador.

## Características

- **4 tipos de malla**: Personaje Inflado, Vóxeles, Mapa de Alturas, Contorno Extruido
- **Filtros de procesamiento**: Laplaciano y Bilateral (iheartmesh)
- **Visualización**: Textura, Curvatura Gaussiana/Media, Normales, Wireframe
- **Materiales PBR**: Normal Map (Sobel), Roughness Map
- **Exportación**: GLB y ZIP (OBJ + MTL + Texturas PBR)
- **100% en el navegador** — No requiere backend de IA

## Uso

1. Sube una imagen (JPG, PNG, WEBP)
2. Selecciona el tipo de malla
3. Ajusta los parámetros
4. Exporta tu modelo 3D

## Deploy en Render

Este proyecto está configurado para desplegarse automáticamente en [Render](https://render.com).

## Tecnologías

- Three.js para renderizado 3D
- Express.js para servir la aplicación
- Algoritmos de procesamiento de mallas (iheartmesh)
