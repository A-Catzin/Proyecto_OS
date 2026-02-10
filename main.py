import flet as ft
from datetime import datetime
from apps.calculadora import CalculadoraApp

class VentanaApp(ft.Container):
    """
    Clase base para ventanas en Flet v0.80.5 (1.0 Beta).
    """
    def __init__(self, titulo, contenido, ancho=600, alto=400, on_close=None, on_focus=None):
        super().__init__()
        self.on_close = on_close
        self.on_focus = on_focus

        # Barra de título
        self.barra_titulo = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        icon_size=18,
                        on_click=self._cerrar,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.BLUE_700,
            padding=10,
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
        )

        self.content = ft.Column(
            controls=[
                self.barra_titulo,
                ft.Container(content=contenido, padding=15, expand=True),
            ],
            spacing=0,
        )

        self.width = ancho
        self.height = alto
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
        self.border_radius = 10
        self.shadow = ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK26)
        self.left = 120
        self.top = 90
        self.on_click = self._focus

    def _cerrar(self, e):
        if self.on_close: 
            self.on_close(self)

    def _focus(self, e):
        if self.on_focus: 
            self.on_focus(self)


def main(page: ft.Page):
    page.title = "Zenith OS"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Ruta local del fondo
    fondo_url = "assets/pol-garden-smile-friends-polgarden.jpg"
    
    # ✅ En 0.80.5: fit es un STRING, no ft.ImageFit.COVER
    fondo_escritorio = ft.Container(
        image=ft.DecorationImage(
            src=fondo_url,
            fit="cover",  # ✅ String directo
        ),
        expand=True,
    )
    
    ventanas_abiertas = []
    
    def actualizar_escritorio():
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
    
    def abrir_ventana_ejemplo(e):
        nueva_ventana = VentanaApp(
            titulo="Ventana de Ejemplo",
            contenido=ft.Column([
                ft.Text("¡Sistema funcionando!", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Flet 0.80.5 - 1.0 Beta", size=12),
                ft.ElevatedButton("Botón de prueba", icon=ft.Icons.STAR)
            ], spacing=10),
            on_close=cerrar_ventana,
            on_focus=traer_al_frente
        )
        ventanas_abiertas.append(nueva_ventana)
        actualizar_escritorio()

    def abrir_calculadora(e):
        calc_ui = CalculadoraApp()
        nueva_ventana = VentanaApp(
            titulo="Calculadora",
            contenido=calc_ui,
            ancho=420,
            alto=520,
            on_close=cerrar_ventana,
            on_focus=traer_al_frente
        )
        ventanas_abiertas.append(nueva_ventana)
        actualizar_escritorio()

    # Iconos del escritorio
    iconos_escritorio = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.IconButton(
                        icon=ft.Icons.WINDOW,
                        icon_size=48, 
                        icon_color=ft.Colors.WHITE, 
                        on_click=abrir_ventana_ejemplo,
                        tooltip="Abrir ventana de ejemplo"
                    ),
                    ft.Text("App Ejemplo", color=ft.Colors.WHITE, size=12, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=15
            ),
            ft.Container(
                content=ft.Column([
                    ft.IconButton(
                        icon=ft.Text("🔢", size=36),
                        icon_color=ft.Colors.WHITE,
                        on_click=abrir_calculadora,
                        tooltip="Abrir Calculadora"
                    ),
                    ft.Text("Calculadora", color=ft.Colors.WHITE, size=12, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=15
            ),
        ],
        top=20, 
        left=20,
    )
    
    # Barra de tareas
    barra_tareas = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.APPS, 
                icon_color=ft.Colors.WHITE, 
                icon_size=28,
                tooltip="Menú Inicio"
            ),
            ft.Container(expand=True),
            ft.Text(
                datetime.now().strftime("%H:%M"), 
                color=ft.Colors.WHITE, 
                size=16,
                weight=ft.FontWeight.BOLD
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=10, 
        height=60, 
        bottom=0, 
        left=0, 
        right=0,
    )
    
    # Stack principal
    escritorio_stack = ft.Stack(
        controls=[fondo_escritorio, iconos_escritorio, barra_tareas],
        expand=True,
    )
    
    page.add(escritorio_stack)


# ✅ Usar ft.app() está bien, el warning es solo informativo
if __name__ == "__main__":
    ft.app(target=main)