from PySide2 import QtWidgets

class MiHerramienta(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi primera herramienta")
        self.resize(300, 200)

        # Layout vertical — organiza los widgets de arriba a abajo
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Campo de texto
        self.campo = QtWidgets.QLineEdit()
        self.campo.setPlaceholderText("Escribe un nombre...")
        layout.addWidget(self.campo)

        # Botón
        self.boton = QtWidgets.QPushButton("Ejecutar")
        self.boton.clicked.connect(self.al_hacer_click)
        layout.addWidget(self.boton)

        # Etiqueta de resultado
        self.resultado = QtWidgets.QLabel("Esperando...")
        layout.addWidget(self.resultado)

    def al_hacer_click(self):
        texto = self.campo.text()
        self.resultado.setText(f"Nombre introducido: {texto}")

app = QtWidgets.QApplication([])
ventana = MiHerramienta()
ventana.show()
app.exec_()