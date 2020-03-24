from tkinter import Frame, Tk, Label, E, W, Button, OptionMenu, StringVar, Entry, LabelFrame, Toplevel
from difflib import SequenceMatcher
from sys import exit, stdout
import logging
import argparse
import socket
import json
import os


class GUIFrame(Frame, object):
    def __init__(self, master, database_file):
        """
        For Creating the GUI for Remote Desktop Monitor
        :param master:
        """
        super(GUIFrame, self).__init__(master)
        self.master = master
        self.logger = self.setup_logger("MapFileReportGeneration", "log.log")
        self.machine_name = socket.gethostname()
        self.machine_ip = socket.gethostbyname(self.machine_name)
        self.logger.info("Running In Machine {0} For IP {1}".format(self.machine_name, self.machine_ip))
        self.database_file = database_file
        self.database = self.get_json_data(self.database_file)
        self.header = LabelFrame(self, text="REMOTE DESKTOP MONITOR", bg="white")
        self.header.grid(row=0, column=0, sticky=E + W, padx=5, pady=5)
        self.static_data()
        self.label_data = LabelFrame(self.header, text="USER NAME", bg="white")
        self.label_data.grid(row=0, column=0, columnspan=2, sticky=E + W, padx=5, pady=5)
        self.option_variable = StringVar(self)
        self.option_variable.set(self.database["USERS"][0])  # default value
        option_menu = OptionMenu(self.label_data, self.option_variable, *self.database["USERS"])
        option_menu.grid(row=1, column=0)

        Button(self.header, text="SUBMIT", command=self.submit, bg="green").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        Button(self.header, text="NEW USER", command=self.update_user, bg="green").grid(row=1, column=1, sticky=W,padx=5, pady=5)

    def static_data(self):
        header = LabelFrame(self, text="MACHINE INFO", bg="white")
        header.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        Label(header, text="MACHINE NAME : " + self.machine_name, borderwidth=2, relief="groove").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        Label(header, text="MACHINE IP : " + self.machine_ip, borderwidth=2, relief="groove").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        if self.machine_ip in self.database["MACHINES"].keys():
            Label(header, text="LAST USER : " + self.database["MACHINES"][self.machine_ip][1], borderwidth=2, relief="groove").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        else:
            Label(header, text="LAST USER : --------------------", borderwidth=2, relief="groove").grid(row=3, column=0, sticky=W, padx=5, pady=5)

    def update_user(self):
        self.logger.info("Registering New User")
        root = PopUpWindow(self, self.database["USERS"])
        self.master.wait_window(root.root)
        self.database["USERS"] = root.users
        self.submit(root.user)

    def submit(self, new_user=None):
        if new_user:
            user = new_user
        else:
            user = self.option_variable.get()
        self.logger.info("Updating Data For User {0}".format(user))
        if user == "SELECT USER":
            self.label_data.config(highlightbackground="red", highlightcolor="red", highlightthickness=3)
            return None
        self.label_data.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
        if self.machine_ip in self.database["MACHINES"].keys():
            if user != self.database["MACHINES"][self.machine_ip][1]:
                self.database["MACHINES"][self.machine_ip] = [self.machine_name, user, self.database["MACHINES"][self.machine_ip][1]]
        else:
            self.database["MACHINES"][self.machine_ip] = [self.machine_name, user, "--------------------"]
        self.save_file(self.database_file, self.database)
        self.master.quit()
        exit()

    def get_json_data(self, input_file):
        self.logger.info("Getting Config Data from {0}".format(input_file))
        with open(input_file) as json_file:
            input_data = json.load(json_file)
        return input_data

    def save_file(self, name, data):
        self.logger.info("Saving... Updated {0}".format(name))
        with open(name, "w") as writer:
            writer.write(json.dumps(data, indent=4))

    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""
        screen = logging.StreamHandler(stdout)
        screen.setLevel(logging.DEBUG)
        screen_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        screen.setFormatter(screen_formatter)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(log_file, "w")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)
        logger.addHandler(screen)
        return logger


