import flet as ft
from components.window import VentanaApp
from components.taskbar import Taskbar
from components.boot_screen import BootScreen
from components.login_screen import LoginScreen
from components.start_menu import StartMenu
from apps.calculadora import CalculadoraApp
from apps.editor import EditorApp
from apps.configuracion import ConfiguracionApp
from apps.terminal import TerminalApp
import time
import threading


def main(page: ft.Page):
    page.title = "Zenith OS"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1200
    page.window.height = 800
    
    # Lista para gestionar ventanas abiertas (Z-Index)
    ventanas_abiertas = []
    
    # Bloqueo para evitar abrir múltiples ventanas por doble clic rápido
    app_lock = threading.Lock()
    
    # Flag para actualizable que está pendiente
    actualizar_pendiente = False
    actualizar_lock = threading.Lock()
    
    # Contenedor principal que cambiará entre pantallas
    contenedor_principal = ft.Container(expand=True)
    
    # --- LÓGICA DE GESTIÓN DE VENTANAS ---
    
    def marcar_actualizar():
        """Marca que hay una actualización pendiente sin llamar page.update() aquí"""
        nonlocal actualizar_pendiente
        with actualizar_lock:
            actualizar_pendiente = True
    
    def actualizar_escritorio():
        """Actualiza el escritorio con todas las ventanas"""
        escritorio_stack.controls = [
            fondo_escritorio,
            iconos_escritorio,
            *ventanas_abiertas,
            menu_inicio,
            barra_tareas,
        ]
        marcar_actualizar()
    
    def traer_al_frente(ventana):
        """Trae una ventana al frente"""
        if ventana in ventanas_abiertas:
            ventanas_abiertas.remove(ventana)
            ventanas_abiertas.append(ventana)
            actualizar_escritorio()
    
    def cerrar_ventana(ventana):
        """Cierra una ventana"""
        if ventana in ventanas_abiertas:
            ventanas_abiertas.remove(ventana)
            actualizar_escritorio()
    
    # --- LANZADORES DE APLICACIONES ---
    
    def abrir_calculadora(e):
        """Abre la aplicación Calculadora"""
        with app_lock:
            # Verificar si ya está abierta
            for v in ventanas_abiertas:
                if v.barra_titulo.content.controls[0].controls[1].value == "Calculadora":
                    traer_al_frente(v)
                    return
            
            calc_ui = CalculadoraApp()
            nueva_ventana = VentanaApp(
                titulo="Calculadora",
                contenido=calc_ui,
                ancho=350,
                alto=500,
                on_close=cerrar_ventana,
                on_focus=traer_al_frente,
                page=page
            )
            ventanas_abiertas.append(nueva_ventana)
            actualizar_escritorio()
    
    def abrir_editor(e):
        """Abre la aplicación Editor de Texto"""
        with app_lock:
            # Verificar si ya está abierta
            for v in ventanas_abiertas:
                if v.barra_titulo.content.controls[0].controls[1].value == "Editor de Texto":
                    traer_al_frente(v)
                    return
            
            editor_ui = EditorApp(page)
            nueva_ventana = VentanaApp(
                titulo="Editor de Texto",
                contenido=editor_ui,
                ancho=700,
                alto=550,
                on_close=cerrar_ventana,
                on_focus=traer_al_frente,
                page=page
            )
            ventanas_abiertas.append(nueva_ventana)
            actualizar_escritorio()
    
    def abrir_configuracion(e):
        """Abre la aplicación Configuración"""
        with app_lock:
            # Verificar si ya está abierta
            for v in ventanas_abiertas:
                if v.barra_titulo.content.controls[0].controls[1].value == "Configuración":
                    traer_al_frente(v)
                    return
            
            config_ui = ConfiguracionApp(page)
            nueva_ventana = VentanaApp(
                titulo="Configuración",
                contenido=config_ui,
                ancho=400,
                alto=400,
                on_close=cerrar_ventana,
                on_focus=traer_al_frente,
                page=page
            )
            ventanas_abiertas.append(nueva_ventana)
            actualizar_escritorio()
    
    def abrir_terminal(e):
        """Abre la aplicación Terminal"""
        with app_lock:
            # Verificar si ya está abierta
            for v in ventanas_abiertas:
                if v.barra_titulo.content.controls[0].controls[1].value == "Terminal":
                    traer_al_frente(v)
                    return
            
            terminal_ui = TerminalApp(page)
            nueva_ventana = VentanaApp(
                titulo="Terminal",
                contenido=terminal_ui,
                ancho=500,
                alto=300,
                on_close=cerrar_ventana,
                on_focus=traer_al_frente,
                page=page
            )
            ventanas_abiertas.append(nueva_ventana)
            actualizar_escritorio()
    
    # --- MENÚ DE INICIO ---
    
    # Definir las aplicaciones disponibles
    apps_disponibles = [
        {
            "nombre": "Calculadora",
            "icono": ft.Icons.CALCULATE,
            "color": ft.Colors.AMBER_400,
            "id": "calculadora",
        },
        {
            "nombre": "Editor de Texto",
            "icono": ft.Icons.EDIT,
            "color": ft.Colors.BLUE_400,
            "id": "editor",
        },
        {
            "nombre": "Configuración",
            "icono": ft.Icons.SETTINGS,
            "color": ft.Colors.GREEN_400,
            "id": "configuracion",
        },
        {
            "nombre": "Terminal",
            "icono": ft.Icons.TERMINAL,
            "color": ft.Colors.PURPLE_400,
            "id": "terminal",
        },
    ]
    
    def manejar_app_menu(app_id):
        """Maneja la selección de una app desde el menú de inicio"""
        if app_id == "calculadora":
            abrir_calculadora(None)
        elif app_id == "editor":
            abrir_editor(None)
        elif app_id == "configuracion":
            abrir_configuracion(None)
        elif app_id == "terminal":
            abrir_terminal(None)
    
    # --- FUNCIONES DE TRANSICIÓN DE PANTALLAS ---
    
    def animar_fade_in(contenedor):
        """Anima el fade in de un contenedor"""
        contenedor.animate_opacity = ft.Animation(400, "easeInOut")
        contenedor.opacity = 1
    
    def animar_iconos_entrada():
        """Anima la entrada de los iconos al escritorio"""
        time.sleep(0.3)
        for icono in iconos_escritorio.controls:
            icono.animate_opacity = ft.Animation(300, "easeInOut")
            icono.opacity = 1
    
    def mostrar_escritorio():
        """Muestra el escritorio principal"""
        contenedor_principal.content = escritorio_stack
        animar_fade_in(contenedor_principal)
        threading.Thread(target=animar_iconos_entrada, daemon=True).start()
    
    def mostrar_login():
        """Muestra la pantalla de login"""
        login_screen = LoginScreen(page, on_login_success=mostrar_escritorio)
        contenedor_principal.content = login_screen
        animar_fade_in(contenedor_principal)
    
    def mostrar_boot():
        """Muestra la pantalla de boot"""
        boot_screen = BootScreen(page, on_complete=mostrar_login)
        contenedor_principal.content = boot_screen
        animar_fade_in(contenedor_principal)
    
    # --- INTERFAZ DEL ESCRITORIO ---
    
    # Fondo de pantalla
    fondo_escritorio = ft.Container(
        image=ft.DecorationImage(
            src="assets/Inicio.jpg",
            fit="cover",
        ),
        expand=True,
    )
    
    # Función para crear icono animado
    def crear_icono_escritorio(icono, texto, color, funcion_click):
        """Crea un icono del escritorio con animaciones"""
        contenedor_icono = ft.Container(
            content=ft.Column([
                ft.Icon(icono, size=50, color=color),
                ft.Text(texto, color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.W_500)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=funcion_click,
            padding=10,
            border_radius=10,
            opacity=0.9,
        )
        
        # Efecto hover con animación
        def on_hover(e):
            es_hover = e.data == "true"
            contenedor_icono.animate_opacity = ft.Animation(200, "easeInOut")
            contenedor_icono.animate_scale = ft.Animation(200, "easeInOut")
            
            if es_hover:
                contenedor_icono.opacity = 1.0
                contenedor_icono.scale = 1.1
                contenedor_icono.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            else:
                contenedor_icono.opacity = 0.9
                contenedor_icono.scale = 1
                contenedor_icono.bgcolor = None
        
        contenedor_icono.on_hover = on_hover
        return contenedor_icono
    
    # Iconos del escritorio con animaciones
    iconos_escritorio = ft.Column(
        controls=[
            crear_icono_escritorio(
                ft.Icons.CALCULATE,
                "Calculadora",
                ft.Colors.AMBER_400,
                abrir_calculadora
            ),
            crear_icono_escritorio(
                ft.Icons.EDIT,
                "Editor de Texto",
                ft.Colors.BLUE_400,
                abrir_editor
            ),
            crear_icono_escritorio(
                ft.Icons.SETTINGS,
                "Configuración",
                ft.Colors.GREEN_400,
                abrir_configuracion
            ),
            crear_icono_escritorio(
                ft.Icons.TERMINAL,
                "Terminal",
                ft.Colors.PURPLE_400,
                abrir_terminal
            ),
        ],
        top=40,
        left=40,
        spacing=20
    )
    
    # Menú de inicio
    menu_inicio = StartMenu(page, apps=apps_disponibles, on_app_click=manejar_app_menu)
    
    def toggle_menu_inicio(e):
        """Alterna el menú de inicio"""
        menu_inicio.toggle()
    
    # Cerrar menú al hacer clic en el fondo del escritorio
    def click_escritorio(e):
        """Cierra el menú de inicio si está abierto al hacer clic en el escritorio"""
        if menu_inicio.esta_abierto:
            menu_inicio.toggle()
    
    fondo_escritorio.on_click = click_escritorio
    
    # Barra de tareas
    barra_tareas = Taskbar(page, on_menu_click=toggle_menu_inicio)
    
    # Stack del escritorio
    escritorio_stack = ft.Stack(
        controls=[fondo_escritorio, iconos_escritorio, menu_inicio, barra_tareas],
        expand=True,
    )
    
    # Configurar contenedor principal
    contenedor_principal.expand = True
    
    # --- SISTEMA DE ACTUALIZACIÓN GLOBAL ---
    def sistema_actualizar():
        """Sistema de actualización global cada 0.5 segundos"""
        pass
    
    # Iniciar thread de actualización global
    threading.Thread(target=sistema_actualizar, daemon=True).start()
    
    # Agregar contenedor a la página
    page.add(contenedor_principal)
    
    # Iniciar con la pantalla de boot
    mostrar_boot()


if __name__ == "__main__":
    # ft.run() requiere main como argumento posicional, no como keyword
    ft.run(main, assets_dir="assets")