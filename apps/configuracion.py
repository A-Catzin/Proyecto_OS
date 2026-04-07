import flet as ft

class ConfiguracionApp(ft.Container):
    """
    Aplicación de configuración básica para Zenith OS.
    Permite cambiar configuraciones simples como tema, sonido, etc.
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        # Configuraciones (simuladas, no persistentes)
        self.tema_oscuro = True
        self.sonido_activado = True
        self.notificaciones = True
        self.font_family = "Arial"
        self.font_size = 16
        self.letter_spacing = 0

        fuentes = [
            "Arial",
            "Courier New",
            "Georgia",
            "Roboto",
            "Comic Sans MS",
        ]

        # Switches para configuraciones
        self.switch_tema = ft.Switch(
            label="Tema Oscuro",
            value=self.tema_oscuro,
            on_change=self._cambiar_tema
        )

        self.dropdown_fuente = ft.Dropdown(
            width=260,
            label="Fuente",
            value=self.font_family,
            options=[ft.DropdownOption(font) for font in fuentes],
            on_select=self._cambiar_fuente,
        )

        self.slider_tamano = ft.Slider(
            min=12,
            max=32,
            divisions=10,
            label="{value}",
            value=self.font_size,
            on_change=self._cambiar_tamano,
        )

        self.slider_espacio = ft.Slider(
            min=0,
            max=10,
            divisions=10,
            label="{value}",
            value=self.letter_spacing,
            on_change=self._cambiar_espacio,
        )

        self.switch_sonido = ft.Switch(
            label="Sonido Activado",
            value=self.sonido_activado,
            on_change=self._cambiar_sonido
        )

        self.switch_notificaciones = ft.Switch(
            label="Notificaciones",
            value=self.notificaciones,
            on_change=self._cambiar_notificaciones
        )

        self.preview_text = ft.Text(
            "Vista previa: Zenith OS",
            style=ft.TextStyle(
                size=self.font_size,
                font_family=self.font_family,
                letter_spacing=self.letter_spacing,
            ),
            color=ft.Colors.WHITE,
        )

        # Botón para aplicar cambios
        self.boton_aplicar = ft.ElevatedButton(
            "Aplicar Cambios",
            on_click=self._aplicar_cambios,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE
        )

        # Layout
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Configuración del Sistema", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Divider(),
                    self.switch_tema,
                    self.dropdown_fuente,
                    ft.Row(
                        controls=[
                            ft.Text("Tamaño de fuente", color=ft.Colors.WHITE),
                            self.slider_tamano,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Espaciado de letras", color=ft.Colors.WHITE),
                            self.slider_espacio,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.preview_text,
                    ft.Divider(),
                    self.switch_sonido,
                    self.switch_notificaciones,
                    ft.Container(height=20),
                    self.boton_aplicar,
                ],
                spacing=16,
            ),
            padding=20,
        )

        self.bgcolor = ft.Colors.BLUE_GREY_900
        self.border_radius = 10
        self.padding = 10

    def _cambiar_tema(self, e):
        self.tema_oscuro = e.control.value

    def _cambiar_fuente(self, e):
        self.font_family = e.control.value
        self.preview_text.style = ft.TextStyle(
            size=self.font_size,
            font_family=self.font_family,
            letter_spacing=self.letter_spacing,
        )

    def _cambiar_tamano(self, e):
        self.font_size = int(e.control.value)
        self.preview_text.style = ft.TextStyle(
            size=self.font_size,
            font_family=self.font_family,
            letter_spacing=self.letter_spacing,
        )

    def _cambiar_espacio(self, e):
        self.letter_spacing = int(e.control.value)
        self.preview_text.style = ft.TextStyle(
            size=self.font_size,
            font_family=self.font_family,
            letter_spacing=self.letter_spacing,
        )

    def _cambiar_sonido(self, e):
        self.sonido_activado = e.control.value

    def _cambiar_notificaciones(self, e):
        self.notificaciones = e.control.value

    def _aplicar_cambios(self, e):
        # Aplicar tema y tipografía
        self._page.theme = ft.Theme(
            font_family=self.font_family,
            text_theme=ft.TextTheme(
                body_large=ft.TextStyle(size=self.font_size, letter_spacing=self.letter_spacing),
                body_medium=ft.TextStyle(size=self.font_size, letter_spacing=self.letter_spacing),
                body_small=ft.TextStyle(size=self.font_size, letter_spacing=self.letter_spacing),
                title_large=ft.TextStyle(size=self.font_size + 4, letter_spacing=self.letter_spacing),
                title_medium=ft.TextStyle(size=self.font_size + 2, letter_spacing=self.letter_spacing),
                label_large=ft.TextStyle(size=self.font_size, letter_spacing=self.letter_spacing),
                label_medium=ft.TextStyle(size=self.font_size, letter_spacing=self.letter_spacing),
            )
        )
        self._page.theme_mode = ft.ThemeMode.DARK if self.tema_oscuro else ft.ThemeMode.LIGHT

        # Mostrar mensaje de confirmación
        snack = ft.SnackBar(
            content=ft.Text("Configuraciones aplicadas", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_600
        )
        self._page.overlay.append(snack)
        snack.open = True