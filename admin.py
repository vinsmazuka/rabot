import tkinter
import easygui
import rabot
import app_logger
from core import DbWriter, DbFormatter, CsvReader

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
        root.title('Не корректный формат данных:')
        root.geometry("1200x400")
        lbl = tkinter.Label(root,
                            text=message,
                            font="Arial 10",
                            )
        lbl.pack()
        root.mainloop()


def add_worker(data):
    """
    записиывает работника в БД если data - список,
    либо выводит сообщение о некорректном формате данных,
    если data - кортеж
    """
    if isinstance(data, tuple):
        root = tkinter.Toplevel()
        root.title('Не корректный формат данных:')
        root.geometry("1200x400")
        for i, value in enumerate(data):
            locals()['lbl' + str(i)] = tkinter.Label(root,
                                                     text=value,
                                                     font="Arial 10",
                                                     )
            locals()['lbl' + str(i)].pack(anchor="w")
        root.mainloop()
    else:
        DbWriter.write_worker(data)


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
                                                       (easygui.fileopenbox("укажите путь к файлу")))))
    lbl1.place(relx=0.00001, rely=0.001)
    btn_m0.place(relx=0.00001, rely=0.06)
    main_window.mainloop()


if __name__ == "__main__":
    menu()











