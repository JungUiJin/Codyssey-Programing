import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('아이폰 스타일 계산기')
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 디스플레이
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet( 'padding: 10px;')
        font = QFont()               # 기본 시스템 글꼴 사용
        font.setPointSize(24)        # 글꼴 크기 설정
        self.display.setFont(font)
        self.display.setText('0')
        main_layout.addWidget(self.display)

        # 버튼 배치
        buttons_layout = QGridLayout()
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row_index, row in enumerate(buttons):
            col_offset = 0
            for col_index, button_text in enumerate(row):
                button = QPushButton(button_text)
                
                if button_text in '0123456789.':
                    button.setStyleSheet('background-color: #505050; color: white; font-size: 20px; border-radius: 30px;')
                elif button_text in ['+', '-', '×', '÷', '=']:
                    button.setStyleSheet('background-color: orange; color: white; font-size: 20px; border-radius: 30px;')
                else:  # 'AC', '+/-', '%'
                    button.setStyleSheet('background-color: #D4D4D2; color: black; font-size: 20px; border-radius: 30px;')

                if button_text == '0':
                    button.setFixedSize(140, 60)
                    buttons_layout.addWidget(button, row_index + 1, 0, 1, 2)
                    col_offset += 1
                else:
                    button.setFixedSize(60, 60)
                    buttons_layout.addWidget(button, row_index + 1, col_index + col_offset)

                button.clicked.connect(self.on_button_clicked)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    # 버튼 클릭
    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()
        current = self.display.text()

        if text == 'AC':
            self.display.setText('0')

        elif text == '=':
            if current and self.is_last_char_number(current):
                self.calculate()

        elif text == '+/-':
            if current and self.is_last_char_number(current):
                self.toggle_sign()

        elif text == '%':
            if current and self.is_last_char_number(current):
                self.display.setText(current + '%')

        elif text in ['+', '-', '×', '÷']:
            if self.is_last_char_number(current):
                self.display.setText(current + " " + text + " ")

        elif text == '.':
            if not current.endswith('.'):
                self.display.setText(current + '.')

        else:
            if current == '0':
                self.display.setText(text) 
            else:
                self.display.setText(current + text)
                
        self.adjust_font_to_fit(self.display.text())

    
    def is_last_char_number(self, text):
        return text[-1].isdigit() or text[-1] == ')'

    def apply_percentage(self):
        current = self.display.text()
        try:
            if current:
                value = str(float(current) / 100)
                self.display.setText(value)
        except Exception:
            self.display.setText('Error')
            
    def precedence(self, op):
        #연산자의 우선순위를 반환
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0
    
    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def infix_to_postfix(self, expression):
        #중위 표기식을 후위 표기식으로 변환
        stack = []
        postfix = []
        tokens = expression.strip().split()
        print(tokens)
        for token in tokens:
            if self.is_number(token):
                postfix.append(token)
            else:  # 연산자
                while stack and self.precedence(stack[-1]) >= self.precedence(token):
                    postfix.append(stack.pop())
                stack.append(token)
        
        while stack:
            postfix.append(stack.pop())

        return postfix

    def evaluate_postfix(self, postfix):
        #후위 표기식 계산
        stack = []
        
        for token in postfix:
            if self.is_number(token):
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(self.add(a, b))
                elif token == '-':
                    stack.append(self.subtract(a, b))
                elif token == '*':
                    stack.append(self.multiply(a, b))
                elif token == '/':
                    stack.append(self.devide(a, b))  # 정수 나눗셈
        if isinstance(stack[0], float) : 
            stack[0] = round(stack[0], 6)
        return str(stack[0])
    
    def add(self, a, b): return a + b
    def subtract(self, a ,b): return a - b
    def multiply(self, a, b): return a * b
    def devide(self, a, b): return a / b
    
    def calculate(self):
        expression = self.display.text()
        expression = expression.replace('×', '*').replace('÷', '/') # 연산기호로 변경경
        #전체 계산 실행
        postfix = self.infix_to_postfix(expression)
        self.display.setText(self.evaluate_postfix(postfix)) 

    def toggle_sign(self):
        current = self.display.text()
        try:
            if current:
                value = float(current)
                value = -value
                if value.is_integer():
                    self.display.setText(str(int(value)))
                else:
                    self.display.setText(str(value))
        except Exception:
            self.display.setText('Error')

    def adjust_font_to_fit(self, text):
        max_width = self.display.width() - 10  # 패딩 감안
        base_size = 24  # 시작 폰트 크기
        font = QFont()
        
        # 폰트 크기를 줄여가며 텍스트가 display 너비를 넘지 않을 때까지 반복
        for size in range(base_size, 10, -1):
            font.setPointSize(size)
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
            if text_width <= max_width:
                break

        self.display.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
