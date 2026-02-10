import flet as ft


class VentanaApp(ft.Container):
    """
    Clase base para ventanas en Zenith OS (Flet v0.80.5).
    Hereda de ft.Container para permitir posicionamiento en ft.Stack.
    """

    def __init__(self, titulo, contenido, ancho=600, alto=400, on_close=None, on_focus=None):
        super().__init__()
        self.on_close = on_close
        self.on_focus = on_focus

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

        # Evento para traer al frente al hacer clic
        self.on_click = self._focus

    def _cerrar(self, e):
        if self.on_close:
            self.on_close(self)

    def _focus(self, e):
        if self.on_focus:
            self.on_focus(self)