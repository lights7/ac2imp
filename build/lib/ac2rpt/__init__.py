
import sys, os, time
from traceback import print_exc

import wx
from wx import xrc
import wx.grid as grd

from .report_utils import *
#import report_utils
from .receipt import *


class ac2rpt(wx.App):
    """
        class ac2rpt
        
        Extends wx.App
        
        Provides a data table to preview csv input.
    """


    def __init__(self):
        wx.App.__init__(self,redirect=False)

    payment_method = {}
    check_number = {}
    
    def OnInit(self):
        """
           Initializes and shows frame from ac2rpt.xrc 
        """
        # load the xml resource
        script_dir = os.path.dirname ( __file__ )
        self.res = xrc.XmlResource ( "%s/ac2rpt.xrc" % script_dir )
        print("inita")
        # load the frame from the resource        
        self.frame = self.res.LoadFrame ( None, "ID_AC2RPT")
        
        print("initb")
        # associate the MenuBar
        self.frame.SetMenuBar (
            self.res.LoadMenuBar("ID_MENUBAR")
        )

        print("initc")
        # the grid
        self.grid = xrc.XRCCTRL(self.frame,"ID_GRID")
        self.grid.EnableEditing(True)
        
        print("initd")
        # the mappings
        self.mappings = xrc.XRCCTRL(self.frame,"ID_MAPPINGS")

        print("inite")
        try:
            try:
              #  try current directory first
              if os.path.isfile ( 'ac2rpt_custom.py' ):
                execfile ( 'ac2rpt_custom.py', globals())
                for mapping in all_mappings:
                    self.mappings.Append ( mapping, all_mappings[mapping] )
              else:
                raise # try the home directory
            except:
                homepath=os.path.expanduser('~')
                cust_mappings = "%s/ac2rpt_custom.py" % homepath
                if os.path.isfile( cust_mappings ):
                    execfile ( cust_mappings, globals() )
                    for mapping in all_mappings:
                        self.mappings.Append ( mapping, all_mappings[mapping] )
        except: 
            print_exc()
            # Use built in mappings as default/backup
        if self.mappings.IsEmpty():
            print("Using Default Mappings")
            from .mappings import all_mappings
            for mapping in mappings.all_mappings:
                self.mappings.Append ( mapping, mappings.all_mappings[mapping] )
        self.mappings.SetSelection(0)

        print("initg")
        # output formats
        self.exports = xrc.XRCCTRL(self.frame,"ID_EXPORT")
        
        print("inith")
        # handle events
        self.Bind ( wx.EVT_MENU, self.OnCloseBtn, id=xrc.XRCID("ID_MENU_CLOSE"))
        self.Bind ( wx.EVT_BUTTON, self.OnCloseBtn, id=xrc.XRCID("ID_BTN_CLOSE"))
        self.Bind ( wx.EVT_MENU, self.OnImport1, id=xrc.XRCID("ID_MENU_IMPORT1"))
        self.Bind ( wx.EVT_MENU, self.OnImport2, id=xrc.XRCID("ID_MENU_IMPORT2"))
        self.Bind ( wx.EVT_BUTTON, self.OnImport1, id=xrc.XRCID("ID_BTN_IMPORT1"))
        self.Bind ( wx.EVT_BUTTON, self.OnImport2, id=xrc.XRCID("ID_BTN_IMPORT2"))
        print("initI")
        self.Bind ( wx.EVT_MENU, self.OnExport, id=xrc.XRCID("ID_MENU_EXPORT"))
        print("initj")
        self.Bind ( wx.EVT_BUTTON, self.OnExport, id=xrc.XRCID("ID_BTN_EXPORT"))
        print("initk")
        self.Bind ( wx.EVT_MENU, self.OnExport, id=xrc.XRCID("ID_MENU_EXPORT"))
        print("initl")
        self.Bind ( wx.EVT_BUTTON, self.OnExport, id=xrc.XRCID("ID_BTN_EXPORT"))
        print("initm")
        self.frame.Bind ( wx.EVT_CLOSE, self.OnClose )
        print("initn")
        self.frame.Bind ( wx.EVT_MOVE, self.OnMove )
        print("initr")
        self.frame.Bind ( wx.EVT_SIZE, self.OnSize )
        print("inits")
        
        
        # app preferences
        self.config = wx.Config ( "ac2rpt" )

        print("initt")
        x=self.config.ReadInt("screenx",100)
        y=self.config.ReadInt("screeny",100)
        w=self.config.ReadInt("screenw",600)
        h=self.config.ReadInt("screenh",550)

        print("initu")
        
        # show the frame        
        self.SetTopWindow(self.frame)
        
        print("initv")
        self.frame.SetPosition( (x,y) )
        self.frame.SetSize( (w,h) )
        self.frame.Show()
        print("initw")
        return True
        
    def OnCloseBtn(self,evt):
        """
            Close the application.
        """
        self.frame.Close()
        
    def OnClose(self,evt):
        """
            Appliction Closing
        """
        print("GoodBye")
        self.config.Flush()
        evt.Skip()
        
    def OnMove(self,evt):
        """
            Application Screen Position Changed
        """
        x,y = evt.GetPosition()
        self.config.WriteInt("screenx",x)
        self.config.WriteInt("screeny",y)
        evt.Skip()
        
    def OnSize(self,evt):
        """
            Application Size Changed
        """
        w,h = evt.GetSize()
        self.config.WriteInt("screenw",w)
        self.config.WriteInt("screenh",h)
        evt.Skip()
        
    def OnImport1(self,evt):
        """
            Import a report file of bank register.
        """
        
        # create an open file dialog
        dlg = wx.FileDialog (
            self.frame,
            message="Open Report of Bank Register File",
            wildcard="Bank Register File (*.txt)|*.txt|All Files (*.*)|*.*",
            style=wx.FD_OPEN|wx.FD_CHANGE_DIR,            
        )
        if dlg.ShowModal() == wx.ID_OK:
            path=dlg.GetPath()
            self._open_file1(path)
