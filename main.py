import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# Конфигурация окна (для тестов на ПК)
Window.size = (400, 700)
Window.clearcolor = get_color_from_hex('#121212')

KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<DisplayLabel@Label>:
    text_size: self.size
    halign: 'right'
    valign: 'middle'
    font_size: '64sp'
    color: get_color_from_hex('#FFFFFF')
    padding: [20, 0]
    font_name: 'Roboto'

<FormulaLabel@Label>:
    text_size: self.size
    halign: 'right'
    valign: 'bottom'
    font_size: '24sp'
    color: get_color_from_hex('#AAAAAA')
    padding: [20, 0]
    font_name: 'Roboto'

<ModernButton>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    color: get_color_from_hex('#FFFFFF')
    font_size: '28sp'
    bold: True
    
    canvas.before:
        # 1. Основной цвет кнопки
        Color:
            rgba: self.bg_color_rgba
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height * 0.25]
        
        # 2. Слой подсветки (анимируем его прозрачность)
        Color:
            rgba: 1, 1, 1, self.highlight_opacity
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height * 0.25]

BoxLayout:
    orientation: 'vertical'
    padding: 15
    spacing: 10
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.3
        
        FormulaLabel:
            id: formula_label
            text: ''
            size_hint_y: 0.3
            
        DisplayLabel:
            id: display_label
            text: '0'
            size_hint_y: 0.7

    GridLayout:
        cols: 4
        spacing: 15
        size_hint_y: 0.7
        
        # Ряд 1
        ModernButton:
            text: 'AC'
            text_color: '#FF5252'
            bg_hex: '#2C2C2C'
            on_release: app.clear_all()
        ModernButton:
            text: '('
            text_color: '#00E5FF'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression('(')
        ModernButton:
            text: ')'
            text_color: '#00E5FF'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression(')')
        ModernButton:
            text: '÷'
            text_color: '#FFA726'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression('/')

        # Ряд 2
        ModernButton:
            text: '7'
            on_release: app.add_to_expression('7')
        ModernButton:
            text: '8'
            on_release: app.add_to_expression('8')
        ModernButton:
            text: '9'
            on_release: app.add_to_expression('9')
        ModernButton:
            text: '×'
            text_color: '#FFA726'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression('*')

        # Ряд 3
        ModernButton:
            text: '4'
            on_release: app.add_to_expression('4')
        ModernButton:
            text: '5'
            on_release: app.add_to_expression('5')
        ModernButton:
            text: '6'
            on_release: app.add_to_expression('6')
        ModernButton:
            text: '-'
            text_color: '#FFA726'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression('-')

        # Ряд 4
        ModernButton:
            text: '1'
            on_release: app.add_to_expression('1')
        ModernButton:
            text: '2'
            on_release: app.add_to_expression('2')
        ModernButton:
            text: '3'
            on_release: app.add_to_expression('3')
        ModernButton:
            text: '+'
            text_color: '#FFA726'
            bg_hex: '#1E1E1E'
            on_release: app.add_to_expression('+')

        # Ряд 5
        ModernButton:
            text: '0'
            on_release: app.add_to_expression('0')
        ModernButton:
            text: '.'
            on_release: app.add_to_expression('.')
        ModernButton:
            text: 'C'
            text_color: '#FF5252'
            bg_hex: '#2C2C2C'
            on_release: app.delete_last()
        ModernButton:
            text: '='
            bg_hex: '#00E5FF'
            text_color: '#000000'
            on_release: app.calculate_result()
"""

class ModernButton(ButtonBehavior, Label):
    bg_hex = StringProperty('#1E1E1E')
    bg_color_rgba = ListProperty([0,0,0,0])
    text_color = StringProperty('#FFFFFF')
    highlight_opacity = NumericProperty(0)
    
    # Сюда сохраним исходный размер шрифта в пикселях
    original_font_size = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.set_initial_values, 0)

    def set_initial_values(self, dt):
        # Конвертируем HEX цвета в RGBA
        self.bg_color_rgba = get_color_from_hex(self.bg_hex)
        self.color = get_color_from_hex(self.text_color)
        
        # Сохраняем текущий размер шрифта (который уже пересчитан в пиксели из '28sp')
        self.original_font_size = self.font_size

    def on_press(self):
        # Анимируем шрифт относительно сохраненного размера (уменьшаем на 5%)
        # Используем original_font_size, чтобы избежать накопительной ошибки уменьшения
        target_size = self.original_font_size * 0.95
        anim = Animation(highlight_opacity=0.2, font_size=target_size, duration=0.05)
        anim.start(self)

    def on_release(self):
        # Возвращаем к original_font_size (это ЧИСЛО, поэтому ошибки умножения строки не будет)
        anim = Animation(highlight_opacity=0, font_size=self.original_font_size, duration=0.1)
        anim.start(self)

class CalculatorApp(App):
    expression = ""
    # Инициализация переменной, чтобы избежать AttributeError
    root_widget = None

    def build(self):
        self.root_widget = Builder.load_string(KV)
        return self.root_widget

    def add_to_expression(self, value):
        if self.expression and self.expression[-1] in '+-*/' and value in '+-*/':
            self.expression = self.expression[:-1] + value
        else:
            self.expression += value
        self.update_label()

    def clear_all(self):
        self.expression = ""
        self.root_widget.ids.formula_label.text = ""
        self.update_label()

    def delete_last(self):
        self.expression = self.expression[:-1]
        self.update_label()

    def calculate_result(self):
        try:
            self.root_widget.ids.formula_label.text = self.expression
            if not self.expression: return
            
            result = eval(self.expression)
            
            if isinstance(result, float) and result.is_integer():
                self.expression = str(int(result))
            else:
                self.expression = str(round(result, 8))
        except Exception:
            self.expression = "Error"
            
        self.update_label()

    def update_label(self):
        display_text = self.expression if self.expression else "0"
        display_text = display_text.replace('*', '×').replace('/', '÷')
        self.root_widget.ids.display_label.text = display_text

if __name__ == '__main__':
    CalculatorApp().run()