#!/usr/bin/python2.7
from AppKit import NSBundle
import base64
import re
import subprocess
import sys
import syslog
import tkFont
import Tkinter
import urllib2
import xml.etree.cElementTree as etree

# This script logs actions to both STDOUT and system.log
# You can set your own 'tag' for the log entries here
syslog.openlog("jamfsw-it-logs")


def log(msg):
    """Logging function to write to system.log and STDOUT"""
    print(msg)
    syslog.syslog(syslog.LOG_ALERT, "AssetTag: " + str(msg))

log("Starting Submit Mac Asset Tag")

# Prevent the Python app icon from appearing in the Dock
info = NSBundle.mainBundle().infoDictionary()
info['LSUIElement'] = True


def get_uuid():
    """This will obtain the UUID of the current Mac using system_profiler"""
    mac_uuid = subprocess.check_output(["/usr/sbin/system_profiler", "SPHardwareDataType"])
    return mac_uuid[mac_uuid.find("Hardware UUID:"):].split()[-1]

# The UUID is used for API calls to the JSS
macUUID = get_uuid()
log("Mac UUID: {0}".format(macUUID))

# The JSS URL and API credentials are assigned here (credentials passed as parameters)
jssURL = "https://yourjss.jamfcloud.com/JSSResource/computers/udid/{}".format(macUUID)
jssAuth = base64.b64encode(sys.argv[4] + ':' + sys.argv[5])

# This is a base64 encoded GIF that will be displayed in the GUI
gifBase = """
R0lGODlhgACAAPcAAO3t7SMfICklJiwoKSsnKDMvMDQwMTczND87PEM/QDg1NkE+P2BdXm1qa2hlZn16e01LTEtJSmVjZIB+f3l3eJ2bnIyKi4mHiIiGhyUk
JVRTVFxbXL69vra1tqCfoJ6dnpeWlwEBAzw8PRUbMQoRJyM3exs5gho1ewYLGCVBhSM8fiU/gSZFigEDBx1CiihHhm5vcSRKkRctUylNjBtHkSJPmCdUnSla
oi5bnigqLS1gpzJmqjFioyxVjylOfjdmoztsqzI1OTU4PDc6Pjs+QjNrrjlrpkFFSjhxsTBglzVooz9xqihFZlaOylmRzTx2swMGCUJ7tUd+tkR3q0t9r2id
0SwvMjAzNiMlJxYXGDU3ORscHWttb0iEukqCt0yFuVCIvFCHuVCEtFWLvViPwVWJuGCazl2TxFiMujxdfDVSbmOVxGeZx0yJvFOLvFWNvlqSwl+YylWJtV2V
w1uQvl+XxV2TwVqNuGOayGWdyl6Ru2KVv2aZw0ZphmqdyG2fy3iv3nWq13Gkzlx+mk9rg2GCnlGOvVWSv1iVwl2YxGuo2GegzEVfc1+cxSUoKiotLy4xM2Kg
yGqmzW1wcAgJCCcoJwYGBQ0NDAMCAAQDAQUEAhgXFQ0KBwsHBBQRDzEuLjw6OiMiIkpISFlXV399fW9tbWpoaHp5eXd2dnNycnFwcG1sbGJhYeDf39TT08jH
x8TDw7q5ubSzs66tra2srKqpqainp6KhoZybm5qZmZWUlJKRkZCPj4aFhYWEhPX19fDw8Ozs7Ovr6+np6efn5+Xl5eLi4t7e3t3d3dvb29ra2tfX19DQ0M3N
zcrKysXFxcLCwsDAwL6+vry8vLu7u7e3t7KysrCwsK6urqurq6WlpaOjo46OjoyMjIqKioODg4KCgoCAgH5+fnx8fHt7e29vb2tra2lpaV9fX1paWlZWVlFR
UU9PT0NDQz8/Pzk5OTY2NjIyMi8vLywsLCoqKiAgIBgYGBUVFRISEhAQEAoKCgQEBAICAgEBAQAAAP///yH5BAEAAP8ALAAAAACAAIAAAAj/AAEIHEiwoMGD
CBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTEYVRK6UuncuXMGPKnEmzpstRDiZx2cmzp7lz3pihpAgNHiVK+pIqXcq0qdOkSJ82pZQvCJEh
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
fnvuu/f+e/DDF5/cgAAAOw==
"""


