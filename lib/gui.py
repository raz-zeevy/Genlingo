import tkinter as tk
import ttkbootstrap as ttk
import lib.const as const
from tkinter import messagebox
import os

s_WORD_METER = 15
pxs_WORD_METER = s_WORD_METER * 8

t_ENTRY_LABEL = 'Insert phrases/words delimited by a row'
DEFAULT_DECK_NAME = 'New Words'
f_ICON = 'icon.ico'
p_ASSETS = r'lib\assets'
ROOT_TITLE = 'Genlingo'

# fonts
f_MAIN_lABLE = ("Arial-BoldMT", int(11.0))
f_ENTRY_lABLE = ("Arial-BoldMT", int(11.0), "bold")
f_ENTRY = ("Arial-BoldMT", int(11.0))

# General Sizes
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 420
x_SIDE = 580
y_BOTTOM = 380

# Main Panel
y_MAIN_LBL = 20
x_MAIN_LBL = 25
# Word Entry
w_ENTRY = 30
y_WRD_ENTRY = 75
size_ENTRY = w_ENTRY * 8.5
x_LFT_WRD_ENTRY = x_MAIN_LBL
x_RT_WRD_ENTRY = x_LFT_WRD_ENTRY + size_ENTRY + 10
t_RIGHT_ENTRY_LBL = "Target \u2192 Native"
t_LFT_ENTRY_LBL = "Native \u2192 Target"
x_LFT_WRD_ENTRY_LBL = x_LFT_WRD_ENTRY + size_ENTRY / 2 - len(
    t_LFT_ENTRY_LBL) * 4.5
x_RT_WRD_ENTRY_LBL = x_RT_WRD_ENTRY + size_ENTRY / 2 - len(
    t_RIGHT_ENTRY_LBL) * 4.5
