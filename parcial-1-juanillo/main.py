import requests
from pokemon import Pokemon
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys


class DetailsWindow(QMainWindow):
    def __init__(self, pokemon: Pokemon):
        super().__init__()

        self.layout_principal = QVBoxLayout()
        self.layout_image_and_description = QVBoxLayout()
        self.page = 0
        self.pokemon_type = ''

        self.label_name = QLabel()
        self.label_description = QLabel()
        self.label_type = QLabel(f'Tipo:{self.pokemon_type}')

        self.layout_principal.addLayout(self.layout_image_and_description)

        widget = QWidget()
        widget.setLayout(self.layout_principal)
        self.setCentralWidget(widget)

    def load_image(self, pokemon_image):
        self.image_data = requests.get(pokemon_image).content
        pixmap = QPixmap()
        pixmap.loadFromData(self.image_data)
        self.image = QLabel()
        self.image.setPixmap(pixmap)
        self.image.setFixedWidth(300)
        self.image.setFixedHeight(300)
        self.image.setScaledContents(True)
        self.layout_image_and_description.addWidget(self.image)

    def render_widget(self, pokemon: Pokemon):
        pokemon.get_data()
        self.setWindowTitle(pokemon.name)
        self.load_image(pokemon.image)
        self.label_name.setText(pokemon.name)
        self.label_description.setText(pokemon.description)
        self.layout_image_and_description.addWidget(self.label_name)
        self.layout_image_and_description.addWidget(self.label_description)
        self.layout_image_and_description.addWidget(self.label_type)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout_principal = QVBoxLayout()
        self.layout_pokemon_list = QHBoxLayout()
        self.grid_info = QGridLayout()
        self.layout_buttons_page = QHBoxLayout()
        self.page = 0
        self.page_modify = 0
        self.count_pages = 1

        self.label_pokemon_list = QLabel('Listado de Pokemon:')
        self.layout_pokemon_list.addWidget(self.label_pokemon_list)

        self.function(self.page)

        self.btn_previous = QPushButton('Atras')
        self.label_pages = QLabel(f'{self.count_pages} de 65')
        self.btn_next = QPushButton('Siguiente')

        self.layout_buttons_page.addWidget(self.btn_previous)
        self.layout_buttons_page.addWidget(self.label_pages)
        self.layout_buttons_page.addWidget(self.btn_next)

        self.btn_previous.clicked.connect(self.atras)
        self.btn_next.clicked.connect(self.siguiente)

        self.layout_principal.addLayout(self.layout_pokemon_list)
        self.layout_principal.addLayout(self.grid_info)
        self.layout_principal.addLayout(self.layout_buttons_page)

        self.widget = QWidget()
        self.widget.setLayout(self.layout_principal)
        self.setCentralWidget(self.widget)

    def function(self, page):
        self.page = page
        pokemon_list = Pokemon.get_pokemon_list(self.page)
        fila = 0
        columna = 0
        for pokemon in pokemon_list:
            self.grid_info.addWidget(PokemonButton(Pokemon(pokemon.name, pokemon.url)), fila, columna)
            columna += 1
            if columna > 1:
                fila += 1
                columna = 0

    def siguiente(self):
        self.page_modify += 1
        if self.count_pages == 65:
            self.count_pages = 65
            self.label_pages.setText(f'{self.count_pages} de 65')
        elif 1 <= self.count_pages <= 65:
            self.count_pages += 1
            self.label_pages.setText(f'{self.count_pages} de 65')
            self.function(self.page_modify)

    def atras(self):
        self.page_modify -= 1
        if self.count_pages == 1:
            self.count_pages = 1
            self.label_pages.setText(f'{self.count_pages} de 65')
        elif 1 <= self.count_pages <= 65:
            self.count_pages -= 1
            self.label_pages.setText(f'{self.count_pages} de 65')
            self.function(self.page_modify)


class PokemonButton(QPushButton):
    def __init__(self, pokemon: Pokemon):
        super().__init__()
        self.pokemon = pokemon
        self.setText(pokemon.name)
        self.clicked.connect(self.open_window)
        self.details_window = DetailsWindow(Pokemon(pokemon.name, pokemon.url))

    def open_window(self):
        self.details_window.render_widget(self.pokemon)
        self.details_window.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



