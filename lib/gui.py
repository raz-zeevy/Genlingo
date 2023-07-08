import tkinter as tk
import ttkbootstrap as ttk
import lib.const as const
from tkinter import messagebox
import os

t_ENTRY_LABEL = 'Insert phrpychases/words delimited by a row: '
DEFAULT_DECK_NAME = 'New Words'
p_ASSETS = r'lib\assets'

WINDOW_WIDTH = 435
WINDOW_HEIGHT = 380
y_l_ENTRY = 10
x_l_ENTRY = 25
y_ENTRY = 35
x_ENTRY = 25
x_SIDE = 300
y_BOTTOM = 335
y_PRS_WRDS_BTN = 75
x_PRS_WRDS_BTN = x_SIDE + 5
y_WORD_PICKER = 120
x_CREATE_DCK_BTN = 70
y_CREATE_DCK_BTN = y_BOTTOM
y_DECK_NAME = y_BOTTOM-35
s_METER = 120
y_WORD_METER = 170
x_WORD_METER = x_SIDE - 10

f_ENTRY_lABLE = ("Arial-BoldMT", int(11.0))
f_ENTRY = ("Arial-BoldMT", int(11.0))
w_ENTRY = 30
h_ENTRY = 14


class GUI():
    def __init__(self):
        self.root = tk.Tk()
        # logo = tk.PhotoImage(file=os.path.join(p_ASSETS,"icon.gif"))
        # self.root.call('wm', 'iconphoto', '354x44',logo)
        self.root.wm_iconbitmap(bitmap=os.path.join(p_ASSETS, 'icon.ico'))
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title('Genlingo')
        self.draw_frame(self.root)

    def draw_frame(self, master):
        # Word Entry: Text, Label, Parse Words Button
        self.l_word_entry = ttk.Label(master, text=t_ENTRY_LABEL,
                                      font=f_ENTRY_lABLE)
        self.l_word_entry.place(x=x_l_ENTRY, y=y_l_ENTRY)
        self.word_entry = tk.Text(master, width=w_ENTRY, height=h_ENTRY)
        self.word_entry.configure(font=f_ENTRY)
        self.word_entry.place(x=x_ENTRY, y=y_ENTRY)
        self.parse_btn = ttk.Button(master, text="Parse Words",
                                    bootstyle="info-outline",
                                    command=self.click_parse)
        self.parse_btn.place(x=x_PRS_WRDS_BTN, y=y_PRS_WRDS_BTN)
        # Create Deck Label
        self.creat_btn = ttk.Button(master, text="Create Deck",
                                    bootstyle="success-outline",
                                    width=25)
        self.creat_btn.place(x=x_CREATE_DCK_BTN, y=y_CREATE_DCK_BTN)
        self.creat_btn.state(["disabled"])
        # Deck Name Entry
        self.deck_name_entry = tk.Entry(master, width=w_ENTRY-10,
                                        font=f_ENTRY,
                                        bg='white', fg='black',
                                        highlightbackground='black',
                                        highlightcolor='black',
                                        highlightthickness=5)
        self.deck_name_entry.place(x=x_ENTRY+90, y=y_DECK_NAME)
        self.deck_name_entry.insert(0, DEFAULT_DECK_NAME)
        # Deck Name Label
        self.l_deck_name = ttk.Label(master, text="Deck Name:",
                                        font=f_ENTRY_lABLE)
        self.l_deck_name.place(x=x_l_ENTRY, y=y_DECK_NAME)
        # Words Meter
        self.word_meter = ttk.Meter(bootstyle="info", metersize=s_METER,
                                    textfont='-size 15 -weight bold',
                                    subtext='words', subtextfont='-size 8')
        self.word_meter.place(x=x_WORD_METER, y=y_WORD_METER)
        # Language
        self.lang_picker = self.draw_lang_picker(x=x_SIDE, y=y_WORD_METER,
                                                 value='asd')
        # self.change_meter()
        # open deck folder
        self.open_search_folder_img = tk.PhotoImage(
            file=os.path.join(p_ASSETS, "open_folder.png"))
        self.open_search_folder = tk.Button(
            image=self.open_search_folder_img,
            text='',
            compound='center',
            fg='white',
            borderwidth=0,
            highlightthickness=0,
            relief='flat')

        self.open_search_folder.place(
            x=x_SIDE + 90, y=15,
            width=24,
            height=22)

    def draw_lang_picker(self, x, y, values=None, value=None,
                         width=120, \
                         height=60,
                         y_offset=30,
                         x_offset=15):
        self.root.option_add("*TCombobox*Listbox*Font", f_ENTRY)
        combobox = ttk.Combobox(self.root, bootstyle="info", width=width,
                                font=f_ENTRY_lABLE, state="readonly")
        combobox['values'] = values
        combobox.place(x=x_SIDE, y=y_WORD_PICKER, width=width - x_offset,
                       height=height - y_offset)

        return combobox

    def set_lang_picker(self, values, value=None):
        self.lang_picker['values'] = values
        values = values
        if value:
            val_ind = values.index(value)
            self.lang_picker.current(val_ind)

    def click_parse(self):
        words = self.word_entry.get("1.0", tk.END)
        return words

    def change_entry_text(self, text):
        self.word_entry.delete("1.0", tk.END)
        self.word_entry.insert("1.0", text)

    def set_meter(self, total):
        self.word_meter['amounttotal'] = total
        self.word_meter['amountused'] = total

    def update_meter(self, used=None, theme=None,strip=None):
        if used is not None:
            self.word_meter['amountused'] = used
        if theme:
            self.word_meter['bootstyle'] = theme
        if strip:
            self.word_meter['stripethickness'] = strip

    def reset_inputs(self):
        self.update_meter(used=0)
        self.change_entry_text('')

    def run(self):
        self.root.mainloop()

    @staticmethod
    def show_msg(msg_type, words=None, name=None):
        msg = msg_type
        if isinstance(msg_type, Exception):
            msg = msg_type.args[0] if len(
                list(msg_type.args)) == 1 else msg_type
        if msg_type == const.DeckCreationSuccess:
            tk.messagebox.showinfo(title='Deck Created Successfully',
                                   message=f'"{name}.apkg" created with'
                                           f' {len(words)} notes')
        else:
            tk.messagebox.showerror(title='Unknown Error', message=msg)


if __name__ == '__main__':
    gui = GUI()
