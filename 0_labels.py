'''
C. Fdez
26/11/2024
Rev 0


Rev 1 --> 06/12/2024
    - archivo config.json con las configuraciones de la aplicación
    - el número de lote se construye con año,mes,dia más el código del proveedor (clave "batch": en config.json)

Rev 2 --> 07/12/2024
    - Se añade acción en el Menú impresora --> se abre una ventana emergente con la lista de las 
      impresoras instaladas en el sistema (solo Linux)
    - Se añade logo de Worldsensing
    

Rev 2.1 --> 07/12/2024
    - En la función search_record(), acondicionamos el valor del filtro si la lectura 
      se hace mediante lector de código de barras
    
Rev 2.2 --> 07/12/2024
    - Se detectan 2 Bugs, se crea area de reporting

Rev 2.3 --> 08/12/2024
    - Solucionados los 2 Bugs.

######################################################################################
To do
    [x]Añadir logo Worldsensing en el top de la app --> 08/12/2024
    [x]Añadir en banner Menú submenú para configuración impresora
        [x] Se crea un archivo json con las configuraciones necesarias --> 06/12/2024
    [x]Añadir en banner Menú submenú para configuración ruta archivos
        [x] Se traspasa a archivo config.json --> 06/12/2024
    []Añadir input con número de copias al imprimir etiquetas
    []Crear menú etiquetas Viriat

#######################################################################################

=======================================================================================
ISSUES / BUGS
    [x] Tras imprimir no se borran los contenidos de los campos
        [x]Solucionado incorporando en la función print_label() --> 08/12/2024
    [x] Si vuelves a pulsar sobre generar pierdes la imágen y ya no ves la nueva etiqueta
        [x]Solucionado cambiando la definición de label en display_label() --> 08/12/2024

=======================================================================================

Dependencias
sudo apt install python3-screeninfo para redimensionar la ventana al ancho máximo


'''
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import csv  # Para trabajar con archivos CSV
import subprocess
from pylibdmtx.pylibdmtx import encod
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import json
import datetime
from screeninfo import get_monitors



# Función para cargar la configuración
def load_config(file_path="config.json"):
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"No se encontró el archivo de configuración: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo JSON: {e}")
        return {}

# Carga la configuración
config = load_config()

# Usa los valores de configuración
IMPRESORA = config.get("IMPRESORA", "")
DIRECTORIO_LOGO = config.get("DIRECTORIO_LOGO", "")
FONT_PATH = config.get("font_path", "")
BATCH_N = config.get ("batch", "")

# Función para seleccionar un archivo
def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N):
    font_size = 30  # Tamaño de la fuente
    font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf"
    font = ImageFont.truetype(font_path, font_size)

    mm_to_px = 11.81  # Factor de conversión de mm a px (300 DPI)

    # Dimensiones de la etiqueta
    label_width = int(50 * mm_to_px)  # 50 mm de ancho
    label_height = int(45 * mm_to_px)  # 36 mm de alto

    # Crear la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    # Cargar e insertar la imagen .png en la etiqueta
    image_path = DIRECTORIO_LOGO+"iconos.png"
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(22 * mm_to_px), int(13 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (label_width - insert_image.width, int(25* mm_to_px)))  # Posición en la esquina superior derecha

    # Insertar logo
    logo_path = DIRECTORIO_LOGO + "logo.png"
    logo = Image.open(logo_path).resize((int(42 * mm_to_px), int(14 * mm_to_px)))
    label.paste(logo, (0, 0))

    # Insertar texto
    draw = ImageDraw.Draw(label)
    draw.text((2 * mm_to_px, 14 * mm_to_px), "Model: " + Model, font=font, fill="black")
    draw.text((2 * mm_to_px, 18 * mm_to_px), "ERP_Code: " + ERP_Code, font=font, fill="black")
    draw.text((2 * mm_to_px, 22 * mm_to_px), "Serial_Nb: " + Serial_N, font=font, fill="black")
    
    # Insertar código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx = dmtx.resize((int(16 * mm_to_px), int(16 * mm_to_px)))
    label.paste(dmtx, (int(34*mm_to_px), int(12 * mm_to_px)))

    # Guardar la etiqueta como archivo
    output_path = "output_test.png"
    label.save(output_path)
    return output_path

