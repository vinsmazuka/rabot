import tkinter
import easygui
import rabot
import app_logger
from core import DbWriter, DbFormatter, CsvReader, DbLoader, CsvWriter, DbChanger
from core import Worker, Schedule, DbEraser

logger = app_logger.get_logger(__name__)
logger.info('Модуль админ запущен')


class AdmMessanger:
    """
    предназначен для вывода сообщений для администратора на экран
    админского интерфейса
    """
    pass

    @staticmethod
    def show_message(message):
        """
        выводит сообщение для администратора на экран админского интерфейса
        """
        root = tkinter.Toplevel()
        root.title('Сообщение для администратора:')
        root.geometry("1200x400")
        lbl = tkinter.Label(root,
                            text=message,
                            font="Arial 10"
                            )
        lbl.pack()
        root.mainloop()

    @staticmethod
    def show_messages(messages):
        """
        выводит окно с сообщениями для администратора
        :param messages - кортеж из сообщений в формате str
        """
        root = tkinter.Toplevel()
        root.title('Не корректный формат данных:')
        root.geometry("1200x400")
        for i, value in enumerate(messages):
            locals()['lbl' + str(i)] = tkinter.Label(root,
                                                     text=value,
                                                     font="Arial 10",
                                                     )
            locals()['lbl' + str(i)].pack(anchor="w")
        root.mainloop()

    @staticmethod
    def delete_month(data):
        """
        открывает окно, в котором администратор может выбрать месяц,
        который будет удален из бызы данных
        :param data: список состоящий из кортежей, каждый кортеж состоит из
        2 элементов, 1 элемент - название месяца, 2 - соответствующий месяцу год
        """
        def save():
            """
            возвращает месяц, выбранный администратором из списка data
            и передает его данные в метод del_schedule класса DbEraser для удаления
            из БД, затем открывает окно с сообщением для администратора
            """
            nonlocal root, selector, selected_month
            user_input = selector.curselection()[0]
            selected_month = selector.get(user_input)
            root.destroy()
            AdmMessanger.show_message(DbEraser.del_schedule(*selected_month))

        selected_month = ()
        root = tkinter.Toplevel()
        root.title('Выберите 1 месяц из списка')
        root.geometry("400x600")
        selector = tkinter.Listbox(root, height=len(data))
        for element in data:
            selector.insert(tkinter.END, element)
        btn = tkinter.Button(root,
                             text="save",
                             width=23,
                             height=3,
                             bg="white",
                             fg="blue",
                             command=lambda: save())
        selector.pack()
        btn.pack()
        root.mainloop()

    @staticmethod
    def delete_worker(data):
        """
        открывает окно, в котором администратор может выбрать сотрудника
        из списка
        :param data: список состоящий из кортежей, каждый кортеж состоит из
        3 элементов: 1 - элемент - id сотрудника в БД, 2 - фамилия сотрудника,
        3 - имя сотрудника
        """
        def save():
            """
            возвращает сотрудника, выбранного администратором из списка data
            и передает его данные в метод del_worker класса DbEraser для удаления
            из БД, затем открывает окно с сообщением для администратора
            """
            nonlocal root, selector, selected_worker
            user_input = selector.curselection()[0]
            selected_worker = selector.get(user_input)
            root.destroy()
            AdmMessanger.show_message(DbEraser.del_worker(selected_worker[0]))

        selected_worker = ()
        root = tkinter.Toplevel()
        root.title('Выберите сотрудника из списка')
        root.geometry("400x600")
        selector = tkinter.Listbox(root, height=len(data))
        for element in data:
            selector.insert(tkinter.END, element)
        btn = tkinter.Button(root,
                             text="save",
                             width=23,
                             height=3,
                             bg="white",
                             fg="blue",
                             command=lambda: save())
        selector.pack()
        btn.pack()
        root.mainloop()

    @staticmethod
    def set_status(data, status=False):
        """
        открывает окно, в котором администратор может выбрать сотрудника
        из списка
        :param data: список состоящий из кортежей, каждый кортеж состоит из
        3 элементов: 1 - элемент - id сотрудника в БД, 2 - фамилия сотрудника,
        3 - имя сотрудника
        :param status: значение, которое необходимо утановить в БД в поле
        "status" в таблице "workers" по сотруднику
        """
        def save():
            """
            возвращает сотрудника, выбранного администратором из списка data
            и передает его данные и значение аргумента status
            в метод change_status класса DbChanger для
            изменения поля "status" по сотруднику в БД,
            затем открывает окно с сообщением для администратора
            """
            nonlocal root, selector, selected_worker, status
            user_input = selector.curselection()[0]
            selected_worker = selector.get(user_input)
            root.destroy()
            AdmMessanger.show_message(DbChanger.change_status(selected_worker[0], status))

        selected_worker = ()
        root = tkinter.Toplevel()
        root.title('Выберите сотрудника из списка')
        root.geometry("400x600")
        selector = tkinter.Listbox(root, height=len(data))
        for element in data:
            selector.insert(tkinter.END, element)
        btn = tkinter.Button(root,
                             text="save",
                             width=23,
                             height=3,
                             bg="white",
                             fg="blue",
                             command=lambda: save())
        selector.pack()
        btn.pack()
        root.mainloop()


