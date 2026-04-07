import flet as ft
import time
import threading


class StartMenu(ft.Container):
    """
    Menú de inicio estilo Windows para Zenith OS.
    Se despliega desde la esquina inferior izquierda con una lista de aplicaciones.
    """

    def __init__(self, page: ft.Page, apps: list, on_app_click):
        """
        Args:
            page: La página principal de Flet.
            apps: Lista de dicts con info de apps: [{"nombre": str, "icono": Icon, "color": Color, "id": str}]
            on_app_click: Callback que recibe el id de la app seleccionada.
        """
        super().__init__()
        self._page = page
        self._on_app_click = on_app_click
        self._visible_menu = False

        # Crear items del menú
        menu_items = []
        for app in apps:
            item = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(app["icono"], size=28, color=app["color"]),
                        ft.Text(
                            app["nombre"],
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                border_radius=8,
                on_click=lambda e, app_id=app["id"]: self._seleccionar_app(app_id),
                on_hover=self._hover_item,
                ink=True,
            )
            menu_items.append(item)

        # Separador y botón de apagar
        boton_apagar = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.POWER_SETTINGS_NEW, size=24, color=ft.Colors.RED_400),
                    ft.Text(
                        "Apagar",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.RED_400,
                    ),
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            border_radius=8,
            on_click=lambda e: self._apagar(),
            on_hover=self._hover_item,
            ink=True,
        )

        # Header del menú
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.BLUE_200),
                    ft.Column(
                        [
                            ft.Text(
                                "Zenith OS",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "Usuario",
                                size=12,
                                color=ft.Colors.BLUE_200,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            border=ft.border.only(
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))
            ),
        )

        # Sección de "Todas las aplicaciones"
        titulo_apps = ft.Container(
            content=ft.Text(
                "Aplicaciones",
                size=12,
                color=ft.Colors.BLUE_200,
                weight=ft.FontWeight.W_600,
            ),
            padding=ft.padding.only(left=20, top=12, bottom=4),
        )

        # Layout del menú
        self.content = ft.Column(
            [
                header,
                titulo_apps,
                *menu_items,
                ft.Container(height=5),  # Espaciador
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                boton_apagar,
            ],
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
        )

        # Estilo visual del menú
        self.width = 280
        self.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900)
        self.border_radius = ft.border_radius.only(top_left=12, top_right=12)
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_400))
        self.shadow = ft.BoxShadow(
            blur_radius=25,
            spread_radius=2,
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        )
        self.padding = ft.padding.only(bottom=10, top=0)
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS

        # Posición: arriba de la taskbar, esquina inferior izquierda
        self.bottom = 50
        self.left = 0

        # Inicialmente oculto
        self.visible = False
        self.opacity = 0
        self.scale = 0.9

    def _hover_item(self, e):
        """Efecto hover en los items del menú"""
        container = e.control
        if e.data == "true":
            container.bgcolor = ft.Colors.with_opacity(0.15, ft.Colors.BLUE_400)
        else:
            container.bgcolor = None

    def _seleccionar_app(self, app_id):
        """Selecciona una app y cierra el menú"""
        self.toggle()
        if self._on_app_click:
            self._on_app_click(app_id)

    def _apagar(self):
        """Cierra la aplicación"""
        self.toggle()
        import sys
        sys.exit(0)

    def toggle(self):
        """Alterna la visibilidad del menú con animación"""
        if self._visible_menu:
            self._cerrar_menu()
        else:
            self._abrir_menu()

    def _abrir_menu(self):
        """Abre el menú con animación"""
        self._visible_menu = True
        self.visible = True
        self.animate_opacity = ft.Animation(500, "easeInOut")
        self.animate_scale = ft.Animation(500, "easeInOut")
        self.opacity = 1
        self.scale = 1

    def _cerrar_menu(self):
        """Cierra el menú con animación"""
        self._visible_menu = False
        self.animate_opacity = ft.Animation(300, "easeInOut")
        self.animate_scale = ft.Animation(300, "easeInOut")
        self.opacity = 0
        self.scale = 0.9
        def hide_after_animation():
            time.sleep(0.3)
            self.visible = False
        threading.Thread(target=hide_after_animation, daemon=True).start()

    @property
    def esta_abierto(self):
        return self._visible_menu
