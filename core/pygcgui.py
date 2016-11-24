# -*- coding: utf-8 -*-
"""
@author: Karl C. Goedel (mail@karl-goedel.de)

This module provides the GUI for pyGC

"""

import wx

class pyGCGuiFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"pyGC - Glass Cutter Control", pos = wx.DefaultPosition, size = wx.Size( 1024,825 ), style = wx.DEFAULT_FRAME_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )		
		
		bSizer2.AddSpacer( ( 220, 0), 1, wx.EXPAND, 5 )
		
		self.connection_label = wx.StaticText( self, wx.ID_ANY, u"Connection:", wx.Point( -1,-1 ), wx.Size( 110,-1 ), 0 )
		self.connection_label.Wrap( 0 )
		bSizer2.Add( self.connection_label, 0, wx.ALL, 10 )
		
		port_comboBoxChoices = [ u"automatic", u"/dev/ttyUSB0", u"/dev/ttyUSB1", u"/dev/ttyUSB2", u"COM1", u"COM2", u"COM3" ]
		self.port_comboBox = wx.ComboBox( self, wx.ID_ANY, u"automatic", wx.DefaultPosition, wx.DefaultSize, port_comboBoxChoices, 0 )
		bSizer2.Add( self.port_comboBox, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5 )
		
		self.connect_button = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.Size( 110,35 ), 0 )
		bSizer2.Add( self.connect_button, 0, wx.ALL, 5 )
		
		self.disconnect_button = wx.Button( self, wx.ID_ANY, u"Disconnect", wx.DefaultPosition, wx.Size( 110,35 ), 0 )
		bSizer2.Add( self.disconnect_button, 0, wx.ALL, 5 )
		
		self.connection_staticText = wx.StaticText( self, wx.ID_ANY, u"disconnected", wx.Point( -1,-1 ), wx.Size( 120,-1 ), 0 )
		self.connection_staticText.Wrap( 0 )
		bSizer2.Add( self.connection_staticText, 0, wx.ALL, 10 )		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel1 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
				
		bSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
				
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"X", wx.DefaultPosition, wx.Size( 40,50 ), 0 )
		self.m_staticText19.Wrap( 0 )
		self.m_staticText19.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_staticText19, 0, wx.ALL, 11 )
		
		self.xread_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_READONLY|wx.TE_RIGHT )
		self.xread_textCtrl.SetMaxLength( 0 ) 
		self.xread_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		self.xread_textCtrl.SetForegroundColour( wx.Colour( 240, 119, 70 ) )
		self.xread_textCtrl.SetBackgroundColour( wx.Colour( 249, 249, 248 ) )
		
		bSizer6.Add( self.xread_textCtrl, 0, wx.ALL, 5 )
		
		self.xset_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		self.xset_textCtrl.SetMaxLength( 0 ) 
		self.xset_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.xset_textCtrl, 0, wx.ALL, 5 )
		
		self.xgo_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.Size( 55,50 ), 0 )
		bSizer6.Add( self.xgo_button, 0, wx.ALL, 5 )
		
		self.xhome_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Home", wx.DefaultPosition, wx.Size( 75,50 ), 0 )
		bSizer6.Add( self.xhome_button, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Units: mm", wx.Point( -1,-1 ), wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_staticText21.Wrap( 0 )
		self.m_staticText21.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_staticText21, 0, wx.ALL, 18 )
		
		
		bSizer4.Add( bSizer6, 4, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText191 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.Size( 40,50 ), 0 )
		self.m_staticText191.Wrap( 0 )
		self.m_staticText191.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_staticText191, 0, wx.ALL, 11 )
		
		self.yread_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_READONLY|wx.TE_RIGHT )
		self.yread_textCtrl.SetMaxLength( 0 ) 
		self.yread_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		self.yread_textCtrl.SetForegroundColour( wx.Colour( 240, 119, 70 ) )
		self.yread_textCtrl.SetBackgroundColour( wx.Colour( 249, 249, 248 ) )
		
		bSizer7.Add( self.yread_textCtrl, 0, wx.ALL, 5 )
		
		self.yset_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		self.yset_textCtrl.SetMaxLength( 0 ) 
		self.yset_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.yset_textCtrl, 0, wx.ALL, 5 )
		
		self.ygo_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.Size( 55,50 ), 0 )
		bSizer7.Add( self.ygo_button, 0, wx.ALL, 5 )
		
		self.yhome_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Home", wx.DefaultPosition, wx.Size( 75,50 ), 0 )
		bSizer7.Add( self.yhome_button, 0, wx.ALL, 5 )
		
		self.m_staticText211 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Units: mm", wx.Point( -1,-1 ), wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_staticText211.Wrap( 0 )
		self.m_staticText211.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_staticText211, 0, wx.ALL, 18 )
		
		bSizer4.Add( bSizer7, 4, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText192 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Z", wx.DefaultPosition, wx.Size( 40,50 ), 0 )
		self.m_staticText192.Wrap( 0 )
		self.m_staticText192.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer8.Add( self.m_staticText192, 0, wx.ALL, 11 )
		
		self.zread_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_READONLY|wx.TE_RIGHT )
		self.zread_textCtrl.SetMaxLength( 0 ) 
		self.zread_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		self.zread_textCtrl.SetForegroundColour( wx.Colour( 240, 119, 70 ) )
		self.zread_textCtrl.SetBackgroundColour( wx.Colour( 249, 249, 248 ) )
		
		bSizer8.Add( self.zread_textCtrl, 0, wx.ALL, 5 )
		
		self.zset_textCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"0.000", wx.DefaultPosition, wx.Size( 150,50 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		self.zset_textCtrl.SetMaxLength( 0 ) 
		self.zset_textCtrl.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer8.Add( self.zset_textCtrl, 0, wx.ALL, 5 )
		
		self.zgo_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.Size( 55,50 ), 0 )
		bSizer8.Add( self.zgo_button, 0, wx.ALL, 5 )
		
		self.zhome_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Home", wx.DefaultPosition, wx.Size( 75,50 ), 0 )
		bSizer8.Add( self.zhome_button, 0, wx.ALL, 5 )
		
		self.m_staticText212 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Units: mm", wx.Point( -1,-1 ), wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_staticText212.Wrap( 0 )
		self.m_staticText212.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer8.Add( self.m_staticText212, 0, wx.ALL, 18 )
		
		bSizer4.Add( bSizer8, 4, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText29 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"All:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( 0 )
		self.m_staticText29.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer9.Add( self.m_staticText29, 0, wx.ALL, 16 )
		
		self.stop_button = wx.Button( self.m_panel1, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.Size( 120,100 ), 0 )
		self.stop_button.SetFont( wx.Font( 16, 70, 90, 90, False, wx.EmptyString ) )
		self.stop_button.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		bSizer9.Add( self.stop_button, 0, wx.ALL, 5 )
		
		self.allhome_button = wx.Button( self.m_panel1, wx.ID_ANY, u"Home", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizer9.Add( self.allhome_button, 0, wx.ALL, 5 )
				
		bSizer4.Add( bSizer9, 4, wx.EXPAND, 5 )
				
		self.m_panel1.SetSizer( bSizer4 )
		self.m_panel1.Layout()
		bSizer4.Fit( self.m_panel1 )
		self.m_notebook.AddPage( self.m_panel1, u"Control", True )
		self.m_panel2 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 25 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText17 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"GCode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( 0 )
		fgSizer1.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.preview_staticText = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Preview:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.preview_staticText.Wrap( 0 )
		fgSizer1.Add( self.preview_staticText, 0, wx.ALL, 5 )
		
		self.gcode_textCtrl = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.TE_LEFT|wx.TE_MULTILINE|wx.HSCROLL|wx.VSCROLL )
		self.gcode_textCtrl.SetMaxLength( 0 ) 
		self.gcode_textCtrl.SetMinSize( wx.Size( 350,500 ) )
		
		fgSizer1.Add( self.gcode_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.gcode_bitmap = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.Point( 10,10 ), wx.Size( 2*285+10,2*285+10 ), 0 )
		fgSizer1.Add( self.gcode_bitmap, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.gcode_open_filePicker = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, u",90,90,-1,70,0", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN )
		bSizer10.Add( self.gcode_open_filePicker, 0, wx.ALL, 5 )
		
		self.gcode_save_button = wx.Button( self.m_panel2, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.gcode_save_button, 0, wx.ALL, 5 )
		
		self.gcode_run_button = wx.Button( self.m_panel2, wx.ID_ANY, u"Run code", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.gcode_run_button, 0, wx.ALL, 5 )
		
		self.gcode_pause_button = wx.Button( self.m_panel2, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.gcode_pause_button, 0, wx.ALL, 5 )
			
		fgSizer1.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer10a = wx.BoxSizer( wx.VERTICAL )
		
		self.tool_cb = wx.CheckBox(self.m_panel2, -1, 'Automatic tool selection when loading file', (50, 255))
		self.tool_cb.SetValue(True)
		bSizer10a.Add( self.tool_cb, 0, wx.ALL, 5 )
		
		self.offset_cb = wx.CheckBox(self.m_panel2, -1, 'Set xy offset to stop bars', (50, 255))
		self.offset_cb.SetValue(True)		
		bSizer10a.Add( self.offset_cb, 0, wx.ALL, 5 )		
		
		fgSizer1.Add( bSizer10a, 0, wx.ALL, 5 )
		
		self.m_panel2.SetSizer( fgSizer1 )
		self.m_panel2.Layout()
		fgSizer1.Fit( self.m_panel2 )
		self.m_notebook.AddPage( self.m_panel2, u"GCode", False )
		self.m_panel3 = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.console_output_textCtrl = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 970,420 ), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL )
		self.console_output_textCtrl.SetMaxLength( 0 ) 
		self.console_output_textCtrl.SetBackgroundColour( wx.Colour( 249, 249, 248 ) )
		
		bSizer12.Add( self.console_output_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText30 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"TinyG-code:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( 0 )
		bSizer12.Add( self.m_staticText30, 0, wx.ALL, 5 )		
		
		bSizer11.Add( bSizer12, 7, wx.EXPAND, 5 )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.console_textCtrl = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 820,120 ), wx.TE_LEFT|wx.TE_MULTILINE|wx.HSCROLL )
		self.console_textCtrl.SetMaxLength( 0 ) 
		bSizer13.Add( self.console_textCtrl, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.open_consolecode_filePicker = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 140,-1 ), wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN )
		bSizer14.Add( self.open_consolecode_filePicker, 0, wx.ALL, 5 )
		
		self.save_consolecode_button = wx.Button( self.m_panel3, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		bSizer14.Add( self.save_consolecode_button, 0, wx.ALL, 5 )
		
		self.console_button = wx.Button( self.m_panel3, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		bSizer14.Add( self.console_button, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
				
		bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )		
		
		bSizer11.Add( bSizer13, 2, wx.EXPAND, 5 )	
		
		self.m_panel3.SetSizer( bSizer11 )
		self.m_panel3.Layout()
		bSizer11.Fit( self.m_panel3 )
		self.m_notebook.AddPage( self.m_panel3, u"TinyG Console", False )
		
		bSizer3.Add( self.m_notebook, 1, wx.EXPAND|wx.ALL, 5 )
				
		bSizer1.Add( bSizer3, 15, wx.EXPAND|wx.LEFT, 5 )
				
		self.SetSizer( bSizer1 )
		self.Layout()
		
		
	def __del__( self ):
		pass


class ThicknessDialog(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title="Change Sample Thickness")
		self.thicknesslabel = wx.StaticText( self, wx.ID_ANY, u"Please select the thickness of the substrate:")
		self.comboBox1 = wx.ComboBox(self, 
                                     choices=[ u"0.5 mm", u"1.0 mm", u"2.2 mm (default)", u"3.0 mm"],
                                     value=u"2.2 mm (default)")
		okBtn = wx.Button(self, wx.ID_OK)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.thicknesslabel, 0, wx.ALL|wx.CENTER, 5)
		sizer.Add(self.comboBox1, 0, wx.ALL|wx.CENTER, 5)
		sizer.Add(okBtn, 0, wx.ALL|wx.CENTER, 5)
		self.SetSizer(sizer)