class App:
    # This class will generate the GUI and all of its elements
    # It also contains all of the functions used when one of the buttons are clicked

    # Regular expression to match asset tag pattern
    # This regex will match inputs to "JSXXXXXX" where 'X' is a number
    assetTag = re.compile('^JS[0-9]{6}$')

    def __init__(self):
        # The first lines create the GUI object and set it to stay on top of all other windows
        self.root = Tkinter.Tk()
        self.root.withdraw()
        self.root.protocol('WM_DELETE_WINDOW', self.clicked_exit)
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.title("Submit Your Asset Tag")

        # Set the default background colors for the window elements
        bgcolor = "#EDEDED"
        self.root.tk_setPalette(highlightbackground=bgcolor, background=bgcolor)

        # Setup the default font for widgets
        font = tkFont.nametofont('TkDefaultFont')
        font.config(family='Helvetica Neue', size=14)
        self.root.option_add("*Font", font)

        # This will prevent menu bar options from appearing when the window is selected
        menubar = Tkinter.Menu(self.root)
        self.root.config(bg=bgcolor, menu=menubar)
        
        # Here we load the data of our GIF image above and place it in the window
        # The '.grid()' method allows you to place elements in the window according to XY coordinates
        gif = Tkinter.PhotoImage(data=gifBase)
        Tkinter.Label(self.root, image=gif, borderwidth=10).grid(row=0, rowspan=5)
        
        # Tkinter labels display text or images within a window and can have unique styles for each
        Tkinter.Label(self.root, text="Enter the asset tag number for your Mac:").grid(padx=15, row=0, column =1)
        Tkinter.Label(self.root, text="(Your asset tag is located beneath your MacBook)",
                      font=("Helvetica Neue", 10)).grid(row=1, column =1)
        
        # Here is another Tkinter variable that will store the value of what is in our entry box
        self.input_variable = Tkinter.StringVar()
        self.input_variable.set("JSxxxxxx")
        # The entry box is a field where a user can type in
        Tkinter.Entry(self.root, width=8, bg='white', textvariable=self.input_variable).grid(row=2, column=1)
        
        # These variables are for the message line in our GUI that changes both text
        # and color based upon success or error messages
        self.messageColor = Tkinter.StringVar()
        self.messageColor.set("red")
        
        self.messageVar = Tkinter.StringVar()
        self.messageVar.set("")
        
        self.messageLabel = Tkinter.Label(self.root, textvariable=self.messageVar,
                                          font=("Helvetica Neue", 10, "italic"), fg=self.messageColor.get())
        self.messageLabel.grid(row=3, column=1)
        
        # To have the 'Exit' and 'Submit' buttons display nicely in the lower-right corner I am
        # 'packing' them inside of a widget called a frame that is place into the grid
        button_frame = Tkinter.Frame(self.root)
        Tkinter.Button(button_frame, text="Exit", command=self.clicked_exit, height=1).pack(side=Tkinter.RIGHT)
        self.submitButton = Tkinter.Button(button_frame, text="Submit", command=self.clicked_submit, height=1)
        self.submitButton.pack(side=Tkinter.RIGHT)
        button_frame.grid(row=4, column=1, padx=10, pady=(0, 5), sticky='e')
        
        # These last lines will position the GUI slightly above the center of the screen
        # when it is finally drawn on the 'self.root.mainloop()' line
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 3
        self.root.geometry("+{0}+{1}".format(x, y))
        self.root.resizable(False,False)
        self.root.deiconify()
        self.root.mainloop()
        
    def display_error(self, msg):
        # This error function writes a log entry and also displays the same text on the
        # message line in the GUI
        log("Message displayed to user: " + str(msg))
        self.messageVar.set(str(msg))
        
    def clicked_exit(self):
        # This will close the window and exit the script
        log("Exit button has been clicked")
        self.root.destroy()
        
    def clicked_submit(self):
        # This function will validate the entered asset tag by the user and also verify
        # that there is not already an asset tag in the inventory record (that issue can
        # also be addressed via smart computer group scoping)
        input_value = self.input_variable.get().upper()
        if not self.assetTag.match(input_value):
            self.display_error("An invalid asset tag was entered")
            return
        
        # XML string for the PUT to the JSS
        xml = '<?xml version="1.0" encoding="UTF-8"?>' \
              '<computer><general><asset_tag>{}</asset_tag></general></computer>'.format(input_value)
        
        # If 'self.checkForExistingTag()' returns 'True' then the API update is performed
        if self.check_for_existing_asset_tag():
            self.update_asset_tag(xml)
        
    def check_for_existing_asset_tag(self):
        # This function checks the JSS for an existing asset tag in the inventory record
        log("Checking the JSS for an existing asset tag in the record")        
        request = urllib2.Request(jssURL + '/subset/general')
        request.add_header('Authorization', 'Basic ' + jssAuth)
        
        # If the API call is successful it will check for an asset tag and return 'True' if
        # there is none or 'False' if a value is present ('False' will prevent the follow-
        # -up API update from occurring)
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            # If an error is encountered it is logged and a message is displayed to the user
            log("There was an error with the API call:")
            log("API error: {0}".format(e))
            self.messageVar.set("There was a problem communicating with the JSS.")
        else:
            existing_tag = etree.fromstring(response.read()).find('general/asset_tag').text
            if existing_tag:
                self.display_error("There is an existing asset tag for this Mac: {}".format(existing_tag))
                self.submitButton['state'] = 'disabled'
                return False
            else:
                return True

    def update_asset_tag(self, xml):
        # This function will update the inventory record in the JSS with the new asset tag
        log("Updating the asset tag in the JSS")
        request = urllib2.Request(jssURL)
        request.add_header('Authorization', 'Basic ' + jssAuth)
        request.add_header('Content-Type', 'text/xml')
        request.get_method = lambda: 'PUT'
        
        # The below is very similar to the 'checkForExistingTag()' function above
        # If the API call is successful the message color is set to blue with a success
        # message displayed to the user and the 'Submit' button is disabled to they
        # cannot perform the action again
        try:            
            urllib2.urlopen(request, xml)
        except Exception as e:
            log("There was an error with the API call:")
            log("API error: {}".format(e))
            log("API error: {}".format(e.read()))
            self.messageVar.set("There was a problem submitting the asset tag to the JSS.")
        else:
            log("Message displayed to user: The asset tag has been submitted to the JSS.")
            self.messageColor.set("blue")
            self.messageLabel.configure(fg=self.messageColor.get())
            self.messageVar.set("Success! The asset tag has been submitted to the JSS.")
            self.submitButton['state'] = 'disabled'


# Execute the GUI by calling the class
if __name__ == '__main__':
    App()
