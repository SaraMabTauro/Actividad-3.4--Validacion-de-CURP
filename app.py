
import tkinter as tk
from tkinter import messagebox, ttk
import random
import re
from datetime import datetime
from typing import List

class EstadoMaquinaTuring:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.transiciones = []
    
    def agregar_transicion(self, simbolo_actual: str, nuevo_simbolo: str, direccion: str, siguiente_estado: str):
        movimiento = 1 if direccion == 'R' else -1
        self.transiciones.append((simbolo_actual, nuevo_simbolo, direccion, movimiento, siguiente_estado))

class MaquinaDeTuring:
    def __init__(self):
        self.estado_actual = 'q0'
        self.cinta = []
        self.posicion = 0
        self.estados = self.inicializar_estados()

    def inicializar_estados(self):
        estados = {}
        estados['q0'] = EstadoMaquinaTuring('q0')
        estados['q0'].agregar_transicion('[A-Z]', '*', 'R', 'q1')
        estados['q1'] = EstadoMaquinaTuring('q1')
        estados['q1'].agregar_transicion('[AEIOU]', '*', 'R', 'qAceptar')
        return estados

    def validar_curp(self, curp: str) -> bool:
        if not curp or len(curp) != 18:
            return False
        patron = r'^[A-Z]{4}\d{6}[HM][A-Z]{2}[BCDFGHJKLMNPQRSTVWXYZ]{3}[0-9A-Z]\d$'
        if not re.match(patron, curp):
            return False
        try:
            fecha = datetime.strptime(curp[4:10], '%y%m%d')
            if fecha > datetime.now():
                return False
        except ValueError:
            return False
        entidades = {'AS','BC','BS','CC','CL','CM','CS','CH','DF','DG','GT','GR','HG','JC','MC','MN','MS','NT','NL','OC','PL','QT','QR','SP','SL','SR','TC','TS','TL','VZ','YN','ZS'}
        if curp[11:13] not in entidades:
            return False
        return True