# Función para buscar un registro
def search_record():
    file_path = file_entry.get()
    filter_value = filter_entry.get()
    # Recogemos el valor del serial (segunda posición) si escaneamos con lector
    if ";" in filter_value:
        serial = filter_value.split(";")
        filter_value = serial[1]


    if not file_path:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo.")
        return
    if not filter_value:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un valor para filtrar.")
        return

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Leer los encabezados
            for row in reader:
                if filter_value in row:  # Buscar el valor en la fila
                    label1_value.set(row[5] if len(row) > 5 else "N/A")
                    texto2 = label1_value.get().replace("-", "")
                    label2_value.set(texto2)
                    #label2_value.set(row[5] if len(row) > 5 else "N/A")
                    label3_value.set(row[13] if len(row) > 4 else "N/A")
                    return
            messagebox.showinfo("Información", "Registro no encontrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al abrir el archivo:\n{e}")

# Función para crear el número de lote
def Crear_Batch():
    fecha = datetime.datetime.today().strftime("%Y%m%d")
    Batch_n = fecha + BATCH_N 
    #print (Batch_n)
    return Batch_n

# Función para mostrar la etiqueta generada
def display_label():
    Batch_n=Crear_Batch()
    #label_preview.config(image=None, text="Vista previa de la etiqueta")
    #label_preview.image = None
    datam = label1_value.get() + ";" + label3_value.get() +";"+ Batch_n
    Model = label1_value.get()
    ERP_Code = label2_value.get()
    Serial_N = label3_value.get()

    if not (Model and ERP_Code and Serial_N):
        messagebox.showwarning("Advertencia", "Faltan datos para generar la etiqueta.")
        return

    try:
        # Crear la etiqueta
        image_path = Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N)
        
        # Limpia la vista previa antes de asignar una nueva imagen
        label_preview.config(image="", text="Vista previa de la etiqueta", bg="gray",width=500,height=350)
        
        if not os.path.exists(image_path):
            messagebox.showerror("Error", "La imagen no se generó correctamente.")
            return

        # Cargar la imagen
        img = Image.open(image_path)

        # Mantener la relación de aspecto
        #original_width, original_height = img.size
        #aspect_ratio = original_width / original_height
        #new_width = 200
        #new_height = int(new_width / aspect_ratio)
        #img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Ajustar dimensiones de la imagen al widget
        widget_width = label_preview.winfo_width()
        widget_height = label_preview.winfo_height()
        img = img.resize((widget_width, widget_height), Image.Resampling.LANCZOS)
        
      
        # Convertir a formato compatible con Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Mostrar en la interfaz
        label_preview.config(image=img_tk)
        label_preview.image = img_tk

        #canvas = tk.Canvas(root, width=400, height=300, bg="white")
        #canvas.pack()
        #canvas.create_image(400, 300, image=img_tk)  # Centrar la imagen
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar o cargar la etiqueta: {e}")

# Función para imprimir la etiqueta
def print_label():
    output_path = "output_test.png"
    if not os.path.exists(output_path):
        messagebox.showwarning("Advertencia", "Primero debe generar la etiqueta.")
        return

    # Enviar el archivo a la impresora configurada
    try:
        os.system(f'lp -o orientation-requested=3 -d {IMPRESORA} {output_path}')
        messagebox.showinfo("Impresión", "La etiqueta se envió a la impresora correctamente.")
        Print = True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo imprimir la etiqueta:\n{e}")
        Print = False
    label1_value.set("N/A")
    label2_value.set("N/A")
    label3_value.set("N/A")
    filter_value.set("")
    label_preview.config(image=None, text="Vista previa de la etiqueta")
    label_preview.image = None