class PopUpWindow(object):
    def __init__(self, master, users):
        self.root = Toplevel(master)
        self.root.attributes('-topmost', True)
        self.root.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
        self.root.resizable(width=False, height=False)
        self.root.geometry("400x135+300+300")
        self.root.overrideredirect(1)
        self.root.title("RemoteDesktopMonitor")
        self.new_user = True
        self.user = ""
        self.users = users
        self.popup_header = LabelFrame(self.root, text="Enter New User Name", bg="white")
        self.popup_header.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        self.entry = Entry(self.popup_header)
        self.entry.grid(row=0, column=0, columnspan=2, sticky=E + W, padx=5, pady=5)
        Button(self.popup_header, text='UPDATE', command=self.cleanup, bg="green").grid(row=1, column=0, sticky=E + W, padx=5, pady=5)
        Button(self.popup_header, text='RETURN', command=lambda: self.root.destroy(), bg="green").grid(row=1, column=1, sticky=E + W, padx=5, pady=5)

    def cleanup(self):
        user = self.entry.get()
        if user == "" or len(user) < 4:
            self.popup_header.config(highlightbackground="red", highlightcolor="red", highlightthickness=3)
            return None
        for each in self.users:
            if SequenceMatcher(None, each.lower(), user.lower()).ratio() > 0.8:
                self.new_user = False
                self.user = each
        if self.new_user:
            self.user = user
            self.users.append(self.user)
        self.popup_header.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
        self.root.destroy()


class QuietPeriodUpdate(object):
    def __init__(self, database_file):
        self.logger = self.setup_logger("MapFileReportGeneration", "log.log")
        self.database_file = database_file
        self.database = self.get_json_data(self.database_file)
        self.machine_name = socket.gethostname()
        self.machine_ip = socket.gethostbyname(self.machine_name)
        self.logger.info("Running In Machine {0} For IP {1}".format(self.machine_name, self.machine_ip))
        self.submit()

    def submit(self, user="--------------------"):
        self.logger.info("Updating Data For User {0}".format(user))
        if self.machine_ip in self.database["MACHINES"].keys():
            if user != self.database["MACHINES"][self.machine_ip][1]:
                self.database["MACHINES"][self.machine_ip] = [self.machine_name, user, self.database["MACHINES"][self.machine_ip][1]]
        else:
            self.database["MACHINES"][self.machine_ip] = [self.machine_name, user, "--------------------"]
        self.save_file(self.database_file, self.database)
        exit()

    def get_json_data(self, input_file):
        self.logger.info("Getting Config Data from {0}".format(input_file))
        with open(input_file) as json_file:
            input_data = json.load(json_file)
        return input_data

    def save_file(self, name, data):
        self.logger.info("Saving... Updated {0}".format(name))
        with open(name, "w") as writer:
            writer.write(json.dumps(data, indent=4))

    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""
        screen = logging.StreamHandler(stdout)
        screen.setLevel(logging.DEBUG)
        screen_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        screen.setFormatter(screen_formatter)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(log_file, "w")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)
        logger.addHandler(screen)
        return logger


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Inputs')
    PARSER.add_argument('-d', '--database', help='No Inputs : GUI Mode and Default Database\n Input: DataBase Path', required=False)
    PARSER.add_argument('-m', '--manual_user', help='Provide True For Updating Quiet Period Data', required=False)
    ARGS = PARSER.parse_args()
    if ARGS.database:
        DATABASE_FILE = ARGS.database
    else:
        DATABASE_FILE = "DesktopDataBase.json"
        if not os.path.exists(DATABASE_FILE):
            open(DATABASE_FILE, "w").write(json.dumps({"USERS":["SELECT USER"], "MACHINES":{}}, indent=4))
    if ARGS.manual_user:
        QuietPeriodUpdate(DATABASE_FILE)
        exit()
    ROOT = Tk()
    ROOT.attributes('-topmost', True)
    ROOT.config(highlightbackground="green", highlightcolor="green", highlightthickness=1)
    ROOT.resizable(width=False, height=False)
    ROOT.geometry("400x135+300+300")
    ROOT.overrideredirect(1)
    ROOT.title("RemoteDesktopMonitor")
    FRAME = GUIFrame(master=ROOT, database_file=DATABASE_FILE)
    FRAME.grid(sticky=E)
    ROOT.mainloop()
