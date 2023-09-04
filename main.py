# This is a Python script to extract the useful information form the pwrterm report.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import re

def fileProcessor(filePath):
    # open pwrterm and process it
    with open(filePath, "r") as pwrterm:
        adminBannerDeletes = []
        adminBannerDeletes.append("Admin Banner Deletes\n")
        myBannerDeletes = []
        myBannerDeletes.append("\nmyBanner Deletes\n")
        workflowDeletes = []
        workflowDeletes.append("\nWorkflow Deletes\n")

        adminBannerRegex = re.compile("^.{16}\w{2,3}\d{1,4}")
        myBannerRegex = re.compile("^\*")
        workflowRegex = re.compile("^.{12}#")

        # run the regexs on each line and save them in their respective lists
        for line in pwrterm:
            # remove whitespace from end of line
            line = line.rstrip() + '\n'

            if adminBannerRegex.match(line):
                adminBannerDeletes.append(line)
            if myBannerRegex.match(line) and line not in adminBannerDeletes:
                myBannerDeletes.append(line)
            if workflowRegex.match(line):
                workflowDeletes.append(line)

    return adminBannerDeletes + myBannerDeletes + workflowDeletes


def driver():
    # creating main window object
    root = Tk()

    # setting the window properties
    root.title("pwrterm reducer")
    root.resizable(True,True)

    frame = ttk.Frame(root, padding=10)

    # create scroll bars
    horizontalScrollbar = Scrollbar(root, orient='horizontal')
    horizontalScrollbar.pack(side=BOTTOM, fill=X)
    verticalScrollbar = Scrollbar(root, orient='vertical')
    verticalScrollbar.pack(side=RIGHT, fill=Y)

    # create file selector
    filePath = filedialog.askopenfilename(
        title='Select pwrterm',
        initialdir=os.path.join(os.path.expanduser('~'),"Downloads"),
        filetypes=(('text files', '*.txt'),('All files', '*.*'))
    )

    # process the pwrterm file and return the usefull lines in order
    lines = fileProcessor(filePath)

    # create the text widget for displaying the info
    textWidget = Text(root, wrap=NONE, xscrollcommand=horizontalScrollbar.set, yscrollcommand=verticalScrollbar.set)

    # insert the usefull lines into the text widget for display
    for line in lines:
        textWidget.insert(END, line)

    # packing the text widget to get it to display
    textWidget.pack(side=TOP, expand=True, fill=BOTH)

    # assigning scrollbars
    horizontalScrollbar.config(command=textWidget.xview)
    verticalScrollbar.config(command=textWidget.yview)

    #print("Admin Deletes: " + str(len(adminBannerDeletes)) + "\nmyBanner Deletes: " + str(len(myBannerDeletes)) + "\nWorkflow Deletes: " + str(len(workflowDeletes)))

    # loop the main panel, i.e. keep the window working
    root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver()