# Función para listar impresoras del sistema
def list_printers():
    """Obtiene la lista de impresoras del sistema."""
    printers = []
    try:
        result = subprocess.run(['lpstat', '-p'], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            printers = [line.split()[2] for line in result.stdout.splitlines() if line.startswith("la impresora")]
        else:
            printers = ["Error al ejecutar 'lpstat'."]
    except FileNotFoundError:
        printers = ["Comando 'lpstat' no disponible."]
    return printers

# Función para crear una ventana emergente y listar las impresoras
def open_printer_window():
    """Abre una ventana con la lista de impresoras."""
    win = tk.Toplevel(root)
    win.title("Lista de Impresoras")
    win.geometry("400x300")
    
    # Etiqueta de descripción
    tk.Label(win, text="Impresoras disponibles:", font=("Arial", 12)).pack(pady=10)
    
    # Obtener la lista de impresoras
    printers = list_printers()
    
    # Mostrar la lista en un Treeview
    tree = ttk.Treeview(win, columns=("Impresoras"), show="headings")
    tree.heading("Impresoras", text="Nombre de la Impresora")
    tree.column("Impresoras", anchor="center", width=350)
    tree.pack(expand=True, fill="both", pady=10, padx=10)
    
    for printer in printers:
        tree.insert("", "end", values=(printer,))
    
    # Botón para cerrar
    tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

def Viriat_label(datam, Resp, Kissflow, fecha,ubicacion):
    font_size = 30  # Tamaño de la fuente
    font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf"
    font = ImageFont.truetype(font_path, font_size)

    mm_to_px = 11.81  # Factor de conversión de mm a px (300 DPI)

    # Dimensiones de la etiqueta
    label_width = int(76 * mm_to_px)  # 76 mm de ancho
    label_height = int(50 * mm_to_px)  # 50 mm de alto

    # Crear la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    # Cargar e insertar la imagen .png en la etiqueta
    image_path = DIRECTORIO_LOGO+"iconos.png"
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(22 * mm_to_px), int(13 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (label_width - insert_image.width, int(25* mm_to_px)))  # Posición en la esquina superior derecha

    # Insertar logo
    logo_path = DIRECTORIO_LOGO + "logo.png"
    logo = Image.open(logo_path).resize((int(42 * mm_to_px), int(14 * mm_to_px)))
    label.paste(logo, (0, 0))

    # Insertar texto
    draw = ImageDraw.Draw(label)
    draw.text((2 * mm_to_px, 14 * mm_to_px), "Resp: " + Resp, font=font, fill="black")
    draw.text((2 * mm_to_px, 18 * mm_to_px), "Kissflow: " + Kissflow, font=font, fill="black")
    draw.text((2 * mm_to_px, 22 * mm_to_px), "Date: " + fecha, font=font, fill="black")
    draw.text((2 * mm_to_px, 26 * mm_to_px), "Location: " + ubicacion, font=font, fill="black")
    
    # Insertar código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx = dmtx.resize((int(16 * mm_to_px), int(16 * mm_to_px)))
    label.paste(dmtx, (int(34*mm_to_px), int(12 * mm_to_px)))

    # Guardar la etiqueta como archivo
    output_path = "Viriat_label.png"
    label.save(output_path)
    return output_path

def Get_ubicacion():
    ubicacion = input(f'scann the storage location')
    return ubicacion

# Crear ventana principal
root = tk.Tk()
root.title("Aplicación de búsqueda y generación de etiquetas")
root.tk.call('tk', 'windowingsystem') 
root.option_add('*tearOff', FALSE)

# Obtener el tamaño de la pantalla
monitor = get_monitors()[0]  # Obtiene el monitor principal
screen_width = monitor.width
screen_height = monitor.height

# Configurar la ventana al tamaño de la pantalla
root.geometry(f"{screen_width}x{screen_height}")

filter_value = tk.StringVar(value="")

# Zona superior
win = tk.Toplevel(root)
menubar = tk.Menu(win)
win['menu'] = menubar
menubar = tk.Menu(root)
menu_setup = tk.Menu(menubar)
menu_edit = tk.Menu(menubar)
menubar.add_cascade(menu=menu_setup, label='Setup')
menubar.add_cascade(menu=menu_edit, label='Edit',state='disabled')

menu_setup.add_command(label='Printer', command=open_printer_window)
menu_setup.add_separator()

menu_setup.add_command(label='Viriat', command = "")
#menu_setup.add_radiobutton(label="Opción 1",state='disabled')
#menu_setup.add_command(label='Close', state='disabled')
root['menu'] = menubar
#menu_label = tk.Label(banner_frame, text="Menú", bg="lightblue", font=("Arial", 12))
#menu_label.pack(side="left", padx=10)

# Creamos el camvas para el logo de WS
#canvas_logo = tk.Canvas(root, height=100, bg="white", highlightthickness=0)
canvas_logo = tk.Canvas(root, height=100, highlightthickness=0)
canvas_logo.pack(fill="x")

# Cargar la imagen PNG
try:
    WS_logo_path = DIRECTORIO_LOGO+"WS_logo.png"
    WS_logo_img = Image.open(WS_logo_path)

    # Redimensionar la imagen para que encaje en la cinta
    WS_logo_img = WS_logo_img.resize((230,80), Image.Resampling.LANCZOS)
    WS_logo_img_tk = ImageTk.PhotoImage(WS_logo_img)

    # Mostrar la imagen en el Canvas
    canvas_logo.create_image(10, 10, anchor="nw", image=WS_logo_img_tk)

    # Mantener una referencia de la imagen
    canvas_logo.image = WS_logo_img_tk
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# Añadir texto en el Canvas
# canvas_logo.create_text(150, 50, text="Labelling App", font=("Arial", 20), anchor="w", fill="black")

      
# Zona central
center_frame = tk.Frame(root, padx=10, pady=10)
center_frame.pack(fill="both", expand=True)


file_label = tk.Label(center_frame, text="Archivo:",width=25)
file_label.grid(row=0, column=0, sticky="w", pady=5)
file_entry = tk.Entry(center_frame, width=100)
file_entry.grid(row=0, column=1, pady=5, padx=15)
file_button = tk.Button(center_frame, text="Seleccionar archivo", command=select_file)
file_button.grid(row=0, column=2, pady=5)

filter_label = tk.Label(center_frame, text="Valor a filtrar:",width=25)
filter_label.grid(row=1, column=0, sticky="w", pady=10)
filter_entry = tk.Entry(center_frame,textvariable=filter_value, width=100)
filter_entry.grid(row=1, column=1,padx=1, pady=5)

search_button = tk.Button(center_frame, text="Buscar", command=search_record)
search_button.grid(row=1, column=2, pady=5)

# Etiquetas para datos

label1_value = tk.StringVar(value="N/A")
label2_value = tk.StringVar(value="N/A")
label3_value = tk.StringVar(value="N/A")

tk.Label(center_frame, text="ERP:",width=25).grid(row=15, column=0, sticky="w", pady=5)
result1 = tk.Label(center_frame, textvariable=label1_value,width=100, anchor="w",relief="sunken")
result1.grid(row=15, column=1, pady=5,padx=1)

tk.Label(center_frame, text="Model:",width=25).grid(row=17, column=0, sticky="w", pady=5)
result2 = tk.Label(center_frame, textvariable=label2_value, width=100, anchor="w", relief="sunken")
result2.grid(row=17, column=1, pady=5,padx=1)

tk.Label(center_frame, text="Serial:",width=25).grid(row=19, column=0, sticky="w", pady=5)
result3 = tk.Label(center_frame, textvariable=label3_value, width=100, anchor="w", relief="sunken")
result3.grid(row=19, column=1, pady=5,padx=1)

# Ubicación de los Botones
btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()
# Botones para generar la etiqueta
generate_button = tk.Button(btn_frame, text="Generar etiqueta", command=display_label)
generate_button.pack(side="left", padx=5)
# Botones para imprimir la etiqueta
print_button = tk.Button(btn_frame, text="Imprimir etiqueta", command=print_label)
print_button.pack(side="left", padx=5)

# Vista previa de la etiqueta generada
label_preview = tk.Label(root, text="Vista previa de la etiqueta", bg="white", width=50, height=36)
label_preview.pack(pady=10)

# Ejecutar aplicación
root.mainloop()
