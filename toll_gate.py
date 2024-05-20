import wx
from STAFF.TRANSACTIONS import TransactionManager
import pymysql

# Connect to the database
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="TOLLGATE"
)
cursor = db.cursor()

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Login', size=(370, 230))
        panel = wx.Panel(self)
        
        self.sid_label = wx.StaticText(panel, label='SID:', pos=(50, 30))
        self.sid_text = wx.TextCtrl(panel, pos=(120, 30), size=(150, -1))
        
        self.pssword_label = wx.StaticText(panel, label='Password:', pos=(50, 70))
        self.pssword_text = wx.TextCtrl(panel, pos=(120, 70), size=(150, -1), style=wx.TE_PASSWORD)
        
        login_button = wx.Button(panel, label='Login', pos=(120, 110))
        login_button.Bind(wx.EVT_BUTTON, self.on_login)
        
        self.result_label = wx.StaticText(panel, label='', pos=(120, 150))

    def on_login(self, event):
        sid = self.sid_text.GetValue()
        password = self.pssword_text.GetValue()
        
        query = "SELECT PSSWORD FROM STAFF WHERE SID = %s"
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        
        if result is None:
            self.result_label.SetLabel('SID not found')
        elif result[0] != password:
            self.result_label.SetLabel('Incorrect password')
        else:
            self.result_label.SetLabel('Login successful')
            app = wx.App()
            frame = TransactionManager(None)
            frame.Show()
            app.MainLoop()

app = wx.App()
frame = LoginFrame()
frame.Show()
app.MainLoop()
