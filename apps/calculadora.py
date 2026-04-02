import flet as ft

class CalculadoraApp(ft.Container):
    """
    Calculadora.
    Soporta operaciones básicas: +, -, *, /
    """
    
    def __init__(self):
        super().__init__()
        
        # Variables de estado para la calculadora
        self.operando1 = ""
        self.operador = ""
        self.operando2 = ""
        self.nuevo_numero = True
        
        # Display de resultado
        self.display = ft.TextField(
            value="0",
            text_align=ft.TextAlign.RIGHT,
            read_only=True,
            text_size=32,
            border_color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            height=90,
        )
        
        # Construir la interfaz
        self.content = ft.Column(
            controls=[
                # Display
                self.display,
                
                # Fila 1: C, /, *, -
                ft.Row(
                    controls=[
                        self._crear_boton("C", ft.Colors.RED_400, self._limpiar, flex=2),
                        self._crear_boton("/", ft.Colors.ORANGE_400, self._operacion),
                        self._crear_boton("*", ft.Colors.ORANGE_400, self._operacion),
                    ],
                    spacing=5,
                ),
                
                # Fila 2: 7, 8, 9, +
                ft.Row(
                    controls=[
                        self._crear_boton("7", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("8", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("9", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("+", ft.Colors.ORANGE_400, self._operacion),
                    ],
                    spacing=5,
                ),
                
                # Fila 3: 4, 5, 6, -
                ft.Row(
                    controls=[
                        self._crear_boton("4", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("5", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("6", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("-", ft.Colors.ORANGE_400, self._operacion),
                    ],
                    spacing=5,
                ),
                
                # Fila 4: 1, 2, 3
                ft.Row(
                    controls=[
                        self._crear_boton("1", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("2", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("3", ft.Colors.BLUE_GREY_700, self._numero),
                        self._crear_boton("=", ft.Colors.GREEN_400, self._calcular),
                    ],
                    spacing=5,
                ),
                
                # Fila 5: 0, .
                ft.Row(
                    controls=[
                        self._crear_boton("0", ft.Colors.BLUE_GREY_700, self._numero, flex=2),
                        self._crear_boton(".", ft.Colors.BLUE_GREY_700, self._numero),
                        # Espacio vacío para alinear con el botón =
                        ft.Container(expand=1),
                    ],
                    spacing=5,
                ),
            ],
            spacing=10,
            expand=True,
        )
        
        # Configuración del contenedor principal
        self.padding = 20
        self.bgcolor = ft.Colors.GREY_800
        self.border_radius = 10
        self.expand = True
    
    def _crear_boton(self, texto, color, funcion, flex=1):
        """
        Crea un botón estilizado para la calculadora.
        
        Args:
            texto: Texto del botón
            color: Color de fondo del botón
            funcion: Función a ejecutar al hacer clic
            flex: Factor de expansión del botón
        """
        return ft.Container(
            content=ft.Text(
                texto,
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            bgcolor=color,
            border_radius=8,
            alignment=ft.Alignment.CENTER,
            height=60,
            expand=flex,
            on_click=lambda e: funcion(texto),
            ink=True,  # Efecto ripple al hacer clic
        )
    
    def _numero(self, valor):
        """Maneja la entrada de números y punto decimal."""
        if self.nuevo_numero:
            self.display.value = valor
            self.nuevo_numero = False
        else:
            if valor == "." and "." in self.display.value:
                return  # Evitar múltiples puntos decimales
            if self.display.value == "0" and valor != ".":
                self.display.value = valor
            else:
                self.display.value += valor
        self.display.update()
    
    def _operacion(self, op):
        """Maneja las operaciones aritméticas."""
        if self.operando1 == "":
            self.operando1 = self.display.value
        elif self.operador != "" and not self.nuevo_numero:
            # Calcular resultado intermedio
            self._calcular("")
            self.operando1 = self.display.value
        
        self.operador = op
        self.nuevo_numero = True
    
    def _calcular(self, _):
        """Realiza el cálculo y muestra el resultado."""
        if self.operando1 == "" or self.operador == "":
            return
        
        self.operando2 = self.display.value
        
        try:
            num1 = float(self.operando1)
            num2 = float(self.operando2)
            
            # Realizar la operación correspondiente
            if self.operador == "+":
                resultado = num1 + num2
            elif self.operador == "-":
                resultado = num1 - num2
            elif self.operador == "*":
                resultado = num1 * num2
            elif self.operador == "/":
                if num2 == 0:
                    self.display.value = "Error: Div/0"
                    self._resetear_estado()
                    self.display.update()
                    return
                resultado = num1 / num2
            else:
                return
            
            # Formatear el resultado (eliminar decimales innecesarios)
            if resultado == int(resultado):
                self.display.value = str(int(resultado))
            else:
                self.display.value = f"{resultado:.8g}"
            
            # Resetear estado para nueva operación
            self._resetear_estado()
            self.operando1 = self.display.value
            
        except Exception as e:
            self.display.value = "Error"
            self._resetear_estado()
        
        self.display.update()
    
    def _limpiar(self, _):
        """Limpia el display y resetea el estado."""
        self.display.value = "0"
        self._resetear_estado()
        self.display.update()
    
    def _resetear_estado(self):
        """Resetea las variables de estado."""
        self.operando1 = ""
        self.operador = ""
        self.operando2 = ""
        self.nuevo_numero = True