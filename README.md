# workshop-sam

# Marketplace Vision AI: “Prueba este producto en tu espacio”

## Resumen

Construir una demo con React + TypeScript y FastAPI, desplegable localmente con Docker y públicamente. Parte de un mockup de marketplace y añade una vista de cámara PWA donde un producto del catálogo se muestra como recorte 2D transparente, movible y escalable. La segmentación se solicita automáticamente desde el backend mediante SAM 3 remoto.

## Implementación

1. Crear el repositorio con dos aplicaciones:
   - `frontend`: React, Vite, TypeScript, PWA, catálogo y cámara.
   - `backend`: FastAPI, cliente de segmentación SAM 3 y procesamiento de imágenes.
   - Docker Compose para ejecutar ambos servicios, variables de entorno de ejemplo y guía de despliegue.

2. Incorporar un catálogo semilla en JSON con 4–6 muebles y sus fotos reales, nombre, descripción, precio y categoría. El mockup consume estos datos sin requerir base de datos.

3. Adaptar el mockup a tres pantallas principales:
   - Catálogo de productos.
   - Detalle del listing con el botón “Probar en mi espacio”.
   - Vista de cámara, con el producto recortado como capa superpuesta.

4. Implementar `POST /api/products/{id}/try-on` en FastAPI:
   - Resolver el listing y descargar/leer su imagen.
   - Generar un prompt breve y específico a partir de nombre, categoría y descripción; por ejemplo, “silla de comedor de madera”.
   - Enviar imagen y prompt al adaptador remoto SAM 3.
   - Seleccionar la máscara principal con mayor puntuación; ante empates, elegir la de mayor área.
   - Aplicar la máscara como canal alfa sobre la foto original y eliminar píxeles fuera del objeto.
   - Recortar al contenido visible, conservar proporciones y retornar PNG/WebP transparente junto con dimensiones y el prompt usado.

5. Definir una interfaz `SegmentationProvider` desacoplada:
   - Entrada: bytes/URL de imagen y prompt textual.
   - Salida: una o varias máscaras binarias, puntuación y metadatos.
   - Implementación inicial: adaptador HTTP configurable mediante `SAM3_API_URL` y `SAM3_API_KEY`, dirigido al gateway remoto que el ponente deje preparado.
   - Mantener el contrato del proveedor aislado para poder sustituir el gateway sin cambiar la API ni la UI.
   - Incluir modo demo local que devuelva máscaras preprocesadas de los assets cuando no existan credenciales, para que el taller funcione aun sin acceso al servicio remoto.

6. Implementar la experiencia móvil:
   - Solicitar permisos de cámara solo al entrar en “Probar”.
   - Renderizar el stream de cámara con `getUserMedia` y dibujar el producto transparente sobre él.
   - Permitir arrastrar con un dedo y escalar/rotar con gesto de dos dedos.
   - Añadir controles alternativos accesibles para centrar, aumentar, reducir y reiniciar la posición.
   - Mantener el objeto dentro del área visible y adaptar la UI a orientación vertical.
   - Mostrar mensajes claros para permisos denegados, cámara no disponible, producto aún procesándose o segmentación fallida.

7. Convertir el frontend en PWA:
   - Manifest, iconos, HTTPS en despliegue y service worker.
   - Cachear shell de la aplicación, catálogo y assets de ejemplo.
   - Mantener la cámara y la inferencia como funciones online; informar cuando no haya conexión.

8. Añadir un efecto de grounding opcional, activable con una bandera:
   - Sombra elíptica semitransparente bajo el producto.
   - Ajustarla al ancho y escala del recorte; no intentar estimación física del suelo en el MVP.

9. Documentar el taller:
   - Diagrama del flujo: listing → prompt → SAM 3 → máscara → PNG alfa → cámara.
   - Preparación de credenciales, Docker y ejecución local.
   - Explicación del adaptador, procesamiento de máscara y puntos donde los estudiantes escriben código.
   - Guía de despliegue: frontend estático HTTPS y backend contenerizado con secretos configurados en el proveedor.
   - Licencias y procedencia de todas las fotografías del catálogo.

