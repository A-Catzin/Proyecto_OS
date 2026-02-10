import flet as ft
from components.window import VentanaApp
from components.taskbar import Taskbar
from apps.calculadora import CalculadoraApp
from apps.editor import EditorApp 

def main(page: ft.Page):
    page.title = "Zenith OS"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK # Modo oscuro por defecto
    
    # Lista para gestionar ventanas abiertas (Z-Index)
    ventanas_abiertas = []

    # --- LÓGICA DE GESTIÓN DE VENTANAS ---
    
    def actualizar_escritorio():
        # El orden en el Stack determina qué está encima
        escritorio_stack.controls = [
            fondo_escritorio,
            iconos_escritorio,
            *ventanas_abiertas,
            barra_tareas,
        ]
        page.update()

    def traer_al_frente(ventana):
        if ventana in ventanas_abiertas:
            ventanas_abiertas.remove(ventana)
            ventanas_abiertas.append(ventana)
            actualizar_escritorio()
    
    def cerrar_ventana(ventana):
        if ventana in ventanas_abiertas:
            ventanas_abiertas.remove(ventana)
            actualizar_escritorio()

    # --- LANZADORES DE APLICACIONES ---

    def abrir_calculadora(e):
        # Verificar si ya está abierta para no duplicar
        for v in ventanas_abiertas:
            if v.barra_titulo.content.controls[0].controls[1].value == "Calculadora":
                traer_al_frente(v)
                return

        calc_ui = CalculadoraApp()
        nueva_ventana = VentanaApp(
            titulo="Calculadora",
            contenido=calc_ui,
            ancho=350,
            alto=500,
            on_close=cerrar_ventana,
            on_focus=traer_al_frente
        )
        ventanas_abiertas.append(nueva_ventana)
        actualizar_escritorio()

    def abrir_editor(e):
        # Verificar si ya está abierta para no duplicar
        for v in ventanas_abiertas:
            if v.barra_titulo.content.controls[0].controls[1].value == "Editor de Texto":
                traer_al_frente(v)
                return

        editor_ui = EditorApp(page)
        nueva_ventana = VentanaApp(
            titulo="Editor de Texto",
            contenido=editor_ui,
            ancho=700,
            alto=550,
            on_close=cerrar_ventana,
            on_focus=traer_al_frente
        )
        ventanas_abiertas.append(nueva_ventana)
        actualizar_escritorio()


    # --- INTERFAZ PRINCIPAL ---

    # Fondo de pantalla (Usando la ruta de tu imagen en assets)
    fondo_escritorio = ft.Container(
        image=ft.DecorationImage(
            src="assets/pol-garden-smile-friends-polgarden.jpg",
            fit="cover",
        ),
        expand=True,
    )

    # Iconos del escritorio
    iconos_escritorio = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CALCULATE, size=50, color=ft.Colors.AMBER_400),
                    ft.Text("Calculadora", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.W_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=abrir_calculadora,
                padding=10,
                border_radius=10,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EDIT, size=50, color=ft.Colors.BLUE_400),
                    ft.Text("Editor de Texto", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.W_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=abrir_editor,
                padding=10,
                border_radius=10,
            ),
        ],
        top=40,
        left=40,
        spacing=20
    )

    # Barra de tareas (Componente separado)
    barra_tareas = Taskbar(page, on_menu_click=lambda _: print("Menú Inicio"))

    # Contenedor Stack para superponer todo
    escritorio_stack = ft.Stack(
        controls=[fondo_escritorio, iconos_escritorio, barra_tareas],
        expand=True,
    )

    page.add(escritorio_stack)

if __name__ == "__main__":
    # El assets_dir es vital para que Flet encuentre la carpeta assets
    ft.app(target=main, assets_dir="assets")