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

Rev 2.4 --> 27/02/2025
    - Ajustamos la interface para que muestre la etiqueta en pantalla y directamente podamos imprimir

######################################################################################
To do
    [x]Añadir logo Worldsensing en el top de la app --> 08/12/2024
    [x]Añadir en banner Menú submenú para configuración impresora
        [x] Se crea un archivo json con las configuraciones necesarias --> 06/12/2024
    [x]Añadir en banner Menú submenú para configuración ruta archivos
        [x] Se traspasa a archivo config.json --> 06/12/2024
    []Añadir input con número de copias al imprimir etiquetas

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
sudo apt-get install libdmtx0b
pip install pylibdmtx
pip install openpyxl


'''
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import csv  # Para trabajar con archivos CSV
import openpyxl # type: ignore
import subprocess
from pylibdmtx.pylibdmtx import encode
#from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageTk as IMG
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
#RUBIK_FONT_PATH = config.get("Rubik_font_path","")
RUBIK_FONT_PATH = "/usr/share/fonts/truetype/Rubik/Rubik-Light.ttf"
BATCH_N = config.get ("batch", "")

# Función para seleccionar un archivo
def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"),("Archivos xlsx", "*.xlsx"))
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N):
    font_size = 28  # Tamaño de la fuente
    ##font_path = "/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf"
    font_path = RUBIK_FONT_PATH
    print(f"directorio y fuente cargada --> {font_path}")
    fuente = ImageFont.truetype(font_path, font_size)
    print(f'valor de font --> {fuente}')

    mm_to_px = 11.81  # Factor de conversión de mm a px (300 DPI)

    # Dimensiones de la etiqueta
    label_width = int(50 * mm_to_px)  # 50 mm de ancho
    label_height = int(45 * mm_to_px)  # 36 mm de alto

    # Crear la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    # Cargar e insertar la imagen .png en la etiqueta
    image_path = DIRECTORIO_LOGO+"iconos.png"
    print(f'directorio --> {image_path}')
    insert_image = Image.open(image_path)
    #insert_image = insert_image.resize((int(22 * mm_to_px), int(13 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (label_width - insert_image.width, int(25* mm_to_px)))  # Posición en la esquina superior derecha
###    
    insert_image.close()
    # Insertar logo
    ##logo_path = DIRECTORIO_LOGO + "logo.png"
    logo_path = "/home/ws-prod23/Documentos/labelling_tk_app/images/W_Label_Devices.png"
    print(f'Imagen logo --> {logo_path}')
    logo = Image.open(logo_path,"r").resize((int(42 * mm_to_px), int(8 * mm_to_px)))
    label.paste(logo, (0, 0))

    # Insertar texto
    draw = ImageDraw.Draw(label)
    print(f'creado draw --> {draw}')
    draw.text((2 * mm_to_px, 8 * mm_to_px), "Viriat 47, 10th Floor, 08014 Barcelona, Spain",font_size=22 ,  fill='black')
    print(f'creado el texto de la dirección de viriat')
    draw.text((2 * mm_to_px, 14 * mm_to_px), "Model:  " + Model, font_size=28, fill="black")
    print(f'creado el texto para el Model')
    draw.text((2 * mm_to_px, 18 * mm_to_px), "ERP Code:  " + ERP_Code,font_size=28,  fill="black")
    print(f'creado el texto para el ERP')
    draw.text((2 * mm_to_px, 22 * mm_to_px), "Serial Nb:  " + Serial_N, font_size=28, fill="black")
    print(f'creado el texto para el Serial')
    print(f'creados los textos en la etiqueta')
    # Insertar código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx = dmtx.resize((int(16 * mm_to_px), int(16 * mm_to_px)))
    label.paste(dmtx, (int(34*mm_to_px), int(12 * mm_to_px)))
    print(f'creado el datamatrix en la etiqueta')
    
    # Guardar la etiqueta como archivo
    output_path = os.path.expanduser("~/Documentos/labelling_tk_app/output_test2.png")
    print(f'ruta donde guardaremos la etiqueta --> {output_path}')
    label.save(output_path)
    print(f'etiqueta guardada')
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
        
        reader = openpyxl.load_workbook(file_path)
        hoja = reader.active
        for fila in hoja.iter_rows(values_only = True):
            #print(f'fila leida --> {fila}')
            if filter_value in fila:  # Buscar el valor en la fila
                
                label1_value.set(fila[5] if len(fila) > 5 else "N/A")
                texto2 = label1_value.get().replace("-", "")
                label2_value.set(texto2)               
                label3_value.set(fila[13] if len(fila) > 4 else "N/A")
                return
             
            #messagebox.showinfo("Información", "Registro no encontrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al abrir el archivo:\n{e}")

# Función para crear el número de lote
def Crear_Batch():
    fecha = datetime.datetime.today().strftime("%Y%m%d")
    Batch_n = fecha + BATCH_N 
    #print (Batch_n)
    return Batch_n

# Función para mostrar la etiqueta generada
#def display_label():
#    Batch_n=Crear_Batch()
    #label_preview.config(image=None, text="Vista previa de la etiqueta")
    #label_preview.image = None
#    datam = label1_value.get() + ";" + label3_value.get() +";"+ Batch_n
#    Model = label1_value.get()
#    ERP_Code = label2_value.get()
#    Serial_N = label3_value.get()

#    if not (Model and ERP_Code and Serial_N):
#        messagebox.showwarning("Advertencia", "Faltan datos para generar la etiqueta.")
#        return

#    try:
#        # Crear la etiqueta
#        image_path = Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N)
#        # Verificar que la imagen se generó correctamente antes de usarla
#        if not os.path.exists(image_path):
#            messagebox.showerror("Error", "La imagen no se generó correctamente.")
#            return
#        template = os.path.expanduser("~/Documentos/labelling_tk_app/output_test2.png")
#        imagen = Image.open(fp=template)
#        imagen.show() 

#        foto = tk.PhotoImage(file= template)
#        imagen = Image.open(fp=template,mode="r")
#        foto = IMG.PhotoImage(imagen)  
#        label_preview.config(height=450, width=650)
#        #label_preview['image']= foto
#        label_preview.image= foto
#        if not os.path.exists(image_path):
#            messagebox.showerror("Error", "La imagen no se generó correctamente.")
#            return
#    except Exception as e:
#        messagebox.showerror("Error", f"Error al generar o cargar la etiqueta: {e}")

def display_label():
    print(f'Entrando en display label')
    try:
        print(f'Entrando en el Try')
        Batch_n = Crear_Batch()
        print(f'Datos del lote --> {Batch_n}')
        datam = label1_value.get() + ";" + label3_value.get() + ";" + Batch_n
        print(f'Datos del Datamatrix --> {datam}')
        Model = label1_value.get()
        ERP_Code = label2_value.get()
        Serial_N = label3_value.get()

        if not (Model and ERP_Code and Serial_N):
            messagebox.showwarning("Advertencia", "Faltan datos para generar la etiqueta.")
            return

        # Crear la etiqueta y verificar si la imagen existe
        image_path = Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N)
        print (f'Datos en la etiqueta --> {image_path}')
        if not os.path.exists(image_path):
            messagebox.showerror("Error", "La imagen no se generó correctamente.")
            return

        # Asegurar que la imagen sea accesible
        template = os.path.expanduser("~/Documentos/labelling_tk_app/output_test2.png")
        print(template)

        # Cargar la imagen correctamente
        imagen = Image.open(template)
        imagen.show()
        foto = IMG.PhotoImage(imagen)  # Usar ImageTk para compatibilidad con tkinter
        
        label_preview.config(height=450, width=650)
        #label_preview.image = foto  # Guardar referencia para evitar recolección de basura
        label_preview.config(image=foto)

        # Mostrar la imagen en visor externo (opcional)
        #imagen.show()

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar o cargar la etiqueta: {e}")
    


# Función para imprimir la etiqueta
def print_label():
    output_path = os.path.expanduser("~/Documentos/labelling_tk_app/output_test2.png")
    imagen = Image.open(fp=output_path, mode="r")
    imagen.show()
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

# *******************************************************************************
# Crear ventana principal
# *******************************************************************************

root = tk.Tk()
root.title("Aplicación de búsqueda y generación de etiquetas")
root.tk.call('tk', 'windowingsystem') 
root.option_add('*tearOff', FALSE)

# Obtener el tamaño de la pantalla
monitor = get_monitors()[0]  # Obtiene el monitor principal
screen_width = monitor.width
screen_height = monitor.height

# *******************************************************************************
# Configurar la ventana al tamaño de la pantalla
# *******************************************************************************

root.geometry(f"{screen_width}x{screen_height}")
filter_value = tk.StringVar(value="")

# *******************************************************************************
# Zona superior
# *******************************************************************************

#win = tk.Toplevel(root)
#menubar = tk.Menu(win)
#win['menu'] = menubar
menubar = tk.Menu(root)
menu_setup = tk.Menu(menubar)
menu_edit = tk.Menu(menubar)
menubar.add_cascade(menu=menu_setup, label='Setup')
menubar.add_cascade(menu=menu_edit, label='Edit',state='disabled')

menu_setup.add_command(label='Printer', command=open_printer_window)
menu_setup.add_separator()

root['menu'] = menubar

# *******************************************************************************
# Cargar el logo de Worldsensing
# *******************************************************************************

canvas_logo = tk.Canvas(root, height=100, highlightthickness=0)
canvas_logo.pack(fill="x")
try:
    WS_logo_path = DIRECTORIO_LOGO+"WS_logo.png"
    WS_logo_img= PhotoImage(file=WS_logo_path)
    print(f'WS_logo_img tiene un tamaño de --> {WS_logo_img}')

    # Mostrar la imagen en el Canvas
    canvas_logo.create_image(10, 10, anchor="nw", image=WS_logo_img)
    
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# *******************************************************************************     
# Zona central
# *******************************************************************************

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

# *******************************************************************************
# Etiquetas para datos
# *******************************************************************************

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

# *******************************************************************************
# Ubicación de los Botones
# *******************************************************************************

btn_frame = tk.Frame(root ,pady=10)
btn_frame.pack()
# Botones para generar la etiqueta
generate_button = tk.Button(btn_frame, text="Generar etiqueta", command=display_label)
generate_button.pack(side="left", padx=5)
# Botones para imprimir la etiqueta
print_button = tk.Button(btn_frame, text="Imprimir etiqueta", command=print_label)
print_button.pack(side="left", padx=5)

# Vista previa de la etiqueta generada
label_preview = tk.Label(root, text="Vista previa de la etiqueta", bg="white", width=150, height=36)
label_preview.pack(pady=10)


# Ejecutar aplicación
root.mainloop()