class InterfazCURP(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.title("CURP - Sistema de Gestión")
        self.configure(bg='#2C3E50')
        # Ajustamos el tamaño de la ventana para que sea más estrecha y alta
        self.geometry("600x400")
        # Establecemos tamaños mínimos y máximos para mantener la proporción
        self.minsize(500, 700)
        self.maxsize(700, 900)
        self.configure_styles()
        self.maquina = MaquinaDeTuring()
        self.setup_ui()

    def configure_styles(self):
        # Configure modern dark theme styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define colors
        self.colors = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'accent': '#3498DB',
            'error': '#E74C3C',
            'success': '#2ECC71',
            'entry_bg': '#34495E',
            'button_bg': '#3498DB',
            'button_active': '#2980B9'
        }

        # Configure individual widget styles
        self.style.configure('Main.TFrame', 
            background=self.colors['bg'],
            padding=5  # Reducimos el padding general
        )
        self.style.configure('Main.TLabel',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            font=('Segoe UI', 8)  # Reducimos el tamaño de fuente
        )
        self.style.configure('Header.TLabel',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            font=('Segoe UI', 10, 'bold')  # Reducimos el tamaño del encabezado
        )
        self.style.configure('Subheader.TLabel',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            font=('Segoe UI', 10)  # Reducimos el tamaño del subencabezado
        )
        
        # Custom button style más compacto
        self.style.configure('Custom.TButton',
            background=self.colors['button_bg'],
            foreground=self.colors['fg'],
            padding=(9, 8),  # Reducimos el padding del botón
            font=('Segoe UI', 7),
            borderwidth=0
        )
        self.style.map('Custom.TButton',
            background=[('active', self.colors['button_active'])]
        )

        # Custom entry style más compacto
        self.style.configure('Custom.TEntry',
            fieldbackground=self.colors['entry_bg'],
            foreground=self.colors['fg'],
            padding=8  # Reducimos el padding de las entradas
        )

        # Custom notebook style más compacto
        self.style.configure('Custom.TNotebook',
            background=self.colors['bg'],
            borderwidth=0
        )
        self.style.configure('Custom.TNotebook.Tab',
            background=self.colors['entry_bg'],
            foreground=self.colors['fg'],
            padding=(9, 8),  # Reducimos el padding de las pestañas
            font=('Segoe UI', 5)
        )
        self.style.map('Custom.TNotebook.Tab',
            background=[('selected', self.colors['accent'])]
        )

        # Añadimos estilo para el frame contenedor
        self.style.configure('Container.TFrame',
            background=self.colors['bg'],
            padding=(10, 10)  # Padding horizontal más pequeño
        )

    def setup_ui(self):
        self.main_frame = ttk.Frame(self, style='Main.TFrame', padding="5")
        self.main_frame.pack(fill='both', expand=True)

        # Header con padding reducido
        # header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        # header_frame.pack(fill='x', pady=(0, 10))  # Reducimos el padding vertical
        # ttk.Label(
        #     header_frame,
        #     text="Sistema de Gestión CURP",
        #     style='Header.TLabel'
        # ).pack(anchor='center')

        # Notebook con estilo personalizado
        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=5)  # Añadimos padding horizontal

        # Contenedor para las pestañas
        self.tab_generacion = self.crear_tab_generacion()
        self.tab_validacion = self.crear_tab_validacion()
        
        self.notebook.add(self.tab_generacion, text='Generar CURP')
        self.notebook.add(self.tab_validacion, text='Validar CURP')

    def crear_tab_generacion(self):
        frame = ttk.Frame(self.notebook, style='Main.TFrame', padding="20")
        
        # Title for generation tab
        # ttk.Label(
        #     frame,
        #     text="Generación de CURP",
        #     style='Subheader.TLabel'
        # ).pack(pady=(0, 20))

        # Create form frame
        form_frame = ttk.Frame(frame, style='Main.TFrame')
        form_frame.pack(fill='both', expand=True)

        self.vars_entrada = {}
        campos = [
            ("Nombre(s)", True),
            ("Apellido Paterno", True),
            ("Apellido Materno", False),
            ("Fecha de Nacimiento (YYYYMMDD)", True)
        ]

        # Create form fields with better spacing and styling
        for i, (campo, required) in enumerate(campos):
            field_frame = ttk.Frame(form_frame, style='Main.TFrame')
            field_frame.pack(fill='x', pady=10)

            label_text = f"{campo}{'*' if required else ''}"
            ttk.Label(
                field_frame,
                text=label_text,
                style='Main.TLabel'
            ).pack(anchor='w')

            var = tk.StringVar()
            self.vars_entrada[campo] = var
            entry = ttk.Entry(
                field_frame,
                textvariable=var,
                style='Custom.TEntry',
                font=('Segoe UI', 9)
            )
            entry.pack(fill='x', pady=(5, 0))

        # Sex selection with custom radio buttons
        sex_frame = ttk.Frame(form_frame, style='Main.TFrame')
        sex_frame.pack(fill='x', pady=10)
        ttk.Label(sex_frame, text="Sexo*", style='Main.TLabel').pack(anchor='w')
        
        radio_frame = ttk.Frame(sex_frame, style='Main.TFrame')
        radio_frame.pack(fill='x', pady=(5, 0))
        
        self.var_sexo = tk.StringVar(value="H")
        ttk.Radiobutton(
            radio_frame,
            text="Hombre",
            variable=self.var_sexo,
            value="H",
            style='Custom.TRadiobutton'
        ).pack(side='left', padx=(0, 20))
        ttk.Radiobutton(
            radio_frame,
            text="Mujer",
            variable=self.var_sexo,
            value="M",
            style='Custom.TRadiobutton'
        ).pack(side='left')

        # State selection
        state_frame = ttk.Frame(form_frame, style='Main.TFrame')
        state_frame.pack(fill='x', pady=10)
        ttk.Label(
            state_frame,
            text="Estado*",
            style='Main.TLabel'
        ).pack(anchor='w')

        self.var_estado = tk.StringVar()
        self.combo_estados = ttk.Combobox(
            state_frame,
            textvariable=self.var_estado,
            font=('Segoe UI', 11),
            state='readonly'
        )
        self.combo_estados['values'] = self.obtener_estados_mexico()
        self.combo_estados.pack(fill='x', pady=(5, 0))

        # Generate button
        ttk.Button(
            form_frame,
            text="Generar CURP",
            command=self.generar_curp,
            style='Custom.TButton'
        ).pack(pady=30)

        # Result label
        self.var_resultado = tk.StringVar()
        result_label = ttk.Label(
            form_frame,
            textvariable=self.var_resultado,
            style='Subheader.TLabel',
            wraplength=50
        )
        result_label.pack(pady=10)

        return frame
    

    def crear_tab_validacion(self):
        frame = ttk.Frame(self.notebook, style='Main.TFrame', padding="30")
        
        # Title for validation tab
        ttk.Label(
            frame,
            text="Validación de CURP",
            style='Subheader.TLabel'
        ).pack(pady=(0, 20))

        # Instructions
        ttk.Label(
            frame,
            text="Ingrese el CURP a validar:",
            style='Main.TLabel'
        ).pack(pady=(20, 10))

        # CURP input
        self.var_curp_validar = tk.StringVar()
        curp_entry = ttk.Entry(
            frame,
            textvariable=self.var_curp_validar,
            font=('Segoe UI', 14),
            style='Custom.TEntry'
        )
        curp_entry.pack(fill='x', padx=50, pady=(0, 20))

        # Validate button
        ttk.Button(
            frame,
            text="Validar CURP",
            command=self.validar_curp,
            style='Custom.TButton'
        ).pack(pady=20)

        # Validation result
        self.var_validacion = tk.StringVar()
        validation_label = ttk.Label(
            frame,
            textvariable=self.var_validacion,
            style='Subheader.TLabel'
        )
        validation_label.pack(pady=20)

        return frame

    # The rest of the methods remain unchanged as they contain the business logic
    def obtener_estados_mexico(self) -> List[str]:
        return ['AS - Aguascalientes', 'BC - Baja California', 'BS - Baja California Sur', 'CC - Campeche', 
                'CL - Coahuila', 'CM - Colima', 'CS - Chiapas', 'CH - Chihuahua', 'DF - Ciudad de México', 
                'DG - Durango', 'GT - Guanajuato', 'GR - Guerrero', 'HG - Hidalgo', 'JC - Jalisco', 
                'MC - Estado de México', 'MN - Michoacán', 'MS - Morelos', 'NT - Nayarit', 'NL - Nuevo León', 
                'OC - Oaxaca', 'PL - Puebla', 'QT - Querétaro', 'QR - Quintana Roo', 'SP - San Luis Potosí', 
                'SL - Sinaloa', 'SR - Sonora', 'TC - Tabasco', 'TS - Tamaulipas', 'TL - Tlaxcala', 
                'VZ - Veracruz', 'YN - Yucatán', 'ZS - Zacatecas']

    def es_bisiesto(self, anio: int) -> bool:
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    def primera_vocal_interna(self, texto: str) -> str:
        if len(texto) < 2:
            return "X"
        for c in texto[1:]:
            if c in "AEIOU":
                return c
        return "X"

    def primera_consonante_interna(self, texto: str) -> str:
        if len(texto) < 2:
            return "X"
        consonantes = "BCDFGHJKLMNPQRSTVWXYZ"
        for c in texto[1:]:
            if c in consonantes:
                return c
        return "X"

    def generar_curp(self):
        try:
            nombre = self.vars_entrada["Nombre(s)"].get().strip().upper()
            ap_paterno = self.vars_entrada["Apellido Paterno"].get().strip().upper()
            ap_materno = self.vars_entrada["Apellido Materno"].get().strip().upper() or "X"
            fecha = self.vars_entrada["Fecha de Nacimiento (YYYYMMDD)"].get().strip()
            sexo = self.var_sexo.get()
            estado = self.var_estado.get()[:2]

            if not all([nombre, ap_paterno, fecha, sexo, estado]):
                raise ValueError("Todos los campos obligatorios deben estar llenos")

            if not re.match(r'^\d{8}$', fecha):
                raise ValueError("La fecha debe tener formato YYYYMMDD")

            anio = int(fecha[:4])
            mes = int(fecha[4:6])
            dia = int(fecha[6:])
            
            dias_por_mes = [31, 29 if self.es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if not (1 <= mes <= 12) or not (1 <= dia <= dias_por_mes[mes - 1]):
                raise ValueError("Fecha de nacimiento no válida")

            nombres = nombre.split()
            primer_nombre = nombres[1] if len(nombres) > 1 and nombres[0] in {"MARIA", "JOSE"} else nombres[0]

            curp = (
                ap_paterno[0] +
                self.primera_vocal_interna(ap_paterno) +
                ap_materno[0] +
                primer_nombre[0] +
                fecha[2:] +
                sexo +
                estado +
                self.primera_consonante_interna(ap_paterno) +
                self.primera_consonante_interna(ap_materno) +
                self.primera_consonante_interna(primer_nombre) +
                str(random.randint(0, 9)) +
                str(random.randint(0, 9))
            )

            self.var_resultado.set(f"{curp}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validar_curp(self):
        curp = self.var_curp_validar.get().strip().upper()
        if self.maquina.validar_curp(curp):
            self.var_validacion.set("CURP válido ✓")
            self.var_validacion.configure(foreground=self.colors['success'])
        else:
            self.var_validacion.set("CURP inválido ✗")
            self.var_validacion.configure(foreground=self.colors['error'])

if __name__ == "__main__":
    app = InterfazCURP()
    app.mainloop()