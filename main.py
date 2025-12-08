import cv2
import numpy as np
import matplotlib.pyplot as plt
import os  # Importamos os para gestionar carpetas

# Herramienta para visualizar pasos intermedios
def mostrar(img, titulo="", cmap="gray"):
    plt.figure()
    plt.imshow(img, cmap=cmap)
    plt.title(titulo)
    plt.axis("off")
    plt.show()


# Aislar tonos rojos
def extraer_dados_rojos(frame_bgr):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Dos bandas para cubrir el rango del rojo
    rojo_1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    rojo_2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))

    mascara = cv2.bitwise_or(rojo_1, rojo_2)
    return mascara


# Contornos a partir de la máscara 
def obtener_contornos(frame):
    mascara = extraer_dados_rojos(frame)
    bordes = cv2.Canny(mascara, 1000, 1500)
    bordes = cv2.dilate(bordes, None, iterations=2)
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contornos


# Detectar área sin movimiento
def detectar_quietud(cont_previos, cont_actuales, umbral=45):
    area_prev = sum(cv2.contourArea(c) for c in cont_previos)
    area_act = sum(cv2.contourArea(c) for c in cont_actuales)
    return abs(area_prev - area_act) < umbral


# Conteo de puntos
def contar_puntos(recorte, ver_pasos=False):
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    
    if ver_pasos: mostrar(gris, "Escala de grises (Detalle Dado)")

    suav = cv2.GaussianBlur(gris, (9, 9), 3)
    if ver_pasos: mostrar(suav, "Desenfoque (Detalle Dado)")

    bordes = cv2.Canny(suav, 30, 150)
    if ver_pasos: mostrar(bordes, "Canny (Detalle Dado)")

    circulos = cv2.HoughCircles(
        bordes, cv2.HOUGH_GRADIENT,
        dp=1.2, minDist=8,
        param1=25, param2=10,
        minRadius=5, maxRadius=8
    )

    cant_puntos = 0
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        cant_puntos = len(circulos[0])
        # Dibujamos solo para mostrar, si se requiere
        if ver_pasos:
            img_debug = recorte.copy()
            for c in circulos[0]:
                cv2.circle(img_debug, (c[0], c[1]), c[2], (0, 255, 0), 2)
            mostrar(img_debug, f"Puntos detectados: {cant_puntos}")
            
    return cant_puntos


# Recorte de candidatos y analisis de cada dado
def analizar_dados(frame, contornos, area_min=4300, area_max=6400, ver_detalle_uno=False):
    datos = []
    
    # Flag interno para asegurar que solo mostramos el primer dado encontrado
    ya_mostre_un_dado = False 

    for c in contornos:
        a = cv2.contourArea(c)
        if area_min <= a <= area_max:
            x, y, w, h = cv2.boundingRect(c)
            rec = frame[y:y+h, x:x+w]

            # Solo mostramos los pasos internos si:
            # 1. Nos lo pidieron (ver_detalle_uno=True)
            # 2. Aún no hemos mostrado ninguno en esta tanda (not ya_mostre_un_dado)
            mostrar_este = False
            if ver_detalle_uno and not ya_mostre_un_dado:
                mostrar_este = True
                ya_mostre_un_dado = True # Bloqueamos para los siguientes dados

            puntos = contar_puntos(rec, ver_pasos=mostrar_este)
            datos.append((x, y, w, h, puntos))

            if mostrar_este:
                print(f"[DEBUG VISUAL] Dado analizado en detalle. Puntos: {puntos}")

    # Ordenar de izquierda a derecha
    datos.sort(key=lambda r: r[0])
    return datos


# Anotar resultados en el frame
def dibujar_anotaciones(frame, info_dados):
    for idx, (x, y, w, h, pts) in enumerate(info_dados):
        etiqueta = f"Dado {idx+1}: {pts}"
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.putText(
            frame, etiqueta,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (255, 0, 0),
            2, cv2.LINE_AA
        )
    return frame


# Procesado
def procesar_video(path_in, path_out, tiempo_ignorar=1.58, debug_visual=False):

    cap = cv2.VideoCapture(path_in)
    if not cap.isOpened():
        print(f"Error al abrir video {path_in}.")
        return

    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(
        path_out,
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS, (W, H)
    )

    frame_previo = None
    quietos = False
    info_dados = []

    print(f"Procesando: {path_in}...")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        tiempo_actual = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        if tiempo_actual < tiempo_ignorar:
            frame_previo = frame.copy()
            out.write(frame)
            continue

        if frame_previo is not None and not quietos:
            cont_prev = obtener_contornos(frame_previo)
            cont_act  = obtener_contornos(frame)

            if detectar_quietud(cont_prev, cont_act):
                print(f"[INFO] Quietud detectada en t = {tiempo_actual:.2f}s")

                # --- BLOQUE VISUALIZACIÓN GENERAL ---
                if debug_visual:
                    # 1. Mostrar Frame Quieto
                    mostrar(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), "1. Frame Detectado como Quieto")
                    
                    # 2. Mostrar Máscara Roja
                    mask = extraer_dados_rojos(frame)
                    mostrar(mask, "2. Máscara de Color (Segmentación)")

                    # 3. Mostrar Contornos Generales
                    frame_cnt = frame.copy()
                    cv2.drawContours(frame_cnt, cont_act, -1, (0,255,0), 2)
                    mostrar(cv2.cvtColor(frame_cnt, cv2.COLOR_BGR2RGB), "3. Contornos Detectados")
                    
                    print("--> Mostrando detalle interno de UN SOLO DADO...")

                # Llamamos al análisis
                info_dados = analizar_dados(frame, cont_act, ver_detalle_uno=debug_visual)

                valores = [d[4] for d in info_dados]
                print(f"=== RESULTADO {path_in} ===")
                print("Valores detectados:", valores)
                print("============================\n")

                debug_visual = False 
                quietos = True

        if quietos:
            frame = dibujar_anotaciones(frame, info_dados)

        out.write(frame)
        frame_previo = frame.copy()

    cap.release()
    out.release()
    print(f"[OK] Guardado: {path_out}")


# Ejecución

# Crear carpeta de salidas si no existe
if not os.path.exists("salidas"):
    os.makedirs("salidas")

# Variable de control: Solo queremos ver gráficos la PRIMERA vez
mostrar_ejemplo = True

for n in [1, 2, 3, 4]:
    # Definir ruta de salida dentro de la carpeta 'salidas'
    ruta_salida = f"salidas/tirada_{n}_reconocimiento_dados.mp4"
    
    procesar_video(
        f"tirada_{n}.mp4",
        ruta_salida,
        debug_visual=mostrar_ejemplo
    )
    
    # Después del primer video, desactivamos los gráficos para el resto
    if mostrar_ejemplo:
        mostrar_ejemplo = False