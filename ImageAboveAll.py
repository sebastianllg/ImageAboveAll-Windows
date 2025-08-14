import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ctypes import windll

# --- Configuración de tu información ---
INFO_TEXTO = """***IMAGE ABOVE ALL***

sebastianllg
WhatsApp: +593 984548191
email: sebastianllg@gmail.com
Paypal Donations: @sebastianllerena1
"""

# --- Constantes Windows ---
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x20
WS_EX_LAYERED = 0x80000

original_styles = None

def make_window_clickthrough(hwnd):
    styles = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT)

def make_window_clickable(hwnd):
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, original_styles)

# --- Ventana principal de la imagen ---
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.attributes('-transparentcolor', 'pink')
root.configure(bg='pink')

img_original = None
scale_factor = [1.0]
opacity = [0.8]
clickthrough_enabled = [False]
photo = None

label = tk.Label(root, bg='pink')
label.pack()

# --- Selección de imagen ---
def seleccionar_imagen():
    global img_original
    file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img_original = Image.open(file_path)
        update_image()

def update_image():
    global photo
    if img_original:
        new_width = int(img_original.width * scale_factor[0])
        new_height = int(img_original.height * scale_factor[0])
        img_resized = img_original.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        label.config(image=photo)
        root.geometry(f"{new_width}x{new_height}")

seleccionar_imagen()
if img_original is None:
    root.destroy()
    exit()

root.update_idletasks()
hwnd = windll.user32.GetParent(root.winfo_id())
original_styles = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

# --- Funciones del panel ---
def toggle_clickthrough():
    clickthrough_enabled[0] = not clickthrough_enabled[0]
    if clickthrough_enabled[0]:
        make_window_clickthrough(hwnd)
        btn_click.config(text="Click-Through: ON", bg="lightgreen")
    else:
        make_window_clickable(hwnd)
        btn_click.config(text="Click-Through: OFF", bg="lightcoral")

def set_opacity(val):
    opacity[0] = float(val)
    root.attributes('-alpha', opacity[0])

def set_size(val):
    scale_factor[0] = float(val)
    update_image()

def mostrar_informacion():
    messagebox.showinfo("About", INFO_TEXTO)

def cerrar_todo():
    try:
        root.destroy()
    except:
        pass
    try:
        control_win.destroy()
    except:
        pass

# --- Panel de Control ---
control_win = tk.Toplevel()
control_win.title("Image Above All")
control_win.attributes('-topmost', True)
control_win.geometry("250x340")

# Mantener siempre arriba
def mantener_arriba():
    control_win.attributes('-topmost', True)
    control_win.after(1000, mantener_arriba)
mantener_arriba()

# Asignamos el cierre de todo al cerrar el panel
control_win.protocol("WM_DELETE_WINDOW", cerrar_todo)

btn_click = tk.Button(control_win, text="Click-Through: OFF", bg="lightcoral", command=toggle_clickthrough)
btn_click.pack(fill="x", pady=5)

tk.Button(control_win, text="Change image", bg="lightblue", command=seleccionar_imagen).pack(fill="x", pady=5)

tk.Label(control_win, text="Transparency").pack()
slider_opacity = tk.Scale(control_win, from_=0.1, to=1.0, resolution=0.05, orient="horizontal", command=set_opacity)
slider_opacity.set(opacity[0])
slider_opacity.pack(fill="x", pady=5)

tk.Label(control_win, text="Size").pack()
slider_size = tk.Scale(control_win, from_=0.1, to=10.0, resolution=0.1, orient="horizontal", command=set_size)
slider_size.set(scale_factor[0])
slider_size.pack(fill="x", pady=5)

tk.Button(control_win, text="About", bg="lightyellow", command=mostrar_informacion).pack(fill="x", pady=5)
tk.Button(control_win, text="Exit", command=cerrar_todo).pack(fill="x", pady=2)

# --- Movimiento de la imagen ---
offset_x = offset_y = 0
def start_move(event):
    global offset_x, offset_y
    if not clickthrough_enabled[0]:
        offset_x = event.x
        offset_y = event.y

def do_move(event):
    if not clickthrough_enabled[0]:
        x = event.x_root - offset_x
        y = event.y_root - offset_y
        root.geometry(f'+{x}+{y}')

label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", do_move)
label.bind("<Double-Button-1>", lambda e: root.destroy())

root.mainloop()
