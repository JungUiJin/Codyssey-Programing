import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
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
        self.display.setStyleSheet('font-size: 24px; padding: 10px;')
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
            self.calculate_result()

        elif text == '+/-':
            self.toggle_sign()

        elif text == '%':
            if current and self.is_last_char_number(current):
                self.display.setText(current + '%')

        elif text in ['+', '-', '×', '÷']:
            if self.is_last_char_number(current):
                self.display.setText(current + text)

        elif text == '.':
            if not current.endswith('.'):
                self.display.setText(current + '.')

        else:
            if current == '0':
                self.display.setText(text) 
            else:
                self.display.setText(current + text)
    
    def is_last_char_number(self, text):
        return text[-1].isdigit() or text[-1] == ')'

    # 정답 계산
    def calculate_result(self): 
        try:
            expression = self.display.text()
            if self.is_last_char_number(expression):
                expression = expression.replace('×', '*').replace('÷', '/') # 연산기호로 변경경
                result = str(eval(expression))
                self.display.setText(result)
        except Exception:
            self.display.setText('Error')

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

    def apply_percentage(self):
        current = self.display.text()
        try:
            if current:
                value = str(float(current) / 100)
                self.display.setText(value)
        except Exception:
            self.display.setText('Error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
