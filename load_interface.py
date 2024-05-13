import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load params")
        self.containers_qua = 0
        self.btn_plus_dict = {}
        self.btn_num = 0
        self.low_num = 0
        self.entries = {}

        l = QVBoxLayout()
        self.l = l
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
        print('container' + '_' + str(self.containers_qua))
        print(getattr(self, 'container' + '_' + str(self.containers_qua)))
        self.container_ui()
        self.stack.addWidget(getattr(self, 'container' + '_' + str(self.containers_qua)))

    def container_ui(self):
        # Сборка контейнера фильтров
        layout = QFormLayout()
        for filter in self.df_load_par['FILTER']:
            layout_line = QHBoxLayout()
            layout_line.addWidget(QLabel(filter))
            layout_line.addWidget(self.add_low(filter))
            layout_line.addWidget(self.add_button(layout, filter))
            layout.addRow(layout_line)
        att = getattr(self, 'container' + '_' + str(self.containers_qua))
        print('container' + '_' + str(self.containers_qua))
        print(att)
        att.setLayout(layout)
    def display(self, i):
        # Отображение только нужного контейнера
        self.stack.setCurrentIndex(i)

    def add_row_btn(self,btn):
        # Добавление еще одной строки с фильтром для возможности указания нескольких значений
        btn_layout = self.btn_plus_dict[btn][0]
        btn_filter = self.btn_plus_dict[btn][1]
        layout_line = QHBoxLayout()
        layout_line.addWidget(QLabel(btn_filter))
        layout_line.addWidget(self.add_low(btn_filter))
        layout_line.addWidget(self.add_button(btn_layout, btn_filter))
        btn_layout.addRow(layout_line)

    def add_button(self, bt_layout, bt_filter):
        # Создание кнопки добавления еще одной строки с фильтром
        self.btn_num += 1
        setattr(self, 'btn' + '_' + str(self.btn_num), QPushButton("+"))
        cur_btn = getattr(self, 'btn' + '_' + str(self.btn_num), QPushButton("+"))
        cur_btn.clicked.connect(lambda x: self.add_row_btn(cur_btn))
        print(cur_btn, bt_layout, bt_filter)
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
        print(df_filters)

# Соответствие тех имени загрузки и ее возможных фильтров
df_all_load_par = pd.read_csv("load_parameters/params.csv", delimiter= ';')
loads = list(set(df_all_load_par['LOAD_NAME']))

app = QApplication([])
window = MainWindow()
window.show()

app.exec()


