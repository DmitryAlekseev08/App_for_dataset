import sys
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QFileDialog, QMainWindow, QTableWidgetItem, QDialog, \
    QApplication

from Main_window import Ui_MainWindow
from Add_delete_window import Intent_Dialog
from Change_window import Change_Intent_Dialog


class Classification(QMainWindow):
    def __init__(self):
        super(Classification, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # info - это словарь, содержащий информацию о датасете (кол-во интентов, вопросов и ответов)
        self.info = {}
        self.ui.list_intents.itemClicked.connect(self.current_intent)
        self.ui.text_questions.textChanged.connect(self.change_questions)
        self.ui.text_answers.textChanged.connect(self.change_answers)

        self.ui.button_add.clicked.connect(self.add_intent)
        self.ui.button_delete.clicked.connect(self.delete_intent)
        self.ui.button_edit.clicked.connect(self.change_intent)
        self.ui.menu.addAction("Создать", self.new_file)
        self.ui.menu.addAction("Открыть", self.open_file)
        self.ui.menu.addAction("Сохранить", self.save_changes)
        self.ui.menu.addAction("Сохранить как", self.save_changes_how)
        self.ui.menu.addAction("Выход", self.close)
        self.ui.info_menu.addAction('Функции программы', self.app_function)
        self.ui.info_menu.addAction('Сохранение по умолчанию', self.save_function)

        self.ui.info_data.setColumnCount(2)
        self.ui.info_data.setRowCount(3)
        self.ui.info_data.setColumnWidth(0, 200)
        self.ui.info_data.setColumnWidth(1, 99)
        self.ui.info_data.setRowHeight(0, 36)
        self.ui.info_data.setRowHeight(1, 36)
        self.ui.info_data.setRowHeight(2, 36)
        self.ui.info_data.setHorizontalHeaderItem(0, QTableWidgetItem('Характеристика'))
        self.ui.info_data.setHorizontalHeaderItem(1, QTableWidgetItem('Значение'))
        self.ui.info_data.setItem(0, 0, QTableWidgetItem('Кол-во интентов'))
        self.ui.info_data.setItem(1, 0, QTableWidgetItem('Кол-во утверждений'))
        self.ui.info_data.setItem(2, 0, QTableWidgetItem('Кол-во ответов'))
        self.new_file()

    # Изменение вариантов вопросов (утверждений)
    def change_questions(self):
        # source_text - датасет
        self.source_text['intents'][self.cur_item]['examples'] = str(self.ui.text_questions.toPlainText()).split('\n')
        self.info_dataset()

    # Изменение вариантов ответов
    def change_answers(self):
        self.source_text['intents'][self.cur_item]['responses'] = str(self.ui.text_answers.toPlainText()).split('\n')
        self.info_dataset()

    # Выбор интента
    def current_intent(self, item: QListWidgetItem):
        # cur_item - текущий интент, информация о котором отображается в форме
        self.cur_item = item.text()
        self.info_dataset()
        self.ui.text_questions.setText('\n'.join(self.source_text['intents'][self.cur_item]['examples']))
        self.ui.text_answers.setText('\n'.join(self.source_text['intents'][self.cur_item]['responses']))

    # Добавление интента
    def add_intent(self):
        # self.dialog = Intent_Dialog()
        # dialog.intent_operation = 'add'
        # self.dialog.show()
        # Открытие формы для добавления интента
        self.dialog = QDialog()
        ui = Intent_Dialog('add')
        ui.setupUi(self.dialog)
        self.dialog.exec_()
        new_intent = ui.name_intent
        if new_intent:
            if not self.source_text['intents']:
                self.ui.list_intents.addItem(new_intent)
                self.source_text['intents'][new_intent] = {}
                self.source_text['intents'][new_intent]['examples'] = ''
                self.source_text['intents'][new_intent]['responses'] = ''
                self.info_dataset()
            elif new_intent not in self.source_text['intents'].keys():
                self.ui.list_intents.addItem(new_intent)
                self.source_text['intents'][new_intent] = {}
                self.source_text['intents'][new_intent]['examples'] = ''
                self.source_text['intents'][new_intent]['responses'] = ''
                self.info_dataset()
            else:
                QMessageBox.critical(self, "Ошибка ", "Интент с таким именем уже есть в списке.", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы не ввели название интента.", QMessageBox.Ok)

    # Удаление интента
    def delete_intent(self):
        # Открытие формы для удаления интента
        self.dialog = QDialog()
        ui = Intent_Dialog('delete')
        ui.setupUi(self.dialog)
        self.dialog.exec_()
        del_intent = ui.name_intent
        if del_intent:
            if not self.source_text['intents']:
                QMessageBox.critical(self, "Ошибка ", "Нет возможности удалить интент. Список интентов пуст.",
                                     QMessageBox.Ok)
            elif del_intent in self.source_text['intents'].keys():
                del self.source_text['intents'][del_intent]
                self.ui.list_intents.clear()
                self.ui.list_intents.addItems(self.source_text['intents'])
                self.info_dataset()
            else:
                QMessageBox.critical(self, "Ошибка ", "Данного интента нет в списке.", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы не ввели название интента.", QMessageBox.Ok)

    # Изменение названия интента
    def change_intent(self):
        # Открытие формы для изменения названия интента
        self.dialog = QDialog()
        ui = Change_Intent_Dialog()
        ui.setupUi(self.dialog)
        self.dialog.exec_()
        new_name = ui.new_name
        old_name = ui.old_name
        if new_name and old_name:
            if not self.source_text['intents']:
                QMessageBox.critical(self, "Ошибка ", "Нет возможности переименовать интент, так как список пуст.",
                                     QMessageBox.Ok)
            elif new_name in self.source_text['intents'].keys():
                QMessageBox.critical(self, "Ошибка ", "Интент с таким именем уже существует.", QMessageBox.Ok)
            elif old_name not in self.source_text['intents'].keys():
                QMessageBox.critical(self, "Ошибка ", "Интент с таким именем отсутствует в списке.", QMessageBox.Ok)
            else:
                self.source_text['intents'][new_name] = {}
                self.source_text['intents'][new_name]['examples'] = self.source_text['intents'][old_name]['examples']
                self.source_text['intents'][new_name]['responses'] = self.source_text['intents'][old_name]['responses']
                del self.source_text['intents'][old_name]
                self.ui.list_intents.clear()
                self.ui.list_intents.addItems(self.source_text['intents'])
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы не ввели название(-я) интента(-ов).", QMessageBox.Ok)

    # Вывод информации о датасете
    def info_dataset(self):
        if self.cur_item:
            self.info['count_intent'] = len(self.source_text['intents'])
            self.info['count_questions'] = len(self.source_text['intents'][self.cur_item]['examples'])
            self.info['count_answers'] = len(self.source_text['intents'][self.cur_item]['responses'])
        else:
            self.info['count_intent'] = 0
            self.info['count_questions'] = 0
            self.info['count_answers'] = 0

        self.ui.info_data.setItem(0, 1, QTableWidgetItem(str(self.info['count_intent'])))
        self.ui.info_data.setItem(1, 1, QTableWidgetItem(str(self.info['count_questions'])))
        self.ui.info_data.setItem(2, 1, QTableWidgetItem(str(self.info['count_answers'])))

    # Сохранение изменений
    def save_changes(self):
        dict_intent = self.source_text['intents']
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                f.write("{'intents': {")
                for intent in self.source_text['intents']:
                    f.write("'" + intent + "': {'examples': ['" + "', '".join(dict_intent[intent]['examples'])
                            + "'], 'responses': ['" + "', '".join(dict_intent[intent]['responses']) + "']}, ")
                f.write("}}")
        except Exception:
            QMessageBox.critical(self, "Ошибка ", "Не удаётся сохранить данные в файл.", QMessageBox.Ok)

    # Обработка нажатия "Сохранить как"
    def save_changes_how(self):
        self.save_file = QFileDialog.getSaveFileName(self)[0]
        self.save_changes()

    # Обрабока нажатия "Открыть"
    def open_file(self):
        self.save_file = QFileDialog.getOpenFileName(self)[0]
        try:
            f = open(self.save_file, 'r', encoding='utf-8')
            ftext = eval(f.read())
            self.ui.list_intents.addItems(ftext['intents'])
            self.source_text = ftext
            self.cur_item = list(self.source_text['intents'])[0]
            self.ui.text_answers.setText('\n'.join(self.source_text['intents'][self.cur_item]['responses']))
            self.ui.text_questions.setText('\n'.join(self.source_text['intents'][self.cur_item]['examples']))
            self.info_dataset()
            f.close()
        except Exception:
            QMessageBox.critical(self, "Ошибка ", "Не удаётся прочесть данные из файла.", QMessageBox.Ok)

    # Обработка нажатия "Создать"
    def new_file(self):
        self.source_text = {'intents': {}}
        self.save_file = 'Dataset.txt'
        self.cur_item = None
        self.info_dataset()

    # Обработка нажатия "Функции программы"
    def app_function(self):
        QMessageBox.information(self, "Функции программы", "  Данная программа позволяет создавать и редактировать "
                                                           "датасет для нейронной сети, занимающейся обработкой "
                                                           "естесственного языка.\n  Функции программы:\n◦ добавлять, "
                                                           "удалять, переименовывать намерения (интенты);\n◦ "
                                                           "добавлять, удалять и изменять возможные варианты "
                                                           "вопросов пользователя и ответов НС.", QMessageBox.Ok)

    # Обработка нажатия "Сохранение по умолчанию"
    def save_function(self):
        QMessageBox.information(self, "Сохранение по умолчанию", "При нажатии Файл->Сохранить сохранение происходит "
                                                                 "следующим образом:\n◦ если датасет был полностью "
                                                                 "создан в данной программе,то сохранение выполняется "
                                                                 "в файл Dataset.txt\n◦ если датасет был открыт из "
                                                                 "файла, то сохранение выполняется в этот же файл.",
                                QMessageBox.Ok)


app = QApplication(sys.argv)
application = Classification()
application.show()
sys.exit(app.exec_())
