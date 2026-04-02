import flet as ft
from components.window import VentanaApp
from components.taskbar import Taskbar
from components.boot_screen import BootScreen
from components.login_screen import LoginScreen
from apps.calculadora import CalculadoraApp
from apps.editor import EditorApp
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
    
    # Contenedor principal que cambiará entre pantallas
    contenedor_principal = ft.Container(expand=True)
    
    # --- LÓGICA DE GESTIÓN DE VENTANAS ---
    
    def actualizar_escritorio():
        """Actualiza el escritorio con todas las ventanas"""
        escritorio_stack.controls = [
            fondo_escritorio,
            iconos_escritorio,
            *ventanas_abiertas,
            barra_tareas,
        ]
        page.update()
    
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
    
    # --- FUNCIONES DE TRANSICIÓN DE PANTALLAS ---
    
    def animar_fade_in(contenedor):
        """Anima el fade in de un contenedor"""
        contenedor.opacity = 0
        page.update()
        
        def animar():
            for i in range(21):
                contenedor.opacity = i / 20
                try:
                    page.update()
                except:
                    break
                time.sleep(0.02)
        
        threading.Thread(target=animar, daemon=True).start()
    
    def animar_iconos_entrada():
        """Anima la entrada de los iconos al escritorio"""
        time.sleep(0.3)
        for i, icono in enumerate(iconos_escritorio.controls):
            icono.opacity = 0
            try:
                page.update()
            except:
                break
            time.sleep(0.1)
            
            # Animación de cada icono
            for j in range(21):
                progress = j / 20
                icono.opacity = progress
                try:
                    page.update()
                except:
                    break
                time.sleep(0.01)
    
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
        page.update()
    
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
        
        # Efecto hover con animación manual
        def on_hover(e):
            def animar_hover(es_hover):
                pasos = 10
                opacidad_inicial = contenedor_icono.opacity
                escala_inicial = contenedor_icono.scale if contenedor_icono.scale is not None else 1.0
                
                if es_hover:
                    opacidad_final = 1.0
                    escala_final = 1.1
                    color_final = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
                else:
                    opacidad_final = 0.9
                    escala_final = 1.0
                    color_final = None
                
                for i in range(pasos + 1):
                    progress = i / pasos
                    contenedor_icono.opacity = opacidad_inicial + (opacidad_final - opacidad_inicial) * progress
                    contenedor_icono.scale = escala_inicial + (escala_final - escala_inicial) * progress
                    if es_hover and i == pasos:
                        contenedor_icono.bgcolor = color_final
                    elif not es_hover and i == pasos:
                        contenedor_icono.bgcolor = None
                    try:
                        page.update()
                    except:
                        break
                    time.sleep(0.01)
            
            es_hover = e.data == "true"
            threading.Thread(target=lambda: animar_hover(es_hover), daemon=True).start()
        
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
        ],
        top=40,
        left=40,
        spacing=20
    )
    
    # Barra de tareas
    barra_tareas = Taskbar(page, on_menu_click=lambda _: print("Menú Inicio"))
    
    # Stack del escritorio
    escritorio_stack = ft.Stack(
        controls=[fondo_escritorio, iconos_escritorio, barra_tareas],
        expand=True,
    )
    
    # Configurar contenedor principal
    contenedor_principal.expand = True
    
    # Agregar contenedor a la página
    page.add(contenedor_principal)
    
    # Iniciar con la pantalla de boot
    mostrar_boot()


if __name__ == "__main__":
    # ft.run() requiere main como argumento posicional, no como keyword
    ft.run(main, assets_dir="assets")
