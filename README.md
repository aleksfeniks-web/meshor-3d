# Meshor 3D — Real 3D Mesh Generator & IA Reconstructor

🔮 Convierte imágenes 2D a modelos 3D reales usando un pipeline híbrido (generación geométrica local en navegador e IA generativa en la nube).

## Características

- **Motor Híbrido**:
  - ⚡ **Modo Local (Geometría)**: Personaje Redondeado (3D Inflado), Vóxeles, Mapa de Alturas, Contorno Extruido.
  - 🧠 **Modo IA Cloud (Replicate - TripoSR)**: Reconstrucción 3D completa de 360 grados usando redes neuronales.
- **Filtros de procesamiento**: Laplaciano y Bilateral (iheartmesh) aplicables a cualquier modelo.
- **Visualización**: Textura, Curvatura Gaussiana/Media, Normales, Wireframe.
- **Materiales PBR**: Normal Map (Sobel), Roughness Map.
- **Exportación**: GLB (Unity/Blender) y ZIP (OBJ + MTL + Texturas PBR).
- **Servidor Integrado**: Express con proxy local para bypass de CORS en la API de Replicate.

## Estructura del Proyecto

- `/public`: Frontend completo de la aplicación (HTML, CSS y Three.js).
- `/cog`: Configuración y script de predicción para compilar y desplegar tu propio modelo en Replicate con Cog.
- `server.js`: Servidor Express para servir los archivos estáticos y servir de proxy CORS para Replicate.

## Uso

1. Selecciona el motor de generación en el panel de control.
2. Si usas **IA Cloud**, introduce tu token de Replicate.
3. Sube una imagen (JPG, PNG, WEBP).
4. Ajusta los parámetros del modelo 3D y aplica filtros.
5. Exporta el modelo a GLB o ZIP.

## Deploy en Render

Este proyecto incluye un blueprint `render.yaml` y está listo para desplegarse automáticamente en [Render](https://render.com).

## Tecnologías

- Three.js para renderizado 3D en cliente.
- Express.js (Node.js) para servir la aplicación y proxy de red.
- TripoSR / Cog (Replicate) para reconstrucción 3D.
- Algoritmos clásicos de procesamiento de mallas (iheartmesh).
