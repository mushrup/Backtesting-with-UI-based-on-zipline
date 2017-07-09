from appJar import gui
import os
# function called by pressing the buttons
pink = ''
orange = ''
def press(btn):

    if btn=="Cancel":
        app.stop()
    else:
        print("Pink:", app.getEntry('user'), "Orange:", app.getEntry('pass'))
        pink=(app.getEntry('user'))
        orange=(app.getEntry('pass'))
        B=(app.getEntry('begin'))
        E=(app.getEntry('end'))
        print(pink,orange)
        file = open('pink_orange.txt','w')
        file.write(pink+' '+orange)
        file.close()
        os.system('pythonw -m zipline run -f CompareDailyReturnRate.py --start '+B+' --end '+E+' -o apple.txt')

if pink=='':
    app = gui()
    app.addLabel("title", "NAME TWO STOCKS", 0, 0, 4)  # Row 0,Column 0,Span 2
    app.addLabel("user", "STOCK ONE:", 1, 0)              # Row 1,Column 0
    app.addEntry("user", 1, 1)                           # Row 1,Column 1
    app.addLabel("pass", "STOCK TWO:", 2, 0)              # Row 2,Column 0
    app.addEntry("pass", 2, 1)                     # Row 2,Column 1
    app.addLabel("begin", "Begin from(YYYY-M-D):", 3, 0)              # Row 2,Column 0
    app.addEntry("begin", 3, 1)
    app.addLabel("end", "End at(YYYY-M-D):", 4, 0)              # Row 4,Column 0
    app.addEntry("end", 4, 1)
    app.addButtons(["Submit", "Cancel"], press, 5, 0, 2) # Row 5,Column 0,Span 2
    app.setEntryFocus("user")
    app.go()


