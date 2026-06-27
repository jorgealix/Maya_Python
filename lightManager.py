from PySide6 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds

class GestorLuces(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Luces")
        self.resize(300, 500)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        boton_refresh = QtWidgets.QPushButton("Refrescar luces")
        boton_refresh.clicked.connect(self.cargar_luces)
        layout.addWidget(boton_refresh)

        self.lista = QtWidgets.QListWidget()
        self.lista.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lista.itemSelectionChanged.connect(self.al_seleccionar)
        layout.addWidget(self.lista)

        # Intensidad
        layout.addWidget(QtWidgets.QLabel("Intensidad:"))
        self.slider_intensidad = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_intensidad.setMinimum(0)
        self.slider_intensidad.setMaximum(100)
        self.slider_intensidad.valueChanged.connect(lambda v: self.label_intensidad.setText(str(v)))
        self.slider_intensidad.sliderReleased.connect(self.cambiar_intensidad)
        layout.addWidget(self.slider_intensidad)
        self.label_intensidad = QtWidgets.QLabel("0")
        layout.addWidget(self.label_intensidad)

        # Exposure
        layout.addWidget(QtWidgets.QLabel("Exposure:"))
        self.slider_exposure = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_exposure.setMinimum(-10)
        self.slider_exposure.setMaximum(10)
        self.slider_exposure.valueChanged.connect(lambda v: self.label_exposure.setText(str(v)))
        self.slider_exposure.sliderReleased.connect(self.cambiar_exposure)
        layout.addWidget(self.slider_exposure)
        self.label_exposure = QtWidgets.QLabel("0")
        layout.addWidget(self.label_exposure)

        # Color
        layout.addWidget(QtWidgets.QLabel("Color:"))
        self.boton_color = QtWidgets.QPushButton("Seleccionar color")
        self.boton_color.clicked.connect(self.cambiar_color)
        layout.addWidget(self.boton_color)

        self.resultado = QtWidgets.QLabel("")
        layout.addWidget(self.resultado)

        self.cargar_luces()

    def cargar_luces(self):
        self.lista.clear()
        luces = cmds.ls(type=["aiAreaLight", "aiSkyDomeLight", "aiLightPortal", "aiPhotometricLight"])
        if not luces:
            self.resultado.setText("No hay luces en la escena")
            return
        for luz in luces:
            self.lista.addItem(luz)

    def luces_seleccionadas(self):
        return [item.text() for item in self.lista.selectedItems()]

    def al_seleccionar(self):
        luces = self.luces_seleccionadas()
        if not luces:
            return
        cmds.select(luces)

        # Leemos valores de la primera luz
        primera = luces[0]
        self.slider_intensidad.setValue(int(cmds.getAttr(f"{primera}.intensity")))
        self.slider_exposure.setValue(int(cmds.getAttr(f"{primera}.exposure")))
        color = cmds.getAttr(f"{primera}.color")[0]
        self._actualizar_boton_color(color)

        self.resultado.setText(f"{len(luces)} luz(es) seleccionada(s)")

    def cambiar_intensidad(self):
        valor = self.slider_intensidad.value()
        for luz in self.luces_seleccionadas():
            cmds.setAttr(f"{luz}.intensity", valor)

    def cambiar_exposure(self):
        valor = self.slider_exposure.value()
        for luz in self.luces_seleccionadas():
            cmds.setAttr(f"{luz}.exposure", valor)

    def cambiar_color(self):
        luces = self.luces_seleccionadas()
        if not luces:
            return
        color_actual = cmds.getAttr(f"{luces[0]}.color")[0]
        qcolor_inicial = QtGui.QColor(
            int(color_actual[0] * 255),
            int(color_actual[1] * 255),
            int(color_actual[2] * 255)
        )
        color = QtWidgets.QColorDialog.getColor(qcolor_inicial, self)
        if color.isValid():
            r, g, b = color.redF(), color.greenF(), color.blueF()
            for luz in luces:
                cmds.setAttr(f"{luz}.color", r, g, b, type="double3")
            self._actualizar_boton_color((r, g, b))

    def _actualizar_boton_color(self, color):
        r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
        self.boton_color.setStyleSheet(f"background-color: rgb({r},{g},{b})")

try:
    gestor_luces.close()
    gestor_luces.deleteLater()
except:
    pass

gestor_luces = GestorLuces()
gestor_luces.show()