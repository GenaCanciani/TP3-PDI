# 🎲 Detector de Dados en Video (OpenCV)

Este proyecto analiza videos de tiradas de dados y detecta automáticamente:

- La posición de cada dado  
- La cantidad de puntos en su cara superior  
- El instante en el que los dados quedan quietos  
- Un video de salida con anotaciones

El código utiliza **OpenCV**, **NumPy** y **Matplotlib**.

---

## 📦 Requisitos

Instalá las dependencias ejecutando:

```bash
pip install opencv-python numpy matplotlib
```

---

## 📁 Estructura esperada

El script espera encontrar los siguientes archivos de video en el mismo directorio donde está `main.py`:

```
tirada_1.mp4
tirada_2.mp4
tirada_3.mp4
tirada_4.mp4
```

Además, el script crea automáticamente la carpeta:

```
salidas/
```

Dentro se guardarán los videos procesados.

---

## ▶️ Cómo ejecutar el código

Desde la terminal, corré:

```bash
python main.py
```

Esto procesará las tiradas en orden y generará archivos como:

```
salidas/tirada_1_reconocimiento_dados.mp4
salidas/tirada_2_reconocimiento_dados.mp4
salidas/tirada_3_reconocimiento_dados.mp4
salidas/tirada_4_reconocimiento_dados.mp4
```

---

## ⚙️ Parámetros importantes del script

### `tiempo_ignorar`
Segundos iniciales donde se ignora el movimiento.  
**Valor por defecto:** `1.58` segundos.

### `debug_visual=True`
Solo aplicado al primer video. Muestra:

- Frame quieto detectado  
- Máscara de color rojo  
- Contornos  
- Pasos internos del conteo de puntos (solo para 1 dado)

Si no querés ver estos gráficos, configurá:

```python
debug_visual = False
```

---

## 🧠 ¿Cómo funciona?

### 1. Detección de rojo  
Convierte el frame a HSV y detecta zonas rojas.

### 2. Contornos  
Aplica Canny + dilatación para identificar candidatos a dados.

### 3. Quietud  
Compara el área total de contornos entre frames consecutivos.  
Si la variación es menor al umbral → **los dados están quietos**.

### 4. Conteo de puntos  
Se recorta cada dado y se detectan círculos con `HoughCircles`.

### 5. Salida  
Se dibuja un rectángulo y se etiqueta:  
`Dado N: X puntos`.# 🎲 Detector de Dados en Video (OpenCV)

Este proyecto analiza videos de tiradas de dados y detecta automáticamente:

- La posición de cada dado  
- La cantidad de puntos en su cara superior  
- El instante en el que los dados quedan quietos  
- Un video de salida con anotaciones

El código utiliza **OpenCV**, **NumPy** y **Matplotlib**.

---

## 📦 Requisitos

Instalá las dependencias ejecutando:

```bash
pip install opencv-python numpy matplotlib
```

---

## 📁 Estructura esperada

El script espera encontrar los siguientes archivos de video en el mismo directorio donde está `main.py`:

```
tirada_1.mp4
tirada_2.mp4
tirada_3.mp4
tirada_4.mp4
```

Además, el script crea automáticamente la carpeta:

```
salidas/
```

Dentro se guardarán los videos procesados.

---

## ▶️ Cómo ejecutar el código

Desde la terminal, corré:

```bash
python main.py
```

Esto procesará las tiradas en orden y generará archivos como:

```
salidas/tirada_1_reconocimiento_dados.mp4
salidas/tirada_2_reconocimiento_dados.mp4
salidas/tirada_3_reconocimiento_dados.mp4
salidas/tirada_4_reconocimiento_dados.mp4
```

---

## ⚙️ Parámetros importantes del script

### `tiempo_ignorar`
Segundos iniciales donde se ignora el movimiento.  
**Valor por defecto:** `1.58` segundos.

### `debug_visual=True`
Solo aplicado al primer video. Muestra:

- Frame quieto detectado  
- Máscara de color rojo  
- Contornos  
- Pasos internos del conteo de puntos (solo para 1 dado)

Si no querés ver estos gráficos, configurá:

```python
debug_visual = False
```

---

## 🧠 ¿Cómo funciona?

### 1. Detección de rojo  
Convierte el frame a HSV y detecta zonas rojas.

### 2. Contornos  
Aplica Canny + dilatación para identificar candidatos a dados.

### 3. Quietud  
Compara el área total de contornos entre frames consecutivos.  
Si la variación es menor al umbral → **los dados están quietos**.

### 4. Conteo de puntos  
Se recorta cada dado y se detectan círculos con `HoughCircles`.

### 5. Salida  
Se dibuja un rectángulo y se etiqueta:  
`Dado N: X puntos`.
