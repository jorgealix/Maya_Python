from PySide6 import QtWidgets
import maya.cmds as cmds

class Renombrador(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Renombrador")
        self.resize(300, 150)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.campo = QtWidgets.QLineEdit()
        self.campo.setPlaceholderText("Nuevo nombre...")
        layout.addWidget(self.campo)

        boton = QtWidgets.QPushButton("Renombrar selección")
        boton.clicked.connect(self.renombrar)
        layout.addWidget(boton)

        self.resultado = QtWidgets.QLabel("")
        layout.addWidget(self.resultado)

    def renombrar(self):
        seleccion = cmds.ls(selection=True)
        if not seleccion:
            self.resultado.setText("No hay nada seleccionado")
            return
        nuevo_nombre = self.campo.text()
        if not nuevo_nombre:
            self.resultado.setText("Escribe un nombre primero")
            return
        cmds.rename(seleccion[0], nuevo_nombre)
        self.resultado.setText(f"Renombrado a: {nuevo_nombre}")

ventana = Renombrador()
ventana.show()