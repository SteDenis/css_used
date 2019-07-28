import cssutils
from stat import *
import os
from cssselect.xpath import SelectorError
from lxml import etree, cssselect
import lxml.html as lh
import logging
from tkinter import filedialog
import tkinter as tk
from tkinter.ttk import Frame, Button, Style, Progressbar
import threading

cssutils.log.setLevel(logging.CRITICAL)
cwd = os.getcwd()

class Interface():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Used CSS checker")
        self.root.geometry("830x730")
        #self.root.resizable(False, False)
        self.style = Style()
        self.style.theme_use("classic")
        self.html_dir = None
        self.css_dir = None
        self.index_css = 0
        self.result = []
        self.deep_css = tk.IntVar()

        frame = tk.Frame(self.root, width=830, height=720)
        frame.pack(fill=tk.X, side=tk.TOP, pady=10)

        frame_left = tk.Frame(frame)
        frame_left.grid(row=0, column=0, padx=20)

        txt1 = tk.Label(frame_left, text="CSS files list", font=('calibri', 10), pady=5, anchor='w')
        txt1.grid(row=0, column=0)

        self.list = tk.Listbox(frame_left, height=32)
        self.list.grid(row=1, column=0)
        self.list.bind('<<ListboxSelect>>', self.onselect_css)

        content_css = tk.Frame(frame, width=300, height=550, padx=5)
        content_css.grid(row=0, column=1)
        self.txt = tk.Text(content_css, borderwidth=3, relief="sunken", width=55, height=40)
        self.txt.config(font=("consolas", 9), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scrollb = tk.Scrollbar(content_css, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        frame_right = tk.Frame(frame)
        frame_right.grid(row=0, column=2)

        txt2 = tk.Label(frame_right, text="HTML Directory :", font=('calibri', 9), pady=5, anchor='w')
        txt2.grid(row=0, column=0)

        self.btn_html = Button(frame_right, width="13", text="Browse", command=self.browse_html_dir)
        self.btn_html.grid(row=1, column=0)
        txt3 = tk.Label(frame_right, text="CSS Directory :", font=('calibri', 9), pady=5, anchor='w')
        txt3.grid(row=2, column=0)
        self.btn_css = Button(frame_right, width="13", text="Browse", command=self.browse_css_dir)
        self.btn_css.grid(row=3, column=0)

        opt = tk.LabelFrame(frame_right, text="Options", padx=20, pady=20)
        opt.grid(row=4, column=0)
        deep_css = tk.Checkbutton(opt, text="Deep search CSS", variable=self.deep_css)
        deep_css.pack()


        actions = tk.Frame(frame_right)
        actions.grid(row=6, column=0, pady=160)

        self.btn_start = Button(actions, width="13", text="Start", command=self.start)
        self.btn_start.grid(row=0, column=0, pady=5)
        self.btn_start['state']='disabled'

        self.btn_reset = Button(actions, width="13", text="Reset", command=self.reset)
        self.btn_reset.grid(row=1, column=0)

        self.btn_save = Button(actions, width="13", text="Save Results", command=self.save)
        self.btn_save.grid(row=2, column=0)
        self.btn_save['state']='disabled'

        self.progress = Progressbar(frame, orient=tk.HORIZONTAL,length=550,  mode='indeterminate')
        self.progress.grid(row=10,column=0, columnspan=3, pady=2)
    def save(self):
        self.btn_save['state']='disabled'
        file = open("result.txt", "w")
        sep = "\n"
        for index,data in enumerate(self.result):
            file.write("\nFile : " + self.list.get(index) + "\n\n")
            file.write(sep.join(self.result[index]))
            file.write("\n\n")


    def reset(self):
        self.btn_save['state']='disabled'
        self.html_dir = None
        self.css_dir = None
        self.btn_html.config(text='Browse')
        self.btn_css.config(text='Browse')
        self.index_css = 0
        self.result = []
        self.list.delete(0,tk.END)

    def browse_html_dir(self):
        file = filedialog.askdirectory(initialdir = cwd, title = "Select HTML directory")
        if file:
            self.html_dir = file
            self.btn_html.config(text=self.html_dir.split("/")[-1])
            if self.css_dir:
                self.btn_start['state']='normal'

    def browse_css_dir(self):
        file = filedialog.askdirectory(initialdir = cwd, title = "Select CSS directory")
        if file:
            self.css_dir = file
            self.btn_css.config(text=self.css_dir.split("/")[-1])
            if self.html_dir:
                self.btn_start['state']='normal'

    def onselect_css(self, event):
        w = event.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
            value = w.get(index)
            sep = '\n'
            self.txt.config(state=tk.NORMAL)
            self.txt.delete('1.0', tk.END)
            self.txt.insert(tk.END, sep.join(self.result[index]))

    def start(self):
        def real_traitement():
            self.progress.start()
            res = self.read_dir_html(self.html_dir)
            self.read_dir_css(self.css_dir, res)
            self.progress.stop()
            self.btn_save['state']='normal'

        self.btn_start['state']='disabled'
        threading.Thread(target=real_traitement).start()

    def selector_exists(self, html, selector):
        try:
            if cssselect.CSSSelector(
                    selector,
                    translator='html'
            )(html):
                return True
        except SelectorError:
            return False
        return False

    def read_dir_html(self, directory):
        result = []
        for content in os.listdir(directory):
            pathname = os.path.join(directory, content)
            mode = os.stat(pathname).st_mode
            if S_ISDIR(mode):
                result = result + self.read_dir_html(pathname)
            elif content.endswith('.html'):
                file = open(pathname)
                result.append(lh.fromstring(file.read()))
        return result

    def start_check(self, page, css):
        tmp = []
        for rule in css:
            try:
                name = rule.selectorText
                if name:
                    if ":" in name:
                        name = name.split(':')[0]
                    if self.selector_exists(page, name) == True:
                        tmp.append(name)
            except AttributeError as e:
                pass
        return tmp

    def read_dir_css(self, css_path, page_list):
        for content in os.listdir(css_path):
            pathname = os.path.join(css_path, content)
            mode = os.stat(pathname).st_mode
            if self.deep_css.get() and S_ISDIR(mode):
                self.read_dir_css(pathname, page_list)
            elif content.endswith('.css'):
                tmp = []
                css = cssutils.parseFile(pathname)
                self.list.insert(self.index_css, content)
                self.index_css += 1
                for page in page_list:
                    tmp = list(set(tmp + self.start_check(page, css)))
                self.result.append(tmp)

if __name__ == "__main__":
    inter = Interface()
inter.root.mainloop()

