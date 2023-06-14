import tkinter as tk
import socket
import threading
import sys

class GUI:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.nickname = None
        self.serv_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_obj.connect((self.host, self.port))
        self.win = tk.Tk()
        self.win.geometry("380x380")
        self.win.title("Tkinter Chat App")
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.listbox = tk.Listbox(self.win, width=40, height=15)
        self.listbox.pack(fill=tk.X, padx = 15, pady=15)
        self.msg_var = tk.StringVar()

        self.messageBox = tk.Entry(self.win,textvariable=self.msg_var)
        # self.messageBox.pack(self.win, height=3, padx=50)
        self.messageBox.bind("<Return>",self.send)
        self.messageBox.pack()
        self.receive_thread = threading.Thread(target = self.receive)
        self.receive_thread.start()
        self.win.mainloop()
        self.serv_obj.close()

    def send(self, event=None):
        self.serv_obj.send(f"{self.nickname}: {self.msg_var.get()}".encode("utf-8"))

    def close(self,event=None):
        print("Closing down!")
        # self.receive_thread.join()
        self.serv_obj.send("quit".encode('utf-8'))
        self.serv_obj.close()
        self.win.destroy()

    def receive(self):
        while True:
            try:
                data = self.serv_obj.recv(4096).decode('utf-8')
                if data.startswith("Nickname"):
                    self.nickname = data.split(' ')[1]
                    print(self.nickname)
                    self.listbox.insert(tk.END, 'Succesfully registered!')
                else:
                    self.listbox.insert(tk.END, data)
            except Exception as e:
                break

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8000
    gui = GUI('localhost',port)