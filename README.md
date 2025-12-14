Reconocimiento Automático de Dados con OpenCV
Sistema de visión por computadora para detectar y contar automáticamente los puntos en dados rojos a partir de videos.
Descripción
Este proyecto procesa videos de tiradas de dados y realiza:

Detección de dados rojos mediante segmentación por color (HSV)
Identificación del momento de quietud tras el lanzamiento
Conteo automático de puntos usando detección de círculos (Hough Transform)
Generación de videos anotados con los resultados

Requisitos
bashpip install opencv-python numpy matplotlib
Estructura del Proyecto
.
├── main.py
├── tirada_1.mp4
├── tirada_2.mp4
├── tirada_3.mp4
├── tirada_4.mp4
└── salidas/
    ├── tirada_1_reconocimiento_dados.mp4
    ├── tirada_2_reconocimiento_dados.mp4
    ├── tirada_3_reconocimiento_dados.mp4
    └── tirada_4_reconocimiento_dados.mp4
Uso
Ejecución Básica
bashpython main.py
El script procesará automáticamente los 4 videos de entrada y generará las versiones anotadas en la carpeta salidas/.
Personalización
Puedes modificar parámetros clave en la función procesar_video():
pythonprocesar_video(
    path_in="tirada_1.mp4",
    path_out="salidas/resultado.mp4",
    tiempo_ignorar=1.58,  # Segundos a ignorar al inicio
    debug_visual=True      # Mostrar pasos intermedios (solo primera vez)
)
Funcionamiento
1. Segmentación por Color

Conversión a espacio HSV
Detección de tonos rojos en dos rangos:

Rango 1: H(0-10), S(50-255), V(50-255)
Rango 2: H(170-180), S(50-255), V(50-255)



2. Detección de Quietud

Compara áreas de contornos entre frames consecutivos
Umbral de diferencia: 45 píxeles²
Activa el análisis cuando los dados dejan de moverse

3. Análisis de Dados

Filtra contornos por área (4300-6400 píxeles²)
Extrae región de interés (ROI) de cada dado
Aplica transformación de Hough para detectar círculos (puntos)
Parámetros de detección:

Radio mínimo: 5 píxeles
Radio máximo: 8 píxeles
Distancia mínima entre círculos: 8 píxeles



4. Visualización

Dibuja rectángulos alrededor de cada dado
Anota el número de puntos detectados
Ordena dados de izquierda a derecha

Modo Debug Visual
En la primera ejecución, el sistema muestra visualizaciones intermedias:

Frame detectado como quieto: Momento exacto de la captura
Máscara de color: Segmentación HSV de tonos rojos
Contornos detectados: Candidatos a dados
Detalle de un dado:

Escala de grises
Desenfoque gaussiano
Detección de bordes (Canny)
Círculos detectados (puntos)



Parámetros Ajustables
Segmentación de Color
python# En extraer_dados_rojos()
rojo_1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
rojo_2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
Detección de Quietud
python# En detectar_quietud()
umbral = 45  # Diferencia máxima de área entre frames
Filtrado de Dados
python# En analizar_dados()
area_min = 4300  # Área mínima del contorno
area_max = 6400  # Área máxima del contorno
Detección de Puntos
python# En contar_puntos()
circulos = cv2.HoughCircles(
    bordes, cv2.HOUGH_GRADIENT,
    dp=1.2,           # Resolución del acumulador
    minDist=8,        # Distancia mínima entre círculos
    param1=25,        # Umbral superior para Canny
    param2=10,        # Umbral del acumulador
    minRadius=5,      # Radio mínimo
    maxRadius=8       # Radio máximo
)
Salida
El sistema imprime en consola:
Procesando: tirada_1.mp4...
[INFO] Quietud detectada en t = 2.34s
=== RESULTADO tirada_1.mp4 ===
Valores detectados: [3, 5, 2]
============================

[OK] Guardado: salidas/tirada_1_reconocimiento_dados.mp4
Limitaciones

Optimizado para dados rojos únicamente
Requiere fondo contrastante
Iluminación uniforme recomendada
Los dados deben estar completamente visibles (sin superposición)

Mejoras Futuras

 Soporte para múltiples colores de dados
 Detección con oclusión parcial
 Calibración automática de umbrales
 Interfaz gráfica (GUI)
 Exportación de resultados a JSON/CSV