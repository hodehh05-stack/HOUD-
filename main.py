
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from kivy.core.window import Window
import ast
import operator

Window.clearcolor = (0.05, 0.02, 0.02, 1)

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg
}

def safe_calc(expression):
    def calc(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](calc(node.left), calc(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](calc(node.operand))
        raise ValueError("Invalid")

    return calc(ast.parse(expression, mode="eval").body)


class HoudApp(App):

    def build(self):
        root = FloatLayout()

        with root.canvas.before:
            self.bg = Rectangle(
                source="naruto.jpg",
                pos=root.pos,
                size=root.size
            )

        root.bind(
            size=lambda obj, val: setattr(self.bg, "size", val),
            pos=lambda obj, val: setattr(self.bg, "pos", val)
        )

        main = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10,
            size_hint=(1, 1)
        )

        title = Label(
            text="[b]HOUD[/b]  CROWN",
            markup=True,
            font_size=38,
            color=(1, 0.45, 0, 1),
            size_hint_y=0.17
        )

        self.display = TextInput(
            hint_text="Kteb l7sab dyalek...",
            font_size=30,
            multiline=False,
            size_hint_y=0.13
        )

        self.result = Label(
            text="Mar7ba bik HOUD!",
            font_size=24,
            color=(1, 0.7, 0.1, 1),
            size_hint_y=0.12
        )

        main.add_widget(title)
        main.add_widget(self.display)
        main.add_widget(self.result)

        grid = GridLayout(
            cols=4,
            spacing=8,
            size_hint_y=0.48
        )

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", ".", "+"
        ]

        for value in buttons:
            btn = Button(
                text=value,
                font_size=27,
                background_color=(0.35, 0.07, 0.02, 1),
                color=(1, 0.65, 0.1, 1)
            )
            btn.bind(on_press=self.press)
            grid.add_widget(btn)

        main.add_widget(grid)

        equal = Button(
            text="=  7seb lia",
            font_size=28,
            background_color=(1, 0.3, 0.02, 1),
            size_hint_y=0.13
        )
        equal.bind(on_press=self.calculate)
        main.add_widget(equal)

        root.add_widget(main)
        return root

    def press(self, instance):
        value = instance.text

        if value == "C":
            self.display.text = ""
            self.result.text = "Mar7ba bik HOUD!"
        else:
            self.display.text += value

    def calculate(self, instance):
        try:
            answer = safe_calc(self.display.text)
            self.result.text = f"HOUD - Natija: {answer}"
        except ZeroDivisionError:
            self.result.text = "Ma t9derch t9sem 3la zero!"
        except:
            self.result.text = "L7sab machi s7i7!"

HoudApp().run()