def add_worker(data):
    """
    записиывает работника в БД если data - список,
    либо выводит сообщение о некорректном формате данных,
    если data - кортеж
    """
    if isinstance(data, tuple):
        AdmMessanger.show_messages(data)
    else:
        DbWriter.write_worker_db(data)
        AdmMessanger.show_message('была осуществлена запись в таблицу "workers" в БД')


def add_schedule(data):
    """
    записивает график в БД если data - список,
    либо выводит сообщение о некорректном формате данных,
    если data - кортеж
    """
    if isinstance(data, tuple):
        AdmMessanger.show_messages(data)
    else:
        DbWriter.write_schedule_db(data)
        AdmMessanger.show_message('была осуществлена запись в таблицу "schedule" в БД')


def write_file_csv(func):
    """
    записывает данные в CSV-файл,
    выводит окно с сообщением для администратора
    :param func: - функция, которая записывает данные
    в файл и возвращает сообщение в формате str
    """
    if func is None:
        pass
    else:
        AdmMessanger.show_message(func)


def inp_path():
    """
    :return: аозвращает путь к файлу, указанному администратором
    """
    return easygui.fileopenbox("укажите путь к файлу")


def menu():
    """Создает главное меню администраторского интерфейса"""
    main_window = tkinter.Tk()
    main_window.title('Администраторский интерфейс бота')
    main_window.geometry("1300x600")
    lbl1 = tkinter.Label(main_window,
                         text='выберите опцию:',
                         font="Arial 14")
    btn_m0 = tkinter.Button(main_window,
                            text="Добавить работников в БД",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: add_worker(DbFormatter.format_worker(CsvReader.read_file
                                                       (inp_path()))))
    btn_m1 = tkinter.Button(main_window,
                            text="Добавить график в БД",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: add_schedule(DbFormatter.format_schedule
                                                         (CsvReader.read_file(inp_path()), DbLoader.load_workers_id())))
    btn_m2 = tkinter.Button(main_window,
                            text="Записать работников\n"
                                 "из БД в файл",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: write_file_csv(CsvWriter.write_worker
                                                           (inp_path(), DbLoader.load_table(Worker))))
    btn_m3 = tkinter.Button(main_window,
                            text="Записать график\n"
                                 "из БД в файл",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: write_file_csv(CsvWriter.write_schedules
                                                           (inp_path(), DbLoader.load_table(Schedule))))
    btn_m4 = tkinter.Button(main_window,
                            text="Удалить график за\n"
                                 "месяц из БД",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: AdmMessanger.delete_month(DbLoader.load_months()))
    btn_m5 = tkinter.Button(main_window,
                            text="Удалить сотрудника\n"
                                 "из БД",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: AdmMessanger.delete_worker(DbLoader.load_workers()))
    btn_m6 = tkinter.Button(main_window,
                            text="Заблокировать сотрудника",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: AdmMessanger.set_status(DbLoader.load_workers()))
    btn_m7 = tkinter.Button(main_window,
                            text="Разблокировать сотрудника",
                            width=23,
                            height=3,
                            bg="white",
                            fg="blue",
                            command=lambda: AdmMessanger.set_status(DbLoader.load_workers(), True))
    lbl1.place(relx=0.00001, rely=0.001)
    btn_m0.place(relx=0.00001, rely=0.06)
    btn_m1.place(relx=0.00001, rely=0.15)
    btn_m2.place(relx=0.00001, rely=0.24)
    btn_m3.place(relx=0.00001, rely=0.33)
    btn_m4.place(relx=0.00001, rely=0.42)
    btn_m5.place(relx=0.00001, rely=0.51)
    btn_m6.place(relx=0.00001, rely=0.60)
    btn_m7.place(relx=0.00001, rely=0.69)
    main_window.mainloop()


if __name__ == "__main__":
    menu()









