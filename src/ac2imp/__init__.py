
import sys, os, time
from traceback import print_exc

import wx
from wx import xrc
import wx.grid as grd

from .import_utils import *
from .accedge import *


class ac2imp(wx.App):
    """
        class ac2imp
        
        Extends wx.App
        
        Provides a data table to preview csv input.
    """


    def __init__(self):
        wx.App.__init__(self,redirect=False)

    def OnInit(self):
        """
           Initializes and shows frame from ac2imp.xrc 
        """
        # load the xml resource
        script_dir = os.path.dirname ( __file__ )
        self.res = xrc.XmlResource ( "%s/ac2imp.xrc" % script_dir )
        # load the frame from the resource        
        self.frame = self.res.LoadFrame ( None, "ID_AC2IMP")
        
        # associate the MenuBar
        self.frame.SetMenuBar (
            self.res.LoadMenuBar("ID_MENUBAR")
        )

        # the grid
        self.grid = xrc.XRCCTRL(self.frame,"ID_GRID")
        self.grid.EnableEditing(True)
        
        # the mappings
        self.mappings = xrc.XRCCTRL(self.frame,"ID_MAPPINGS")

        try:
            try:
              #  try current directory first
              if os.path.isfile ( 'ac2imp_custom.py' ):
                execfile ( 'ac2imp_custom.py', globals())
                for mapping in all_mappings:
                    self.mappings.Append ( mapping, all_mappings[mapping] )
              else:
                raise # try the home directory
            except:
                homepath=os.path.expanduser('~')
                cust_mappings = "%s/ac2imp_custom.py" % homepath
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

        # output formats
        self.exports = xrc.XRCCTRL(self.frame,"ID_EXPORT")
        
        # handle events
        self.Bind ( wx.EVT_MENU, self.OnCloseBtn, id=xrc.XRCID("ID_MENU_CLOSE"))
        self.Bind ( wx.EVT_BUTTON, self.OnCloseBtn, id=xrc.XRCID("ID_BTN_CLOSE"))
        self.Bind ( wx.EVT_MENU, self.OnImport1, id=xrc.XRCID("ID_MENU_IMPORT1"))
#        self.Bind ( wx.EVT_MENU, self.OnImport2, id=xrc.XRCID("ID_MENU_IMPORT2"))
        self.Bind ( wx.EVT_BUTTON, self.OnImport1, id=xrc.XRCID("ID_BTN_IMPORT1"))
#        self.Bind ( wx.EVT_BUTTON, self.OnImport2, id=xrc.XRCID("ID_BTN_IMPORT2"))
        self.Bind ( wx.EVT_MENU, self.OnExport, id=xrc.XRCID("ID_MENU_EXPORT"))
        self.Bind ( wx.EVT_BUTTON, self.OnExport, id=xrc.XRCID("ID_BTN_EXPORT"))
        self.Bind ( wx.EVT_MENU, self.OnExport, id=xrc.XRCID("ID_MENU_EXPORT"))
        self.Bind ( wx.EVT_BUTTON, self.OnExport, id=xrc.XRCID("ID_BTN_EXPORT"))
        self.frame.Bind ( wx.EVT_CLOSE, self.OnClose )
        self.frame.Bind ( wx.EVT_MOVE, self.OnMove )
        self.frame.Bind ( wx.EVT_SIZE, self.OnSize )
        
        
        # app preferences
        self.config = wx.Config ( "ac2imp" )

        x=self.config.ReadInt("screenx",100)
        y=self.config.ReadInt("screeny",100)
        w=self.config.ReadInt("screenw",600)
        h=self.config.ReadInt("screenh",550)

        
        # show the frame        
        self.SetTopWindow(self.frame)
        
        self.frame.SetPosition( (x,y) )
        self.frame.SetSize( (w,h) )
        self.frame.Show()
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
            message="Open Manual comma separated Transaction File",
            wildcard="Transaction (*.txt)|*.txt|All Files (*.*)|*.*",
            style=wx.FD_OPEN|wx.FD_CHANGE_DIR,            
        )
        if dlg.ShowModal() == wx.ID_OK:
            path=dlg.GetPath()
            self._open_file1(path)
        dlg.Destroy()
    
    def _open_file1(self,path):
#        self.grid.CreateGrid(1,1)
#        self.grid.SetTable(self.grid.grid_table)
        """
            Opens a report of bank register file and loads it's contents into the data table.
            
            path: path to the manual accounting file .
        """
        mapping = self.mappings.GetClientData(self.mappings.GetSelection())
        try:
          delimiter=mapping['_params']['delimiter']
        except:
          delimiter=','
        try:
          skip_last=mapping['_params']['skip_last']
        except:
          skip_last=0
        self.grid_table = LoadTransactions(path,delimiter,skip_last)
#        data_format = self.grid_table.data_format
        self.grid.SetTable(self.grid_table)
#        self.data_format=data_format
#       for export file name
        self.opened_path=path

    def OnExport(self,evt):
        if not hasattr(self,'grid_table'):
            wx.MessageDialog(
                self.frame,
                "Use import to load a Transactions file.",
                "No File loaded.",
                wx.OK|wx.ICON_ERROR                
            ).ShowModal()
            return
        
        format = self.exports.GetStringSelection()
        mapping=self.mappings.GetClientData(self.mappings.GetSelection())[format]
        grid=self.grid_table
        data_format=self.grid_table.data_format
        if format == 'AccountEdge' and data_format !="Credit":
            ac2imp_export = accedge.export
        elif format == 'AccountEdge' and data_format =="Credit":
            ac2imp_export = accedge.credit_export
        else:
            raise Exception ( "Unhandled export format: %s" % format )
        path=self.opened_path
        leng=len(path)
        if path.find(".txt",leng-4,leng) != -1: # found .txt
           path_receive = path.replace('.txt','_receive.csv') 
           path_spend = path.replace('.txt','_spend.csv') 
        elif path.find(".csv",leng-4,leng) != -1: # found .csv:
           path_receive = path.replace('.csv','_receive.txt') 
           path_spend = path.replace('.csv','_spend.txt') 
        else:
           path_receive = path + '_receive.txt'
           path_spend = path + '_spend.txt'

        result=ac2imp_export(path_receive,path_spend,mapping,grid)
        if result == 0:
           wx.MessageDialog (
               self.frame,
               "%s file saved at:\n%s" % ( format, path ),
               "Export Complete",
               wx.OK|wx.ICON_INFORMATION
           ).ShowModal()
        elif result == 15:
           wx.MessageDialog (
               self.frame,
               "Account information cannot be empty for Credit ", 
               "No File exported.",
               wx.OK|wx.ICON_INFORMATION
           ).ShowModal()
        elif result == 1:
           wx.MessageDialog (
               self.frame,
               "Something is wrong ", 
               "No File exported.",
               wx.OK|wx.ICON_INFORMATION
           ).ShowModal()


