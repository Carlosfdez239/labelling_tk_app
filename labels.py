'''
C. Fdez
26/11/2024
Rev 0

To do
    []Añadir logo Worldsensing en top
    []Añadir en banner Menú submenú para configuración impresora
    []Añadir en banner Menú submenú para configuración ruta archivos
    
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import csv  # Para trabajar con archivos CSV
import subprocess
from pylibdmtx.pylibdmtx import encode
#from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

#IMPRESORA = "Brother_QL-820NWB"
IMPRESORA ="Brother_QL-820NWB"
DIRECTORIO_LOGO = '/home/casa/Documentos/Worldsensing/Thread/Test/Thread_test/outputs/'

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

# Función para crear la etiqueta
#def Impr_Node_packaging_label(datam,Model,ERP_Code,Serial_N):
    '''
    Parámetros de este método
    datam: contenido del datamatrix, los campos deben ir separados por ;
    Model: Modelo comercial del producto
    ERP_Code: Código del ERP
    Serial_N: Número de serie del producto
    '''

    font_size = 25  # Reduce o aumenta el tamaño según sea necesario
    font_path = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    #Agregamos los imagotipos y el logo de Ws
    logo_ruta = DIRECTORIO_LOGO+"logo.png"
    #imagotipo_ruta = DIRECTORIO_LOGO+"imagotipos_nodos.png"


    #Agregamos texto
    Model = Model
    ERP_Code = ERP_Code
    Serial_N = Serial_N

    # Convertimos milímetros a píxeles (asumiendo 300 DPI)
    mm_to_px = 11.81  # factor de conversión de mm a px (300 DPI)

    # Dimensionamos la etiqueta
    label_width = int(50 * mm_to_px)  # 50 mm de longitud
    label_height = int(36 * mm_to_px)  # 36 mm de altura

    # Creamos el lienzo de la etiqueta
    label = Image.new("RGB", (label_width, label_height), "white")
    
    # Cargar e insertar la imagen .png en la etiqueta
    image_path = DIRECTORIO_LOGO+"iconos.png"
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(18 * mm_to_px), int(13 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (label_width - insert_image.width, int(16* mm_to_px)))  # Posición en la esquina superior derecha

    # Cargar e insertar el logo de Worldsensing
    image_path = logo_ruta
    insert_image = Image.open(image_path)
    insert_image = insert_image.resize((int(29 * mm_to_px), int(9 * mm_to_px)))  # Redimensionar si es necesario
    label.paste(insert_image, (0, 0))  # Posición en la esquina superior izda

    draw = ImageDraw.Draw(label)
    draw.text((2* mm_to_px, 9* mm_to_px), "Model: " + Model, font=font, fill='black')
    draw.text((2* mm_to_px, 12* mm_to_px), "ERP_Code: " + ERP_Code, font=font, fill='black')
    draw.text((2* mm_to_px, 15* mm_to_px), "Serial_Nb: " + Serial_N, font=font, fill='black')

    # Generar el código Data Matrix
    encoded = encode(datam.encode('utf8'))
    dmtx = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    dmtx.save("dmtx_debug.png")
    label.paste(dmtx,(label_width-encoded.width,int(8*mm_to_px)))
    #dmtx.show()

    label.save("output_test.png")
    #label.show()

    #contenido = datam.split(";")
    #ETIQUETA = 'etiqueta_4_' + contenido[-1] + '.png'

    # Grabamos la etiqueta    
    #label.save(ETIQUETA)


    # Mostramos en pantalla la etiqueta
    #label.show()
# Función para mostrar la etiqueta generada
def display_label():
    datam = label1_value.get() + ";" + label3_value.get() +";"+"20241022000126"
    Model = label1_value.get()
    ERP_Code = label2_value.get()
    Serial_N = label3_value.get()

    if not (Model and ERP_Code and Serial_N):
        messagebox.showwarning("Advertencia", "Faltan datos para generar la etiqueta.")
        return

    try:
        # Crear la etiqueta
        image_path = Impr_Node_packaging_label(datam, Model, ERP_Code, Serial_N)

        if not os.path.exists(image_path):
            messagebox.showerror("Error", "La imagen no se generó correctamente.")
            return

        # Cargar la imagen
        img = Image.open(image_path)

        # Mantener la relación de aspecto
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = 200
        new_height = int(new_width / aspect_ratio)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
      
        # Convertir a formato compatible con Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Mostrar en la interfaz
        label_preview.config(image=img_tk)
        label_preview.image = img_tk

        canvas = tk.Canvas(root, width=200, height=190, bg="white")
        canvas.pack()
        canvas.create_image(100, 100, image=img_tk)  # Centrar la imagen
        
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
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo imprimir la etiqueta:\n{e}")


# Crear ventana principal
root = tk.Tk()
root.title("Aplicación de búsqueda y generación de etiquetas")

# Zona superior
banner_frame = tk.Frame(root, bg="lightblue", height=50)
banner_frame.pack(side="top", fill="x")

menu_label = tk.Label(banner_frame, text="Menú", bg="lightblue", font=("Arial", 12))
menu_label.pack(side="left", padx=10)

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
filter_entry = tk.Entry(center_frame, width=100)
filter_entry.grid(row=1, column=1,padx=1, pady=5)

search_button = tk.Button(center_frame, text="Buscar", command=search_record)
search_button.grid(row=1, column=2, pady=5)

# Etiquetas para datos
label1_value = tk.StringVar(value="N/A")
label2_value = tk.StringVar(value="N/A")
label3_value = tk.StringVar(value="N/A")

tk.Label(center_frame, text="ERP:",width=25).grid(row=15, column=0, sticky="w", pady=5)
result1 = tk.Label(center_frame, textvariable=label1_value, bg="white",width=100, anchor="w",relief="sunken")
result1.grid(row=15, column=1, pady=5,padx=1)

tk.Label(center_frame, text="Model:",width=25).grid(row=17, column=0, sticky="w", pady=5)
result2 = tk.Label(center_frame, textvariable=label2_value, bg="white", width=100, anchor="w", relief="sunken")
result2.grid(row=17, column=1, pady=5,padx=1)

tk.Label(center_frame, text="Serial:",width=25).grid(row=19, column=0, sticky="w", pady=5)
result3 = tk.Label(center_frame, textvariable=label3_value, bg="white", width=100, anchor="w", relief="sunken")
result3.grid(row=19, column=1, pady=5,padx=1)

# Botones para generar y imprimir la etiqueta
btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()

generate_button = tk.Button(btn_frame, text="Generar etiqueta", command=display_label)
generate_button.pack(side="left", padx=5)

print_button = tk.Button(btn_frame, text="Imprimir etiqueta", command=print_label)
print_button.pack(side="left", padx=5)

# Vista previa de la etiqueta generada
label_preview = tk.Label(root, text="Vista previa de la etiqueta", bg="white", width=50, height=36)
#label_preview = tk.Label(center_frame, text="Vista previa de la etiqueta", bg="white", width=50, height=36)
label_preview.pack(pady=10)




# Ejecutar aplicación
root.mainloop()