#        wx.CallLater(100,dlg.Destroy(),1)
        dlg.Destroy()
    

    def OnImport2(self,evt):
        """
            Import a report file of bank register.
        """
        
        # create an open file dialog
        dlg = wx.FileDialog (
            self.frame,
            message="Open Report of Card Transaction File",
            wildcard="Card Transaction File (*.txt)|*.txt|All Files (*.*)|*.*",
            style=wx.FD_OPEN|wx.FD_CHANGE_DIR,            
        )
        if dlg.ShowModal() == wx.ID_OK:
            path=dlg.GetPath()
            self._open_file2(path)
            print("init-1")
#        wx.CallLater(100,dlg.Destroy(),1)
        dlg.Destroy()
        print("init0")
        print("init01")
        print("init02")
        print("init03")

    def _open_file1(self,path):

        """
            Opens a report of bank register file and loads it's contents into the data table.
            
            path: path to the report file of bank register.
        """
        global payment_method, check_number, period
        print("Open File %s" % path)
                      
        mapping = self.mappings.GetClientData(self.mappings.GetSelection())
        try:
          delimiter=mapping['_params']['delimiter']
        except:
          delimiter=','
        try:
          skip_last=mapping['_params']['skip_last']
        except:
          skip_last=0
        self.grid_table = Bank_Register_Grid(path,delimiter,skip_last)
        period = self.grid_table.report_period
        if self.grid_table.report_name != 'Bank Register':
            wx.MessageDialog(
                self.frame,
                "This is not a Bank Register report, please import a Bank Register report file",
                "No File loaded.",
                wx.OK|wx.ICON_ERROR
            ).ShowModal()
            return

        self.grid.SetTable(self.grid_table)
        payment_method = self.grid_table.payment_method
        check_number = self.grid_table.check_number
        self.opened_path = path
        
    def _open_file2(self,path):
        """
            Opens a report of card transaction file and loads it's contents into the data table.
            
            path: path to the report file of card transaction
        """
        global payment_method,check_number,period
        print("Open File %s" % path)
                      
        mapping = self.mappings.GetClientData(self.mappings.GetSelection())
        try:
          delimiter=mapping['_params']['delimiter']
        except:
          delimiter=','
        try:
          skip_last=mapping['_params']['skip_last']
        except:
          skip_last=0
          print("init1")
#        self.grid_table = Card_Transaction_Grid(path,delimiter,skip_last)
        self.card_table=Card_Transaction_Grid(path,delimiter,skip_last)
        print("init2")
        print(self.card_table.report_period)
        if self.card_table.report_period != period:
           wx.MessageDialog(
                self.frame,
                "The period in the Bank Register and Card Transactions are not",
                "the same, make sure they #have the same period.",
                "No File loaded.",
                wx.OK|wx.ICON_ERROR
           ).ShowModal()
           return

        if self.card_table.report_name != 'Card Transactions':
            wx.MessageDialog(
                self.frame,
                "This is not a Card Transaction report, please import a Card Transaction report file",
                "No File loaded.",
                wx.OK|wx.ICON_ERROR
            ).ShowModal()
            return

        print("init3")
        self.grid.SetTable(self.card_table)
        print("init4")
        self.opened_path = path
        print("init5")

    def OnExport(self,evt):
        if not hasattr(self,'grid_table'):
            wx.MessageDialog(
                self.frame,
                "Use import to load a Bank Register report and a Card Transaction Report files.",
                "No File loaded.",
                wx.OK|wx.ICON_ERROR                
            ).ShowModal()
            return
        
        print("init6")
        format = self.exports.GetStringSelection()
        dlg = wx.DirDialog(
            self.frame,
            message='Export Files',
#            wildcard="Excel XLSX Files (*.xlsx)", 
            style=wx.FD_SAVE|wx.FD_CHANGE_DIR,
#	    defaultDir=os.path.dirname(self.opened_path),
#            defaultFile=os.path.basename(self.opened_path).replace('txt',format.lower()) 
        )
#	dlg.SetFilterIndex( format=="xlsx" and 1 or 0 )
        path=None
        path=dlg.GetPath()
        try:
            if dlg.ShowModal() == wx.ID_OK:
                path=dlg.GetPath()
            else:
                return
        finally:
            dlg.Destroy();
        
        print("init7")
        mapping=self.mappings.GetClientData(self.mappings.GetSelection())[format]
        grid=self.card_table
        
        if format == 'Receipt':
            ac2rpt_export = receipt.export
        else:
            raise Exception ( "Unhandled export format: %s" % format )
        print("init8")
        result=ac2rpt_export(path,mapping,grid,payment_method,check_number)
        print("result=%d",result)
        print("init9")
        if result == 0:
           wx.MessageDialog (
               self.frame,
               "%s file saved at:\n%s" % ( format, path ),
               "Export Complete",
               wx.OK|wx.ICON_INFORMATION
           ).ShowModal()
        elif result == 1:
           wx.MessageDialog (
               self.frame,
               "Make sure the periods are the same between Bank Register file and Card Transactions file. Transactions are not the same in these two files.", 
               "No File exported.",
               wx.OK|wx.ICON_INFORMATION
           ).ShowModal()
