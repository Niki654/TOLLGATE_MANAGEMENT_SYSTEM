import wx
import pymysql
import wx.grid

# Connect to the database
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="TOLLGATE"
)
cursor = db.cursor()

class TransactionManager(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Transaction Manager", size=(400, 300))
        panel = wx.Panel(self)

        new_transaction_btn = wx.Button(panel, label="New Transaction", pos=(50, 50))
        new_transaction_btn.Bind(wx.EVT_BUTTON, self.on_new_transaction)

        show_failed_btn = wx.Button(panel, label="Show Failed Transactions", pos=(50, 100))
        show_failed_btn.Bind(wx.EVT_BUTTON, self.on_show_failed)

        show_successful_btn = wx.Button(panel, label="Show Successful Transactions", pos=(50, 150))
        show_successful_btn.Bind(wx.EVT_BUTTON, self.on_show_successful)
        
        show_successful_btn = wx.Button(panel, label="Show Transactions", pos=(50, 200))
        show_successful_btn.Bind(wx.EVT_BUTTON, self.on_show_transaction)

    def on_new_transaction(self, event):
        # Create a dialog for entering transaction details
        dialog = wx.Dialog(self, title="New Transaction", size=(350, 450))
        
        # Add controls to the dialog
        tgid_label = wx.StaticText(dialog, label="TGID:")
        tgid_text = wx.TextCtrl(dialog)
        sid_label = wx.StaticText(dialog, label="SID:")
        sid_text = wx.TextCtrl(dialog)
        vid_label = wx.StaticText(dialog, label="VID:")
        vid_text = wx.TextCtrl(dialog)
        cost_label = wx.StaticText(dialog, label="Cost:")
        cost_text = wx.TextCtrl(dialog)
        status_label = wx.StaticText(dialog, label="Status:")
        status_choice = wx.Choice(dialog, choices=["Successful", "Failed"])
        
        # Add a button to submit the transaction
        submit_button = wx.Button(dialog, label="Submit")
        
        # Arrange controls in a vertical box sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tgid_label, 0, wx.ALL, 5)
        sizer.Add(tgid_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(sid_label, 0, wx.ALL, 5)
        sizer.Add(sid_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(vid_label, 0, wx.ALL, 5)
        sizer.Add(vid_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(cost_label, 0, wx.ALL, 5)
        sizer.Add(cost_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(status_label, 0, wx.ALL, 5)
        sizer.Add(status_choice, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(submit_button, 0, wx.ALL | wx.CENTER, 5)
        
        dialog.SetSizer(sizer)
        
        # Define a function to handle the submit button click event
        def on_submit(event):
            tgid = tgid_text.GetValue()
            sid = sid_text.GetValue()
            vid = vid_text.GetValue()
            cost = cost_text.GetValue()
            status = status_choice.GetStringSelection()
            
            # Insert the new transaction into the database
            cursor.execute("INSERT INTO TRANSACTIONS (TGID, SID, VID, COST, STATUS) VALUES (%s, %s, %s, %s, %s)",
                        (tgid, sid, vid, cost, status))
            db.commit()
            dialog.Destroy()
        
        submit_button.Bind(wx.EVT_BUTTON, on_submit)
        
        # Show the dialog
        dialog.ShowModal()
        dialog.Destroy()


    def on_show_failed(self, event):
        # Create a dialog for displaying failed transactions
        dialog = wx.Dialog(self, title="Failed Transactions", size=(600, 400))
        
        # Create a grid for displaying the transactions
        grid = wx.grid.Grid(dialog)
        grid.CreateGrid(0, 5)  # 6 columns for TID, TGID, SID, VID, COST, TIME
        grid.SetColLabelValue(0, "TRANSACTION ID")
        grid.SetColLabelValue(1, "TOLL GATE ID")
        grid.SetColLabelValue(2, "  STAFF ID  ")
        grid.SetColLabelValue(3, "VEHICLE ID")
        grid.SetColLabelValue(4, "  COST  ")
        
        # Fetch and display failed transactions
        cursor.execute("SELECT TID, TGID, SID, VID, COST, TIME FROM TRANSACTIONS WHERE STATUS = 'Failed'")
        transactions = cursor.fetchall()
        for i, transaction in enumerate(transactions):
            grid.AppendRows(1)
            grid.SetCellValue(i, 0, str(transaction[0]))
            grid.SetCellValue(i, 1, str(transaction[1]))
            grid.SetCellValue(i, 2, transaction[2])
            grid.SetCellValue(i, 3, transaction[3])
            grid.SetCellValue(i, 4, str(transaction[4]))
        
        # Auto-size columns
        grid.AutoSizeColumns()
        
        # Arrange the grid in a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        dialog.SetSizer(sizer)
        
        # Show the dialog
        dialog.ShowModal()
        dialog.Destroy()


    def on_show_successful(self, event):
        # Create a dialog for displaying failed transactions
        dialog = wx.Dialog(self, title="Successful Transactions", size=(600, 400))
        
        # Create a grid for displaying the transactions
        grid = wx.grid.Grid(dialog)
        grid.CreateGrid(0, 5)  # 6 columns for TID, TGID, SID, VID, COST, TIME
        grid.SetColLabelValue(0, "TRANSACTUON ID")
        grid.SetColLabelValue(1, "TOLL GATE ID")
        grid.SetColLabelValue(2, "  STAFF ID  ")
        grid.SetColLabelValue(3, "VEHICLE ID")
        grid.SetColLabelValue(4, "  COST  ")
        
        # Fetch and display failed transactions
        cursor.execute("SELECT TID, TGID, SID, VID, COST, TIME FROM TRANSACTIONS WHERE STATUS = 'Successful'")
        transactions = cursor.fetchall()
        
        for i, transaction in enumerate(transactions):
            grid.AppendRows(1)
            grid.SetCellValue(i, 0, str(transaction[0]))
            grid.SetCellValue(i, 1, str(transaction[1]))
            grid.SetCellValue(i, 2, transaction[2])
            grid.SetCellValue(i, 3, transaction[3])
            grid.SetCellValue(i, 4, str(transaction[4]))
        
        # Auto-size columns
        grid.AutoSizeColumns()
        
        # Arrange the grid in a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        dialog.SetSizer(sizer)
        
        # Show the dialog
        dialog.ShowModal()
        dialog.Destroy()
        
    def on_show_transaction(self, event):
        # Create a dialog for displaying failed transactions
        dialog = wx.Dialog(self, title="Transactions", size=(600, 400))
        
        # Create a grid for displaying the transactions
        grid = wx.grid.Grid(dialog)
        grid.CreateGrid(0, 6)  # 6 columns for TID, TGID, SID, VID, COST, TIME
        grid.SetColLabelValue(0, "TRANSACTUON ID")
        grid.SetColLabelValue(1, "TOLL GATE ID")
        grid.SetColLabelValue(2, "  STAFF ID  ")
        grid.SetColLabelValue(3, "VEHICLE ID")
        grid.SetColLabelValue(4, "  COST  ")
        grid.SetColLabelValue(5, "FASTTRACK ID")
        
        # Fetch and display failed transactions
        cursor.execute("SELECT TID, TGID, SID, VID, COST, TIME FROM TRANSACTIONS")
        transactions = cursor.fetchall()
        
        for i, transaction in enumerate(transactions):
            grid.AppendRows(1)
            grid.SetCellValue(i, 0, str(transaction[0]))
            grid.SetCellValue(i, 1, str(transaction[1]))
            grid.SetCellValue(i, 2, transaction[2])
            grid.SetCellValue(i, 3, transaction[3])
            grid.SetCellValue(i, 4, str(transaction[4]))
            cursor.execute("SELECT FTID FROM VEHICLE WHERE VID=%s",(transaction[3],))
            FID =  cursor.fetchone()
            grid.SetCellValue(i, 5, str(FID))
        
        # Auto-size columns
        grid.AutoSizeColumns()
        
        # Arrange the grid in a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 5)
        dialog.SetSizer(sizer)
        
        # Show the dialog
        dialog.ShowModal()
        dialog.Destroy()

# if __name__ == "__main__":
#     app = wx.App()
#     frame = MyFrame()
#     frame.Show()
#     app.MainLoop()
