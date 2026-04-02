import flet as ft
import time
import threading


class VentanaApp(ft.Container):
    """
    Clase base para ventanas en Zenith OS (Flet v0.80.5).
    Hereda de ft.Container para permitir posicionamiento en ft.Stack.
    Incluye animaciones de apertura y cierre.
    """

    def __init__(self, titulo, contenido, ancho=600, alto=400, on_close=None, on_focus=None, page=None):
        super().__init__()
        self.on_close = on_close
        self.on_focus = on_focus
        self._page = page
        self._ancho_original = ancho
        self._alto_original = alto

        # Barra de título de la ventana
        self.barra_titulo = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.WINDOW, color=ft.Colors.WHITE, size=16),
                            ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        spacing=10,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        icon_size=18,
                        on_click=self._cerrar,
                        tooltip="Cerrar",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.BLUE_700,
            padding=ft.padding.only(left=15, right=5, top=5, bottom=5),
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
        )

        # Estructura interna: Barra + Contenido
        self.content = ft.Column(
            controls=[
                self.barra_titulo,
                ft.Container(content=contenido, padding=15, expand=True),
            ],
            spacing=0,
        )

        # Propiedades visuales de la ventana
        self.width = ancho
        self.height = alto
        self.bgcolor = ft.Colors.SURFACE
        self.border_radius = 10
        self.shadow = ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK26)

        # Posición inicial por defecto
        self.left = 150
        self.top = 100

        # Opacidad inicial para animación
        self.opacity = 0
        self.scale = 0.8

        # Evento para traer al frente al hacer clic
        self.on_click = self._focus
        
        # Iniciar animación de apertura
        self._animar_apertura()

    def _animar_apertura(self):
        """Anima la apertura de la ventana con fade in y scale"""
        def animar():
            for i in range(21):
                progress = i / 20
                self.opacity = progress
                self.scale = 0.8 + (progress * 0.2)  # De 0.8 a 1.0
                if self._page:
                    try:
                        self._page.update()
                    except:
                        break
                time.sleep(0.01)
        
        threading.Thread(target=animar, daemon=True).start()

    def _cerrar(self, e):
        """Cierra la ventana con animación"""
        def animar_cierre():
            for i in range(21):
                progress = 1 - (i / 20)
                self.opacity = progress
                self.scale = 1.0 - (progress * 0.2)  # De 1.0 a 0.8
                if self._page:
                    try:
                        self._page.update()
                    except:
                        break
                time.sleep(0.01)
            
            # Llamar al callback después de la animación
            if self.on_close:
                self.on_close(self)
        
        threading.Thread(target=animar_cierre, daemon=True).start()

    def _focus(self, e):
        """Trae la ventana al frente cuando se hace clic"""
        if self.on_focus:
            self.on_focus(self)