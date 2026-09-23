import tkinter as tk
from tkinter import messagebox, ttk
import socket
import time
import threading
import ipaddress


# ==========================================================
# FUNCIONES
# ==========================================================

def iniciar_escaneo():
    """Valida los datos e inicia el escaneo."""

    ip = entrada_ip.get().strip()

    # Validar dirección IP
    if not ip:
        messagebox.showerror(
            "Error",
            "Debe ingresar una dirección IP."
        )
        return

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        messagebox.showerror(
            "Error",
            "La dirección IP ingresada no es válida."
        )
        return

    # Validar puertos
    try:
        puerto_inicio = int(entrada_puerto_inicial.get())
        puerto_fin = int(entrada_puerto_final.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Los puertos deben ser números enteros."
        )
        return

    # Validar rango de puertos
    if puerto_inicio < 1 or puerto_fin > 65535:
        messagebox.showerror(
            "Error",
            "Los puertos deben estar entre 1 y 65535."
        )
        return

    # Validar que el puerto inicial no sea mayor
    if puerto_inicio > puerto_fin:
        messagebox.showerror(
            "Error",
            "El puerto inicial no puede ser mayor que el puerto final."
        )
        return

    # Limpiar resultados anteriores
    cuadro_resultados.config(state="normal")
    cuadro_resultados.delete("1.0", tk.END)
    cuadro_resultados.config(state="disabled")

    etiqueta_resumen.config(
        text="Esperando resultados..."
    )

    etiqueta_estado.config(
        text="Iniciando escaneo..."
    )

    etiqueta_porcentaje.config(
        text="0%"
    )

    barra_progreso["value"] = 0

    # Desactivar botón mientras trabaja
    boton_escanear.config(state="disabled")
    boton_limpiar.config(state="disabled")

    # Ejecutar el escaneo en segundo plano
    hilo = threading.Thread(
        target=escanear_puertos,
        args=(ip, puerto_inicio, puerto_fin),
        daemon=True
    )

    hilo.start()


def escanear_puertos(ip, puerto_inicio, puerto_fin):
    """Realiza el escaneo TCP de los puertos."""

    puertos_abiertos = []

    total_puertos = puerto_fin - puerto_inicio + 1

    inicio_tiempo = time.time()

    for posicion, puerto in enumerate(
        range(puerto_inicio, puerto_fin + 1),
        start=1
    ):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # Tiempo máximo de espera
        sock.settimeout(0.1)

        try:
            resultado = sock.connect_ex(
                (ip, puerto)
            )

            # Código 0 = conexión realizada
            if resultado == 0:

                puertos_abiertos.append(
                    puerto
                )

                ventana.after(
                    0,
                    agregar_resultado,
                    puerto
                )

        except socket.error:
            pass

        finally:
            sock.close()

        # Calcular progreso
        porcentaje = (
            posicion / total_puertos
        ) * 100

        ventana.after(
            0,
            actualizar_progreso,
            porcentaje,
            puerto
        )

    # Calcular tiempo total
    tiempo_total = (
        time.time() - inicio_tiempo
    )

    ventana.after(
        0,
        mostrar_resumen,
        ip,
        puerto_inicio,
        puerto_fin,
        puertos_abiertos,
        tiempo_total
    )


def agregar_resultado(puerto):
    """Muestra los puertos abiertos encontrados."""

    cuadro_resultados.config(
        state="normal"
    )

    cuadro_resultados.insert(
        tk.END,
        f"✓  Puerto {puerto} - ABIERTO\n"
    )

    cuadro_resultados.see(
        tk.END
    )

    cuadro_resultados.config(
        state="disabled"
    )


def actualizar_progreso(porcentaje, puerto):
    """Actualiza la barra y el estado del escaneo."""

    barra_progreso["value"] = porcentaje

    etiqueta_porcentaje.config(
        text=f"{porcentaje:.0f}%"
    )

    etiqueta_estado.config(
        text=f"Escaneando puerto {puerto}..."
    )


def mostrar_resumen(
    ip,
    puerto_inicio,
    puerto_fin,
    puertos_abiertos,
    tiempo_total
):
    """Muestra el resumen final."""

    total = (
        puerto_fin - puerto_inicio + 1
    )

    # Si no se encontró ningún puerto
    if not puertos_abiertos:

        cuadro_resultados.config(
            state="normal"
        )

        cuadro_resultados.insert(
            tk.END,
            "No se encontraron puertos abiertos."
        )

        cuadro_resultados.config(
            state="disabled"
        )

        lista_abiertos = "Ninguno"

    else:

        lista_abiertos = ", ".join(
            map(str, puertos_abiertos)
        )

    # Crear resumen
    resumen = (
        f"Dirección IP: {ip}\n"
        f"Rango analizado: {puerto_inicio} - {puerto_fin}\n"
        f"Puertos escaneados: {total}\n"
        f"Puertos abiertos: {len(puertos_abiertos)}\n"
        f"Puertos encontrados: {lista_abiertos}\n"
        f"Tiempo de escaneo: {tiempo_total:.2f} segundos"
    )

    etiqueta_resumen.config(
        text=resumen
    )

    etiqueta_estado.config(
        text="✓ Escaneo finalizado"
    )

    etiqueta_porcentaje.config(
        text="100%"
    )

    barra_progreso["value"] = 100

    # Activar nuevamente los botones
    boton_escanear.config(
        state="normal"
    )

    boton_limpiar.config(
        state="normal"
    )


