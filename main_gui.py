# main_gui.py (con historial visual y gráfico de toxicidad)
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from logic import SistemaExpertoQuimico
from typing import List, Dict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Experto Químico - cveraQ v1.0")
        self.geometry("900x700")
        self.configure(bg='#f0f0f0')

        self.sistema = SistemaExpertoQuimico()
        self.seleccionados = []

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Sistema Experto para Manejo de Químicos", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, pady=10, columnspan=3)
        ttk.Label(main_frame, text="Tierra del Fuego - Argentina", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, columnspan=3)

        ttk.Label(main_frame, text="Seleccione compuestos:").grid(row=2, column=0, sticky=tk.W)

        self.tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre', 'Categoría'), show='headings', height=10)
        self.tree.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW, columnspan=2)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Categoría', text='Categoría')

        for comp in self.sistema.compuestos:
            self.tree.insert('', tk.END, values=(comp['id'], comp['nombre'], comp['categoria']))

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=3, column=2, sticky=tk.NS)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=10, columnspan=3)

        ttk.Button(btn_frame, text="Agregar selección", command=self.agregar_compuesto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar selección", command=self.limpiar_seleccion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Evaluar mezcla", command=self.mostrar_dialogo_evaluacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver historial", command=self.mostrar_historial).pack(side=tk.RIGHT, padx=5)

        ttk.Label(main_frame, text="Compuestos seleccionados:").grid(row=5, column=0, sticky=tk.W, pady=(10,0))
        self.lista_seleccionados = tk.Listbox(main_frame, height=4)
        self.lista_seleccionados.grid(row=6, column=0, sticky=tk.EW, pady=5, columnspan=3)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.style = ttk.Style()
        self.style.configure('Accent.TButton', foreground='white', background='#0078d7')

    def agregar_compuesto(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            id_comp = item['values'][0]

            if id_comp not in self.seleccionados:
                self.seleccionados.append(id_comp)
                self.actualizar_lista_seleccionados()
            else:
                messagebox.showwarning("Advertencia", "Este compuesto ya fue seleccionado")

    def limpiar_seleccion(self):
        self.seleccionados = []
        self.actualizar_lista_seleccionados()

    def actualizar_lista_seleccionados(self):
        self.lista_seleccionados.delete(0, tk.END)
        for id_comp in self.seleccionados:
            comp = next(c for c in self.sistema.compuestos if c['id'] == id_comp)
            self.lista_seleccionados.insert(tk.END, f"{comp['id']}: {comp['nombre']} ({comp['categoria']})")

    def mostrar_dialogo_evaluacion(self):
        if len(self.seleccionados) < 2:
            messagebox.showerror("Error", "Seleccione al menos 2 compuestos")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Evaluación de Propiedades")
        dialog.geometry("600x500")
        dialog.transient(self)
        dialog.grab_set()

        sustancia = self.sistema.combinar_compuestos(self.seleccionados)

        frame_preg = ttk.Frame(dialog, padding="10")
        frame_preg.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_preg, text=f"Evaluar mezcla: {', '.join(sustancia['nombres'])}", font=('Helvetica', 12, 'bold')).pack(pady=5)

        self.respuestas = {}
        preguntas = [
            ('pH', f"¿El pH está fuera de rango seguro (2-12)? {'(Actual: '+str(sustancia['pH'])+')' if sustancia['pH'] else '(Desconocido)'}"),
            ('inflamable', "¿La sustancia es inflamable?"),
            ('reactivo', "¿La sustancia es reactiva?"),
            ('metales_pesados', "¿Contiene metales pesados?"),
            ('volatil', "¿Es volátil?"),
            ('explosivo', "¿La sustancia es explosiva o pirofórica?"),
            ('radiactivo', "¿Presenta riesgo radiactivo?"),
            ('biologico', "¿Contiene agentes biológicos peligrosos?")
        ]

        for i, (prop, preg) in enumerate(preguntas):
            frame = ttk.Frame(frame_preg)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=preg, width=50).pack(side=tk.LEFT)

            var = tk.StringVar(value='desconocido')
            self.respuestas[prop] = var

            ttk.Radiobutton(frame, text="Sí", variable=var, value='si').pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="No", variable=var, value='no').pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="Desconocido", variable=var, value='desconocido').pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_preg, text="Evaluar Toxicidad", command=lambda: self.mostrar_resultados(sustancia, dialog)).pack(pady=15)


    def mostrar_resultados(self, sustancia: Dict, dialog: tk.Toplevel):
        try:
            respuestas = {k: v.get() for k, v in self.respuestas.items()}
            nivel, detalle = self.sistema.evaluar_toxicidad(respuestas)
            recomendaciones = self.sistema.generar_recomendaciones(sustancia, nivel) or "⚠️ No se pudieron generar recomendaciones."

            self.sistema.registrar_consulta(sustancia['nombres'], (nivel, detalle))

            result_win = tk.Toplevel(self)
            result_win.title("Resultados de Evaluación")
            result_win.geometry("900x700")

            frame = ttk.Frame(result_win, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)

            ttk.Label(frame, text="RESULTADOS DE EVALUACIÓN", font=('Helvetica', 14, 'bold')).pack(pady=10)
            ttk.Label(frame, text=f"Mezcla: {', '.join(sustancia['nombres'])}", font=('Helvetica', 12)).pack(pady=5)
            ttk.Label(frame, text=f"Nivel de toxicidad: {nivel}", font=('Helvetica', 12, 'bold'), foreground='red').pack(pady=10)
            ttk.Label(frame, text=f"Detalle: {detalle}").pack(pady=5)

            ttk.Label(frame, text="RECOMENDACIONES PARA DESCARTE", font=('Helvetica', 12, 'bold')).pack(pady=(20,5))

            text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=10)
            text_area.pack(pady=10)
            text_area.insert(tk.INSERT, recomendaciones)
            text_area.configure(state='disabled')

            # Agregar gráfico de barras
            fig = self.sistema.generar_grafico_riesgo(detalle)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            ttk.Button(frame, text="Cerrar", command=result_win.destroy).pack(pady=10)

            dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def mostrar_historial(self):
        historial = self.sistema.obtener_historial()
        if not historial:
            messagebox.showinfo("Historial", "No hay evaluaciones registradas.")
            return

        win = tk.Toplevel(self)
        win.title("Historial de Evaluaciones")
        win.geometry("700x500")

        frame = ttk.Frame(win, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("Fecha", "Compuestos", "Nivel", "Detalle"), show="headings")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Compuestos", text="Compuestos")
        tree.heading("Nivel", text="Nivel Toxicidad")
        tree.heading("Detalle", text="Detalle")
        tree.pack(fill=tk.BOTH, expand=True)

        for reg in historial:
            tree.insert("", tk.END, values=(reg['fecha'], ', '.join(reg['compuestos']), reg['nivel_toxicidad'], reg['detalle']))

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()