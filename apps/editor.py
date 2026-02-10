#Logica del editor de texto
import flet as ft

class EditorApp(ft.Container):
    """
    Aplicación de Editor de Texto para Zenith OS
    Permite escribir, limpiar y guardar texto (simulado)
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # Campo de texto multilínea para el editor
        self.campo_texto = ft.TextField(
            multiline=True,
            min_lines=20,
            max_lines=None,
            expand=True,
            hint_text="Escribe aquí tu texto...",
            border_color=ft.Colors.BLUE_400,
            text_size=14,
        )
        
        # Botones de acción
        self.btn_nuevo = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ADD, size=18),
                ft.Text("Nuevo"),
            ], spacing=5),
            on_click=self.limpiar_texto,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        self.btn_guardar = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.SAVE, size=18),
                ft.Text("Guardar"),
            ], spacing=5),
            on_click=self.guardar_texto,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
        )
        
        # Barra de herramientas
        self.barra_herramientas = ft.Row(
            controls=[
                self.btn_nuevo,
                self.btn_guardar,
            ],
            spacing=10,
        )
        
        # Contenedor principal del editor
        self.content = ft.Column(
            controls=[
                self.barra_herramientas,
                ft.Divider(height=1, color=ft.Colors.GREY_400),
                self.campo_texto,
            ],
            spacing=10,
            expand=True,
        )
        
        # Configuración del contenedor
        self.padding = 15
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 5
        self.expand = True
    
    def limpiar_texto(self, e):
        """Limpia el contenido del editor"""
        self.campo_texto.value = ""
        self._page.update()
        
        # Mostrar notificación
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text("Documento nuevo creado"),
            bgcolor=ft.Colors.BLUE_700,
        )
        self._page.snack_bar.open = True
        self._page.update()
    
    def guardar_texto(self, e):
        """Simula el guardado del texto"""
        if self.campo_texto.value and self.campo_texto.value.strip():
            # Mostrar diálogo de confirmación
            dialogo = ft.AlertDialog(
                title=ft.Text("Guardar archivo"),
                content=ft.Text(
                    f"Archivo guardado exitosamente (simulado)\n\n"
                    f"Caracteres: {len(self.campo_texto.value)}\n"
                    f"Palabras: {len(self.campo_texto.value.split())}"
                ),
                actions=[
                    ft.TextButton("Aceptar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                ],
            )
            self._page.dialog = dialogo
            dialogo.open = True
            self._page.update()
        else:
            # Mostrar advertencia si no hay texto
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text("No hay contenido para guardar"),
                bgcolor=ft.Colors.ORANGE_700,
            )
            self._page.snack_bar.open = True
            self._page.update()
    
    def cerrar_dialogo(self, dialogo):
        """Cierra el diálogo"""
        dialogo.open = False
        self._page.update()