import tkinter as tk
import textwrap
from tkinter.ttk import Scrollbar

class InstructionsTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        yscrollbar = Scrollbar(self, orient=tk.VERTICAL)
        self.instructions = tk.Text(self, bg='white', relief='raised', wrap='word', yscrollcommand=yscrollbar.set)
        self.instructions.config(height=600, width=400, state='disabled', tabstyle='tabular', padx=25, pady=5)
        self.instructions.grid(column=0, row=0, sticky='nsew')
        yscrollbar.config(command=self.instructions.yview)
        yscrollbar.grid(column=1, row=0, sticky='ns')

        message = """First of all - Disclaimer! Backup copies of your GCODE files before using in this application.  \
        This application is still in development and may have bugs that could cause damage to your GCODE files, \
        cause them to call tools incorrectly, crash your machine or cause any other number of issues. The author \
        assumes no responsibility for any damage caused by this application in any form. Use at your own risk!\n\n
        This application is called GGCODE and is meant to help users \
        make minor edits to GCODE files.\n\n \
        
        The left core layout is a text pane that displays the GCODE file. \
        An attempt was made to color code the text to make it easier to read.\n\n
        
        There are also '<-Tool' and 'Tool->' buttons that will seek to the \
        previous or next tool change in the file.\n\n
        
        The following is a list of features: \n
        1. N-Code Renumbering All, Isolation to Tool Change or Removal \n
        2. Tapping Cycle Conversion To Repeat Rigid Tapping using G95 (IPR) \n
        3. Altering Tool Numbers and Corresponding H and D Values \n
        4. Altering Work Offsets and updating the corresponding probing cycle 'S' values. \n
        
        General Instructions:\n
        To get started, please first click the file tab and select a G-Code File.  \
        Then press 'initial scan' to scan the file and enable the rest of the features. \n\n
        
        As you navigate through the tabs and make changes, you need to complete the choices \
        in each tab and click 'Send To File' before advancing to the next tab otherwise \
        choices may be lost.\n\n
        
        The choices you make will be reflected in the left text pane.\n\n
        
        *Note: For the Tapping, Tool Data and Work Offset Tabs, you first save a 'log' of your desired edits\n\n \
        by pressing 'Store Changes' after selections have been made.  When you have finally made all of your\
        edits you press 'Send To File'.\
        
        'FILE' Tab Features:\n\n
        1. Select a G-Code File
        2. Click 'Initial Scan' to parse document and enable other features.
        3. Activate Textbox to edit left text pane manually.
        4. Deactivate Textbox to lock it once more (recommended).
        
        'RENUMBER' Tab Features:
        1. Select a Renumbering Option
         a) No Change
         b) Remove All N-Codes
         c) Renumber All N-Codes
         d) Renumber and Place Only At Tool Changes
         
        2. Select and Increment if Desired (DEFAULT 10)
        3. Enter a max number of digits if your control has a max number and 
        will error out if exceeded. (DEFAULT 99999)
        4. Enter the starting number if desired.  (DEFAULT 10)
        5. Click 'Send To File' to send changes to the left text pane.
        
        'TAPPING' Tab Features:
        1. Select a Tool Number
        2. Select 'True' or 'False'
        3. Select a Tap Depth
        4. Press 'Store Changes' to store changes in the log.
        5. Press 'Send To File' to send changes to the left text pane.
        *Note: For the application to recognize the type of tap (pitch size) you must
        add a comment in parenthesis the line before the tool change for the tap. 
        Example: (1/4-20 TAP) *important to add the word 'TAP' in the comment.
        
        'TOOL DATA' Tab Features:
        1. First combo box must be selected in conjunction with 'Send Changes To File' if you want an
        initial tool list generated and placed after the program line O#####.
        2. Select a Tool Radio Button
        3. Select ComboBox 'Update Tool Comments' If you want to update the tool comments with what you enter
        4. Enter in tool change information along with metrics such as DIA, LOC, FL, TYPE, OAL, etc.
        5. Click 'Store Changes' to store changes in the log and review.
        6. Click 'Send Changes To File' to send changes to the left text pane when you have completed all changes.
        
        'WORK OFFSETS' Tab Features:
        1. Select a Work Offset Radio Button
        2. Enter In Work Offset Information *INCLUDE THE 'G' in the entry
        3. Click 'Store Changes' to store changes in the log and review.
        4. Click 'Send Changes To File' to send changes to the left text pane when you have completed all changes.
        *Note this application supports G54-G59 and G154 P1 - P99
        
        Please log issues on the GitHub page for this project, my profile. https://github.com/MadTown86
        """



        self.instructions.config(state='normal')
        self.instructions.insert("1.0", ''.join(textwrap.dedent(message.splitlines())))
        self.instructions.config(state='disabled')
