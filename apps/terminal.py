import flet as ft
import subprocess
import platform

class TerminalApp(ft.Container):
    """
    Aplicación que abre la terminal del sistema operativo.
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        # Detectar el sistema operativo
        self.os = platform.system()

        # Botón para abrir terminal
        self.boton_abrir = ft.ElevatedButton(
            "Abrir Terminal del Sistema",
            icon=ft.Icons.TERMINAL,
            on_click=self._abrir_terminal,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
            height=50
        )

        # Texto informativo
        self.texto_info = ft.Text(
            f"Esta aplicación abrirá la terminal de {self.os}.",
            color=ft.Colors.WHITE,
            size=14
        )

        # Layout
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Terminal del Sistema", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Divider(),
                    self.texto_info,
                    ft.Container(height=20),
                    self.boton_abrir,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )

        self.bgcolor = ft.Colors.BLUE_GREY_900
        self.border_radius = 10
        self.padding = 10

    def _abrir_terminal(self, e):
        try:
            if self.os == "Windows":
                subprocess.Popen(["cmd.exe"])
            elif self.os == "Linux":
                subprocess.Popen(["Konsole"])
            else:
                raise Exception("Sistema operativo no soportado")

            # Mostrar mensaje de éxito
            snack = ft.SnackBar(
                content=ft.Text("Terminal abierta exitosamente", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_600
            )
            self._page.overlay.append(snack)
            snack.open = True

        except Exception as ex:
            # Mostrar mensaje de error
            snack = ft.SnackBar(
                content=ft.Text(f"Error al abrir terminal: {str(ex)}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_600
            )
            self._page.overlay.append(snack)
            snack.open = True