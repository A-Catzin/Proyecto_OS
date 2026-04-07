import flet as ft
import time
import threading


class BootScreen(ft.Container):
    """
    Pantalla de carga (Boot Screen) para Zenith OS
    Simula el proceso de arranque de un sistema operativo real
    """
    
    def __init__(self, page: ft.Page, on_complete):
        super().__init__()
        self._page = page
        self.on_complete = on_complete
        self.progreso = 0
        
        # Logo y título
        self.logo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.COMPUTER,
                        size=120,
                        color=ft.Colors.BLUE_400,
                    ),
                    ft.Text(
                        "ZenithOS",
                        size=48,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Sistema Operativo v1.0",
                        size=16,
                        color=ft.Colors.GREY_400,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.Alignment.CENTER,
        )
        
        # Barra de progreso animada
        self.barra_progreso = ft.ProgressBar(
            width=400,
            height=8,
            color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.GREY_800,
            value=0,
        )
        
        # Texto de estado del boot
        self.texto_estado = ft.Text(
            "Inicializando sistema...",
            size=14,
            color=ft.Colors.GREY_300,
            text_align=ft.TextAlign.CENTER,
        )
        
        # Mensajes de boot (simulando procesos del sistema)
        self.mensajes_boot = [
            "Inicializando sistema...",
            "Cargando núcleo...",
            "Iniciando servicios...",
            "Configurando red...",
            "Cargando interfaz gráfica...",
            "Preparando escritorio...",
            "Listo",
        ]
        self.indice_mensaje = 0
        
        # Contenedor principal
        self.content = ft.Column(
            controls=[
                self.logo,
                ft.Container(height=60),  # Espaciador
                self.barra_progreso,
                ft.Container(height=20),
                self.texto_estado,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        
        # Estilo del contenedor
        self.bgcolor = ft.Colors.BLACK
        self.expand = True
        self.padding = 0
        
        # Iniciar animación de boot
        self._iniciar_boot()
    
    def _iniciar_boot(self):
        """Inicia la animación del proceso de boot"""
        def animar_boot():
            for i in range(101):
                time.sleep(0.03)  # Controla la velocidad del boot
                self.progreso = i / 100
                self.barra_progreso.value = self.progreso
                
                # Actualizar mensaje cada cierto progreso
                if i % 15 == 0 and self.indice_mensaje < len(self.mensajes_boot):
                    self.texto_estado.value = self.mensajes_boot[self.indice_mensaje]
                    self.indice_mensaje += 1
            
            # Esperar un momento antes de completar
            time.sleep(0.5)
            if self.on_complete:
                self.on_complete()
        
        # Ejecutar en un hilo separado
        threading.Thread(target=animar_boot, daemon=True).start()