def limpiar():
    """Limpia todos los campos y resultados."""

    entrada_ip.delete(
        0,
        tk.END
    )

    entrada_puerto_inicial.delete(
        0,
        tk.END
    )

    entrada_puerto_final.delete(
        0,
        tk.END
    )

    cuadro_resultados.config(
        state="normal"
    )

    cuadro_resultados.delete(
        "1.0",
        tk.END
    )

    cuadro_resultados.config(
        state="disabled"
    )

    etiqueta_resumen.config(
        text="Esperando escaneo..."
    )

    etiqueta_estado.config(
        text="Listo para iniciar"
    )

    etiqueta_porcentaje.config(
        text="0%"
    )

    barra_progreso["value"] = 0

    entrada_ip.focus()


def salir():
    """Cierra la aplicación."""

    respuesta = messagebox.askyesno(
        "Salir",
        "¿Desea cerrar el Escáner de Puertos?"
    )

    if respuesta:
        ventana.destroy()


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================

ventana = tk.Tk()

ventana.title(
    "Escáner de Puertos TCP"
)

# Tamaño solicitado
ventana.geometry(
    "700x700"
)

ventana.resizable(
    False,
    False
)


# ==========================================================
# TÍTULO
# ==========================================================

titulo = tk.Label(
    ventana,
    text="ESCÁNER DE PUERTOS TCP",
    font=("Arial", 22, "bold")
)

titulo.pack(
    pady=(20, 5)
)


subtitulo = tk.Label(
    ventana,
    text="Herramienta de análisis de puertos de red",
    font=("Arial", 10)
)

subtitulo.pack(
    pady=(0, 15)
)


# ==========================================================
# DATOS DEL ESCANEO
# ==========================================================

marco_datos = tk.LabelFrame(
    ventana,
    text=" Datos del escaneo ",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=10
)

marco_datos.pack(
    padx=40,
    fill="x"
)


# Dirección IP

tk.Label(
    marco_datos,
    text="Dirección IP:"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=5
)

entrada_ip = tk.Entry(
    marco_datos,
    width=35
)

entrada_ip.grid(
    row=0,
    column=1,
    padx=15,
    pady=5
)


# Puerto inicial

tk.Label(
    marco_datos,
    text="Puerto inicial:"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=5
)

entrada_puerto_inicial = tk.Entry(
    marco_datos,
    width=35
)

entrada_puerto_inicial.grid(
    row=1,
    column=1,
    padx=15,
    pady=5
)


# Puerto final

tk.Label(
    marco_datos,
    text="Puerto final:"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=5
)

entrada_puerto_final = tk.Entry(
    marco_datos,
    width=35
)

entrada_puerto_final.grid(
    row=2,
    column=1,
    padx=15,
    pady=5
)


# ==========================================================
# BOTONES
# ==========================================================

marco_botones = tk.Frame(
    ventana
)

marco_botones.pack(
    pady=15
)


boton_escanear = tk.Button(
    marco_botones,
    text="INICIAR ESCANEO",
    command=iniciar_escaneo,
    width=18,
    height=2,
    font=("Arial", 10, "bold")
)

boton_escanear.grid(
    row=0,
    column=0,
    padx=5
)


boton_limpiar = tk.Button(
    marco_botones,
    text="LIMPIAR",
    command=limpiar,
    width=12,
    height=2
)

boton_limpiar.grid(
    row=0,
    column=1,
    padx=5
)


boton_salir = tk.Button(
    marco_botones,
    text="SALIR",
    command=salir,
    width=12,
    height=2
)

boton_salir.grid(
    row=0,
    column=2,
    padx=5
)


# ==========================================================
# PROGRESO
# ==========================================================

marco_progreso = tk.Frame(
    ventana
)

marco_progreso.pack(
    pady=(0, 10)
)


barra_progreso = ttk.Progressbar(
    marco_progreso,
    orient="horizontal",
    length=500,
    mode="determinate",
    maximum=100
)

barra_progreso.grid(
    row=0,
    column=0,
    padx=5
)


etiqueta_porcentaje = tk.Label(
    marco_progreso,
    text="0%",
    width=5
)

etiqueta_porcentaje.grid(
    row=0,
    column=1
)


etiqueta_estado = tk.Label(
    ventana,
    text="Listo para iniciar",
    font=("Arial", 10)
)

etiqueta_estado.pack(
    pady=(0, 10)
)


# ==========================================================
# RESULTADOS
# ==========================================================

marco_resultados = tk.LabelFrame(
    ventana,
    text=" Resultados ",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

marco_resultados.pack(
    padx=40,
    fill="x"
)


cuadro_resultados = tk.Text(
    marco_resultados,
    width=70,
    height=7,
    font=("Consolas", 10)
)

cuadro_resultados.pack()

cuadro_resultados.config(
    state="disabled"
)


# ==========================================================
# RESUMEN
# ==========================================================

marco_resumen = tk.LabelFrame(
    ventana,
    text=" Resumen del escaneo ",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

marco_resumen.pack(
    padx=40,
    pady=15,
    fill="both",
    expand=True
)


etiqueta_resumen = tk.Label(
    marco_resumen,
    text="Esperando escaneo...",
    justify="left",
    anchor="nw",
    font=("Arial", 10)
)

etiqueta_resumen.pack(
    anchor="w"
)


# ==========================================================
# DATOS INICIALES DE EJEMPLO
# ==========================================================

entrada_ip.insert(
    0,
    "127.0.0.1"
)

entrada_puerto_inicial.insert(
    0,
    "1"
)

entrada_puerto_final.insert(
    0,
    "100"
)


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

ventana.mainloop()