## Interfaces públicas

- `POST /api/products/{id}/try-on`: devuelve `{ imageUrl | imageBase64, width, height, prompt, cached }`.
- `GET /api/products`: devuelve el catálogo semilla.
- `SegmentationProvider.segment(image, prompt)`: contrato interno que devuelve máscaras candidatas y sus puntuaciones.
- Variables: `SAM3_API_URL`, `SAM3_API_KEY`, `SEGMENTATION_PROVIDER`, `DEMO_MASKS_ENABLED`, `CORS_ORIGINS`.

## Pruebas

- Backend: prompt generado desde el listing, selección de máscara, transparencia fuera de la máscara, recorte correcto, caché y errores del proveedor.
- Frontend: navegación catálogo→detalle→cámara, estados de carga/error, controles de transformación y fallback sin cámara.
- PWA: instalación, manifest válido y carga del catálogo/assets cacheados.
- Validación manual móvil: permisos de cámara, arrastre, pinza, orientación vertical y funcionamiento por HTTPS.
- Demo de taller: ejecutar una segmentación real con SAM 3 y repetirla en modo demo sin credenciales.

## Supuestos

- El mockup se entregará o integrará como capa visual de React; el alcance no incluye diseñar un marketplace completo.
- El ponente aprovisionará un gateway SAM 3 remoto compatible con el adaptador HTTP y sus credenciales.
- La versión inicial segmenta el objeto principal de una foto de producto; no maneja múltiples variantes, inventario, cuentas ni pagos.
- La visualización es 2D sobre video, no AR/WebXR ni detección real de superficies.

---

## Ejecutar la demo

1. Copia `.env.example` a `.env`. La configuración por defecto (`SEGMENTATION_PROVIDER=demo`) funciona sin credenciales y genera una máscara determinista para ensayar el flujo completo.
2. Ejecuta `docker compose up --build`.
3. Abre `http://localhost:5173` desde un navegador. Para probar la cámara desde un teléfono, publica el frontend detrás de HTTPS y actualiza `CORS_ORIGINS` con su URL.

Para desarrollo sin Docker, inicia el API con `cd backend; python -m uvicorn app.main:app --reload` y la interfaz con `cd frontend; npm install; npm run dev`.

## Flujo del taller

```text
listing → prompt breve → gateway SAM 3 → máscaras candidatas
        → selección → PNG con alfa → superposición sobre cámara
```

El código que los estudiantes pueden desarrollar de manera incremental está en:

- `backend/app/image_service.py`: generación del prompt, elección de máscara y recorte RGBA.
- `backend/app/providers.py`: contrato `SegmentationProvider` y adaptador HTTP para el gateway SAM 3.
- `frontend/src/components/TryOnCamera.tsx`: permisos de cámara, gestos y sombra opcional.

## Conectar un gateway SAM 3

Configura `SEGMENTATION_PROVIDER=sam3`, `SAM3_API_URL` y `SAM3_API_KEY`. El adaptador envía `multipart/form-data` con `image` y `prompt`. El gateway debe responder:

```json
{ "masks": [{ "png_base64": "...", "score": 0.98 }] }
```

Cada `png_base64` es una máscara PNG de un canal, alineada con la imagen de entrada. El backend escoge la mayor máscara entre las de misma puntuación, aplica el alfa y guarda el resultado en memoria para solicitudes posteriores.

## Despliegue y atribución

El frontend debe hospedarse como sitio estático con HTTPS (requisito de cámara en móvil); el contenedor de FastAPI se despliega en un servicio con `SAM3_API_KEY` como secreto. Las fotos semilla usan URLs de Unsplash únicamente como placeholders para el taller: antes de publicar, reemplázalas por fotografías propias o activos con licencia y conserva su atribución.

## Verificación

Ejecuta las pruebas del backend desde `backend` con `python -m pytest`. Comprueban la generación del prompt, el desempate de máscaras y el PNG recortado con alfa.