h_WORD_ENTRY = 14
# Bottom Panel
x_CREATE_DCK_BTN = x_SIDE / 2 - 100
y_CREATE_DCK_BTN = y_BOTTOM
CREATE_DECK_BTN_w = 25
#
t_DECK_NAME_LBL = "Deck Name:"
y_DECK_NAME_LBL = 10
x_DECK_NAME_LBL = x_CREATE_DCK_BTN - 35
y_DECK_NAME = y_BOTTOM-35
x_DECK_NAME_ENTRY = x_CREATE_DCK_BTN + len(t_DECK_NAME_LBL) * 5 + 5
w_DECK_NAME_ENTRY = w_ENTRY - 10
# Side Panel
y_LANG_PICKER = 120
#
y_WORD_METER = 170
y_CLEAR_BTN = y_WORD_METER + pxs_WORD_METER + 10
x_WORD_METER = x_SIDE - 10
s_METER = 120
# Parse Words Button
y_PARSE_WRDS_BTN = 75
x_PARSE_WRDS_BTN = x_SIDE + 5

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_iconbitmap(bitmap=os.path.join(p_ASSETS, f_ICON))
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title(ROOT_TITLE)
        self.draw_frame(self.root)

    def draw_frame(self, master):
        """
        Draw the entire frame
        """
        # Main Panel: Main Label, Entry Label, Entries
        self.draw_main_panel(master)
        # Side Panel: Language Picker, Word Meter, Parse Words Button
        self.draw_side_panel(master)
        # Bottom Panel: Create Deck Button, Deck Name Entry, Deck Name Label
        self.draw_btm_panel(master)

    def draw_main_panel(self, master):
        """Main Panel: Main Label, Entry Label, Entries"""
        # labels
        self.main_lbl = ttk.Label(master, text=t_ENTRY_LABEL,
                                  font=f_MAIN_lABLE)
        self.main_lbl.place(x=x_RT_WRD_ENTRY_LBL-len(t_ENTRY_LABEL)*5,
                            y=y_MAIN_LBL)
        #
        self.left_entry_lbl = ttk.Label(master, text=t_LFT_ENTRY_LBL,
                                        font=f_ENTRY_lABLE,)
        self.left_entry_lbl.place(x=x_LFT_WRD_ENTRY_LBL, y=y_WRD_ENTRY - 25)
        #
        self.right_entry_lbl = ttk.Label(master, text=t_RIGHT_ENTRY_LBL,
                                         font=f_ENTRY_lABLE)
        self.right_entry_lbl.place(x=x_RT_WRD_ENTRY_LBL, y=y_WRD_ENTRY - 25)
        #####
        self.word_entry = tk.Text(master, width=w_ENTRY, height=h_WORD_ENTRY)
        self.word_entry.configure(font=f_ENTRY)
        self.word_entry.place(x=x_LFT_WRD_ENTRY, y=y_WRD_ENTRY)
        self.rev_word_entry = tk.Text(master, width=w_ENTRY,
                                      height=h_WORD_ENTRY)
        self.rev_word_entry.configure(font=f_ENTRY)
        self.rev_word_entry.place(x=x_RT_WRD_ENTRY, y=y_WRD_ENTRY)


    def draw_side_panel(self, master):
        """Side Panel: Language Picker, Word Meter, Parse Words Button"""
        # parse button
        self.parse_btn = ttk.Button(master, text="Parse Words",
                                    bootstyle="info-outline",
                                    command=self.click_parse)
        self.parse_btn.place(x=x_PARSE_WRDS_BTN, y=y_PARSE_WRDS_BTN)
        # Language
        self.lang_picker = self.draw_lang_picker(x=x_SIDE, y=y_WORD_METER,
                                                 value='asd')
        # open deck folder
        self.deck_folder_img = tk.PhotoImage(
            file=os.path.join(p_ASSETS, "open_folder.png"))
        self.deck_folder = tk.Button(
            image=self.deck_folder_img,
            text='',
            compound='center',
            fg='white',
            borderwidth=0,
            highlightthickness=0,
            relief='flat')
        self.deck_folder.place(
            x=x_SIDE + 90, y=15,
            width=24,
            height=22)
        # Words Meter
        self.word_meter = ttk.Meter(bootstyle="info", metersize=s_METER,
                                    textfont=(f'-size {s_WORD_METER}'
                                              f' -weight bold'),
                                    subtext='words', subtextfont='-size 8')
        self.word_meter.place(x=x_WORD_METER, y=y_WORD_METER)
        # clear button
        self.clear_btn = ttk.Button(master, text="Clear Words",
                                    bootstyle="secondary-outline",
                                    command=self.click_parse)
        self.clear_btn.place(x=x_PARSE_WRDS_BTN, y= y_CLEAR_BTN)

    def draw_btm_panel(self, master):
        """Bottom Panel: Create Deck Button, Deck Name Entry, Deck Name
        Label"""
        # Create Deck Button
        self.creat_btn = ttk.Button(master, text="Create Deck",
                                    bootstyle="success-outline",
                                    width=CREATE_DECK_BTN_w)
        self.creat_btn.place(x=x_CREATE_DCK_BTN, y=y_CREATE_DCK_BTN)
        self.creat_btn.state(["disabled"])
        # Deck Name Entry
        self.deck_name_entry = tk.Entry(master, width=w_DECK_NAME_ENTRY,
                                        font=f_ENTRY,
                                        bg='white', fg='black',
                                        highlightbackground='black',
                                        highlightcolor='black',
                                        highlightthickness=5)
        self.deck_name_entry.place(x=x_DECK_NAME_ENTRY, y=y_DECK_NAME)
        self.deck_name_entry.insert(0, DEFAULT_DECK_NAME)
        # Deck Name Label
        self.l_deck_name = ttk.Label(master, text=t_DECK_NAME_LBL,
                                     font=f_MAIN_lABLE)
        self.l_deck_name.place(x=x_DECK_NAME_LBL, y=y_DECK_NAME)

    def draw_lang_picker(self, x, y, values=None, value=None,
                         width=120, \
                         height=60,
                         y_offset=30,
                         x_offset=15):
        self.root.option_add("*TCombobox*Listbox*Font", f_ENTRY)
        combobox = ttk.Combobox(self.root, bootstyle="info", width=width,
                                font=f_MAIN_lABLE, state="readonly")
        combobox['values'] = values
        combobox.place(x=x_SIDE, y=y_LANG_PICKER, width=width - x_offset,
                       height=height - y_offset)

        return combobox

    def set_lang_picker(self, values, value=None):
        self.lang_picker['values'] = values
        values = values
        if value:
            val_ind = values.index(value)
            self.lang_picker.current(val_ind)

    def click_parse(self):
        reg_words = self.word_entry.get("1.0", tk.END)
        rev_words = self.rev_word_entry.get("1.0", tk.END)
        return reg_words, rev_words

    def change_entries_text(self, text, side=None):
        if side != 'rev':
            self.word_entry.delete("1.0", tk.END)
            self.word_entry.insert("1.0", text)
        if side != 'reg':
            self.rev_word_entry.delete("1.0", tk.END)
            self.rev_word_entry.insert("1.0", text)

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
        self.change_entries_text('')

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
