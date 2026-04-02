import flet as ft
from datetime import datetime
import threading
import time


class Taskbar(ft.Container):
    """
    Barra de tareas de Zenith OS con reloj funcional.
    """

    def __init__(self, page: ft.Page, on_menu_click):
        super().__init__()
        self._page = page

        # Reloj de la barra de tareas
        self.reloj = ft.Text(
            self._obtener_hora(),
            color=ft.Colors.WHITE,
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        self.content = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.APPS,
                    icon_color=ft.Colors.WHITE,
                    icon_size=28,
                    on_click=on_menu_click,
                    tooltip="Menú Inicio",
                ),
                ft.Container(expand=True),  # Espaciador
                ft.Row(
                    [
                        ft.Icon(ft.Icons.WIFI, color=ft.Colors.WHITE, size=16),
                        ft.Icon(ft.Icons.BATTERY_FULL, color=ft.Colors.WHITE, size=16),
                        ft.VerticalDivider(width=10),
                        self.reloj,
                    ],
                    spacing=15,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.bgcolor = ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900)
        self.padding = ft.padding.symmetric(horizontal=20)
        self.height = 50
        self.bottom = 0
        self.left = 0
        self.right = 0
        self.border = ft.border.only(top=ft.BorderSide(1, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_400)))
        
        # Animación de entrada
        self.opacity = 0
        self._animar_entrada()

        # Iniciar hilo para actualizar el reloj
        threading.Thread(target=self._actualizar_reloj, daemon=True).start()
    
    def _animar_entrada(self):
        """Anima la entrada de la barra de tareas"""
        def animar():
            for i in range(21):
                self.opacity = i / 20
                try:
                    self._page.update()
                except:
                    break
                time.sleep(0.01)
        
        threading.Thread(target=animar, daemon=True).start()

    def _obtener_hora(self):
        return datetime.now().strftime("%H:%M:%S")

    def _actualizar_reloj(self):
        while True:
            time.sleep(1)  # Actualiza cada segundo
            self.reloj.value = self._obtener_hora()
            try:
                self._page.update()
            except:
                break