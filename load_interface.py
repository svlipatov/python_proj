import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    # QWidget
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load params")
        self.centralWidget = QWidget()  # +++
        self.setCentralWidget(self.centralWidget)
        self.statusBar().showMessage("")
        # Создадим меню
        # Кнопка сохранить
        sAction = QAction('Save', self)
        sAction.setShortcut('Ctrl+S')
        sAction.setStatusTip('Save the document')
        sAction.triggered.connect(self.save_btn_click)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(sAction)

        self.containers_qua = 0
        self.btn_plus_dict = {}
        self.btn_num = 0
        self.low_num = 0
        self.entries = {}

        l =  QVBoxLayout(self.centralWidget)
        self.l = l
        p = QPixmap('filter.png')
        self.pic = QLabel(self)
        self.pic.adjustSize()
        self.pic.setPixmap(p)
        l.addWidget(self.pic)
        # Выпадающий список
        self.cbox = QComboBox()
        self.cbox.addItems(loads)
        self.cbox.currentIndexChanged.connect(self.ind_chng)
        l.addWidget(self.cbox)
        # Кнопка сохранения фильтров
        self.save_btn = QPushButton("Сохранить фильтры")
        self.save_btn.clicked.connect(self.save_btn_click)
        l.addWidget(self.save_btn)
        # Кнопка lобавления параметров
        self.btn = QPushButton("Добавить параметры выгрузки")
        self.btn.clicked.connect(self.btn_click)
        l.addWidget(self.btn)
        self.setLayout(l)
        # Сразу запускаем обработку
        self.ind_chng(self.cbox.currentIndex())
        # Список выгрузок
        self.left_list = QListWidget()
        self.l.addWidget(self.left_list)
        self.left_list.currentRowChanged.connect(self.display)
        self.stack = QStackedWidget(self)
        self.l.addWidget(self.stack)

    def ind_chng(self, i):
        # Обработчик изменения значения в выпадающем списке загрузок
        self.load = self.cbox.currentText()
        # Настройки выгрузки
        self.df_load_par = df_all_load_par[df_all_load_par['LOAD_NAME'] == self.load]

    def btn_click(self):
        # Добавление еще одного контейнера фильтров
        self.containers_qua += 1
        self.left_list.insertItem(0, 'Параметры выгрузки №' + str(self.containers_qua))
        setattr(self, 'container' + '_' + str(self.containers_qua), QWidget())
        self.container_ui()
        self.stack.addWidget(getattr(self, 'container' + '_' + str(self.containers_qua)))

    def container_ui(self):
        # Сборка контейнера фильтров
        layout = QFormLayout()
        for filter in self.df_load_par['FILTER']:
            layout_line = QHBoxLayout()
            label = QLabel(filter)
            # Стили
            label.setStyleSheet(
            'font-family: Times New Roman;'
            'font-size: 12px;'
            'font-weight: bold;')
            layout_line.addWidget(label)
            layout_line.addWidget(self.add_low(filter))
            layout_line.addWidget(self.add_button(layout, filter))
            layout_line.addWidget(self.add_button_minus(layout, layout.count()))
            layout.addRow(layout_line)
        att = getattr(self, 'container' + '_' + str(self.containers_qua))
        att.setLayout(layout)
    def display(self, i):
        # Отображение только нужного контейнера
        self.stack.setCurrentIndex(i)

    def add_row_btn(self,btn):
        # Добавление еще одной строки с фильтром для возможности указания нескольких значений
        btn_layout = self.btn_plus_dict[btn][0]
        btn_filter = self.btn_plus_dict[btn][1]
        layout_line = QHBoxLayout()
        label = QLabel(btn_filter)
        label.setStyleSheet(
            'font-family: Times New Roman;'
            'font-size: 12px;'
            'font-weight: bold;')
        layout_line.addWidget(label)
        layout_line.addWidget(self.add_low(btn_filter))
        layout_line.addWidget(self.add_button(btn_layout, btn_filter))
        layout_line.addWidget(self.add_button_minus(btn_layout, btn_layout.count()))
        btn_layout.addRow(layout_line)


    def add_button(self, bt_layout, bt_filter):
        # Создание кнопки добавления еще одной строки с фильтром
        self.btn_num += 1
        setattr(self, 'btn' + '_' + str(self.btn_num), QPushButton("+"))
        cur_btn = getattr(self, 'btn' + '_' + str(self.btn_num), QPushButton("+"))
        cur_btn.clicked.connect(lambda x: self.add_row_btn(cur_btn))
        self.btn_plus_dict[cur_btn] = [bt_layout, bt_filter]
        return cur_btn

    def add_low(self, bt_filter):
        # Создание элемента ввода значения фильтра
        self.low_num += 1
        setattr(self, 'low' + '_' + str(self.low_num), QLineEdit())
        cur_low = getattr(self, 'low' + '_' + str(self.low_num), QLineEdit())
        cur_low.textEdited.connect(lambda x: self.val_cngd_low(cur_low,bt_filter))
        return cur_low

    def val_cngd_low(self,low, filter):
        # Обработчик изменения значения фильтра
        low_value = low.text()
        self.entries[low] = [self.stack.currentIndex(), filter, low_value]

    def save_btn_click(self):
        # Обработчик кнопки сохранения фильтра
        data_list = []
        for lines in self.entries:
            data_list.append(self.entries[lines])
        df_filters = pd.DataFrame(data_list, columns = ['load_num', 'load_field', 'value'])
        df_filters.to_csv('filters/filter.csv', index=False)
        self.statusBar().showMessage('Фильтры сохранены')
        print(df_filters)

    def add_button_minus(self, bt_layout, num):
        # Создание кнопки добавления еще одной строки с фильтром
        setattr(self, 'btn_min' + '_' + str(self.btn_num), QPushButton("-"))
        cur_btn_min = getattr(self, 'btn_min' + '_' + str(self.btn_num), QPushButton("-"))
        cur_btn_min.clicked.connect(lambda x: self.delete_row(bt_layout, num))
        return cur_btn_min

    def delete_row(self, bt_layout, num):
        bt_layout.removeRow(num)


# Соответствие тех имени загрузки и ее возможных фильтров
df_all_load_par = pd.read_csv("load_parameters/params.csv", delimiter= ';')
loads = list(set(df_all_load_par['LOAD_NAME']))

app = QApplication([])
window = MainWindow()
window.show()

app.exec()


