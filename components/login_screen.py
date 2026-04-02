import flet as ft
import time


class LoginScreen(ft.Container):
    """
    Pantalla de login para Zenith OS
    """
    
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self._page = page
        self.on_login_success = on_login_success
        
        # Credenciales por defecto (en un sistema real, esto vendría de una base de datos)
        self.usuario_valido = "admin"
        self.password_valido = "zenith"
        
        # Campo de usuario
        self.campo_usuario = ft.TextField(
            label="Usuario",
            hint_text="Ingresa tu usuario",
            prefix_icon=ft.Icons.PERSON,
            width=350,
            autofocus=True,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_600,
            text_size=14,
        )
        
        # Campo de contraseña
        self.campo_password = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=350,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_600,
            text_size=14,
            on_submit=self._intentar_login,
        )
        
        # Botón de login
        self.boton_login = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LOGIN, size=20),
                    ft.Text("Iniciar Sesión", size=16, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=350,
            height=50,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self._intentar_login,
        )
        
        # Mensaje de error
        self.mensaje_error = ft.Text(
            "",
            color=ft.Colors.RED_400,
            size=12,
            text_align=ft.TextAlign.CENTER,
            visible=False,
        )
        
        # Indicador de carga
        self.indicador_carga = ft.ProgressRing(
            width=30,
            height=30,
            stroke_width=3,
            color=ft.Colors.BLUE_400,
            visible=False,
        )
        
        # Contenedor del formulario
        self.contenedor_formulario = ft.Container(
            content=ft.Column(
                controls=[
                    # Logo pequeño
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.COMPUTER,
                            size=80,
                            color=ft.Colors.BLUE_400,
                        ),
                        alignment=ft.alignment.Alignment.CENTER,
                        margin=ft.margin.only(bottom=20),
                    ),
                    ft.Text(
                        "ZenithOS",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Iniciar Sesión",
                        size=18,
                        color=ft.Colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=40),
                    self.campo_usuario,
                    ft.Container(height=15),
                    self.campo_password,
                    ft.Container(height=10),
                    self.mensaje_error,
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            self.indicador_carga,
                            self.boton_login,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=40,
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.GREY_900),
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_400)),
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            ),
        )
        
        # Contenedor principal con fondo
        self.content = ft.Stack(
            controls=[
                # Fondo con imagen (opcional) o color sólido
                ft.Container(
                    bgcolor=ft.Colors.BLACK,
                    expand=True,
                ),
                # Formulario centrado
                ft.Container(
                    content=self.contenedor_formulario,
                    alignment=ft.alignment.Alignment.CENTER,
                ),
            ],
            expand=True,
        )
        
        # Estilo del contenedor principal
        self.bgcolor = ft.Colors.BLACK
        self.expand = True
        self.padding = 0
    
    def _intentar_login(self, e):
        """Intenta iniciar sesión con las credenciales ingresadas"""
        usuario = self.campo_usuario.value.strip()
        password = self.campo_password.value.strip()
        
        # Validar campos vacíos
        if not usuario or not password:
            self._mostrar_error("Por favor, completa todos los campos")
            return
        
        # Mostrar indicador de carga
        self.boton_login.disabled = True
        self.indicador_carga.visible = True
        self.mensaje_error.visible = False
        self._page.update()
        
        # Simular verificación (en un sistema real, esto sería una llamada a API/BD)
        def verificar_login():
            time.sleep(0.8)  # Simular tiempo de verificación
            
            if usuario == self.usuario_valido and password == self.password_valido:
                # Login exitoso
                if self.on_login_success:
                    self.on_login_success()
            else:
                # Login fallido
                self.boton_login.disabled = False
                self.indicador_carga.visible = False
                self._mostrar_error("Usuario o contraseña incorrectos")
                self._page.update()
        
        import threading
        threading.Thread(target=verificar_login, daemon=True).start()
    
    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.mensaje_error.value = mensaje
        self.mensaje_error.visible = True
        self._page.update()

