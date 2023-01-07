from tkinter import *
from tkinter import ttk
import json

import chatbot_testing as testpy
import chatbot_training as trainpy

# Constants
BG_GRAY = "#ABB2B9"
BG_COLOR = "#000"
TEXT_COLOR = "#FFF"
BUTTON_COLOR = '#3498DB'
ENTRY_COLOR = '#D6EAF8'
WIDGET_TEXT_COLOR = '#000'
WIDGET_BG_COLOR = '#FFF'
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatBot:
    def __init__(self):
        # initialize tkinter window
        self.window = Tk()
        self.main_window()
        self.test = testpy.Testing()
        
    def run(self):
        '''
        Run the chatbot

        args:
            None

        returns:
            None
        '''
        self.window.mainloop()
    
    def main_window(self):
        '''
        Configure the main window

        args:
            None

        returns:
            None
        '''
        # style tabs
        style = ttk.Style()
        style.theme_create( "MyStyle", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
                "TNotebook.Tab": {"configure": {"padding": [10, 10] },}})

        style.theme_use("MyStyle")

        # add title to window and configure it
        self.window.title("Stained Glass Chatbot")
        self.window.resizable(width = False, height = False)
        self.window.configure(width = 520, height = 520, bg = BG_COLOR)
        
        # add tab for Chatbot and Train Bot in Notebook frame
        self.tab = ttk.Notebook(self.window)
        self.tab.pack(expand = 1, fill = 'both')
        
        self.bot_frame = ttk.Frame(self.tab, width = 520, height = 520)
        self.train_frame = ttk.Frame(self.tab, width = 520, height = 520)
        
        self.tab.add(self.bot_frame, text='Stained Glass Bot'.center(100))
        self.tab.add(self.train_frame, text = 'Help Train Me Bot'.center(100))
        
        self.add_bot()
        self.add_train()
        
    
    def add_bot(self):
        '''
        Add the main chatbot to the window

        args:
            None

        returns:
            None
        '''
        # add heading to the Chabot window
        head_label = Label(self.bot_frame, bg = BG_COLOR, fg = TEXT_COLOR, 
                            text = "Welcome to Stained Glass Chatbot", font = FONT_BOLD, pady = 10)
        head_label.place(relwidth = 1)
        line = Label(self.bot_frame, width = 450, bg = BG_COLOR)
        line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        # create text widget where conversation will be displayed
        self.text_widget = Text(self.bot_frame, width = 20, height = 2,
                                bg = WIDGET_BG_COLOR, fg = WIDGET_TEXT_COLOR, font = FONT, 
                                padx = 5, pady = 5, wrap = WORD)
        self.text_widget.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.text_widget.insert(END, "Annabot: Welcome to Stained Glass Chatbot\nI will try to answer all your questions about Stained Glass.\n\n")
        self.text_widget.configure(cursor = "arrow", state = DISABLED)

        # create scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.configure(command = self.text_widget.yview)

        # create bottom label where message widget will placed
        bottom_label = Label(self.bot_frame, bg = BG_GRAY, height = 80)
        bottom_label.place(relwidth = 1,rely = 0.825)
        
        # this is for user to put query
        self.msg_entry = Entry(bottom_label, bg = ENTRY_COLOR, fg = WIDGET_TEXT_COLOR, font = FONT, borderwidth = 15, relief = FLAT)
        self.msg_entry.place(relwidth = 0.788, relheight = 0.06, rely = 0.008, relx = 0.008)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter)

        # send button which will call on_enter function to send the query
        send_button = Button(bottom_label, text = "Send", font = FONT_BOLD, width = 8,
                            bg = BUTTON_COLOR, command = lambda: self.on_enter(None))
        send_button.place(relx = 0.80, rely = 0.008, relheight = 0.06, relwidth = 0.20)

    def add_train(self):
        '''
        Add the trainingbot to the window

        args:
            None

        returns:
            None
        '''
        # Add heading to the Train Bot window
        head_label = Label(self.train_frame, bg = BG_COLOR, fg = TEXT_COLOR, text = "Help Train Me",
            font = FONT_BOLD, pady = 10)
        head_label.place(relwidth = 1)

        # Tag Label and Entry for intents tag. 
        tag_label = Label(self.train_frame, fg = WIDGET_TEXT_COLOR, text = "Subject", font = FONT)
        tag_label.place(relwidth = 0.2, rely = 0.14, relx = 0.008)
        self.tag = Entry(self.train_frame, bg = WIDGET_BG_COLOR, fg = WIDGET_TEXT_COLOR, font = FONT)
        self.tag.place(relwidth = 0.7, relheight = 0.06, rely = 0.14, relx = 0.22)

        # Pattern Label and Entry for pattern to our tag.
        self.pattern = []
        for i in range(2):
            pattern_label = Label(self.train_frame, fg = WIDGET_TEXT_COLOR, text = "Question %d"%(i + 1), font = FONT)
            pattern_label.place(relwidth = 0.2, rely = 0.28 + 0.08 * i, relx = 0.008)
            self.pattern.append(Entry(self.train_frame, bg = WIDGET_BG_COLOR, fg = WIDGET_TEXT_COLOR, font = FONT))
            self.pattern[i].place(relwidth = 0.7, relheight = 0.06, rely = 0.28 + 0.08 * i, relx = 0.22)

        # Response Label and Entry for response to our pattern.
        self.response = []
        for i in range(2):
            response_label = Label(self.train_frame, fg = WIDGET_TEXT_COLOR, text = "Answer %d"%(i + 1), font = FONT)
            response_label.place(relwidth = 0.2, rely = 0.50 + 0.08 * i, relx = 0.008)
            self.response.append(Entry(self.train_frame, bg = WIDGET_BG_COLOR, fg = WIDGET_TEXT_COLOR, font = FONT))
            self.response[i].place(relwidth = 0.7, relheight = 0.06, rely = 0.50 + 0.08 * i, relx = 0.22)

        # To train our bot create Train Bot button which will call on_train function
        bottom_label = Label(self.train_frame, bg = BG_GRAY, height = 80)
        bottom_label.place(relwidth = 1, rely = 0.825)

        train_button = Button(bottom_label, text = "Train Me", font = FONT_BOLD, width = 12, bg = BUTTON_COLOR, 
            command = lambda: self.on_train(None))
        train_button.place(relx = 0.20, rely = 0.008, relheight = 0.06, relwidth = 0.60)
    
    def on_train(self, event):
        '''
        Read and append the new trainingbot to the intent file

        args:
            event

        returns:
            None
        '''
        # clear text when Train button is pressed
        def clear_add_train_text():
            self.tag.delete(0, END)
            for i in range(2):
                self.pattern[i].delete(0, END)
            for i in range(2):
                self.response[i].delete(0, END)

        # read intent file and append created tag, pattern and responses from add_train function
        with open('intents.json','r+') as json_file:
            file_data = json.load(json_file)

            # get pattern and responses from training bot
            patterns = [i.get() for i in self.pattern]
            responses = [i.get() for i in self.response]

            # remove empty patterns and responses
            patterns = list(filter(None, patterns))
            responses = list(filter(None, responses))

            # append tag, patterns, and responses to intents.json file
            file_data['intents'].append({
                "tag": self.tag.get(),
                "patterns": patterns,
                "responses": responses,
                "context": ""
            })
            json_file.seek(0)
            json.dump(file_data, json_file, indent = 1)
        
        # run and compile model from our training.py file.
        train = trainpy.Training()
        train.build()

        print("Trained Successfully")
        clear_add_train_text()
        self.test = testpy.Testing()
        
    def on_enter(self, event):
        '''
        When enter pressed, get query and bot response

        args:
            None

        returns:
            None
        '''
        # get user query and bot response
        msg = self.msg_entry.get()

        self.my_msg(msg, "You")
        self.bot_response(msg, "Annabot")
        
    def bot_response(self, msg, sender):
        '''
        Get bot response and put into sender's window

        args:
            msg (str)
            sender (str)

        returns:
            None
        '''
        # get the response for the user's query from testing.py file
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, f"{str(sender)}: {self.test.response(msg)}\n\n")
        self.text_widget.configure(state = DISABLED)
        self.text_widget.see(END)
    
    def my_msg(self, msg, sender):
        '''
        Get user query and put into sender's window

        args:
            msg (str)
            sender (str)

        returns:
            None
        '''
        # if no msg then exit
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, f"{str(sender)}: {str(msg)}\n")
        self.text_widget.configure(state = DISABLED)
        
# Main Program
if __name__ == "__main__":
    bot = ChatBot()
    bot.run()
