# -*- coding: utf-8 -*-
"""
@author: Karl C. Goedel (mail@karl-goedel.de)

This is the main program to control an automated CNC glass cutter.
The communication is done via a TinyG board.
More info:

"""

# wx provides the GUI framework
import wx
# pygcgui provides the pyGCGuiFrame class which defines the actual GUI
import pygcgui
# pyTG provides control commands for the communication with the TinyG board
import pyTG
# parsegcode provides custom functions for preview and gcode parsing
import parsegcode
# Other imports
import os
import re
from subprocess import call
from ConfigParser import SafeConfigParser


# Class for the main program
class pyGCFrame ( pygcgui.pyGCGuiFrame ):
	
	def __init__( self, parent ):
		
		# Initialise the GUI in pygcgui
		pygcgui.pyGCGuiFrame.__init__(self,parent)
		
		# Connect GUI events to functions
		self.connect_button.Bind( wx.EVT_BUTTON, self.connect )
		self.disconnect_button.Bind( wx.EVT_BUTTON, self.disconnect )
		self.xset_textCtrl.Bind( wx.EVT_TEXT_ENTER, self.go_x )
		self.xgo_button.Bind( wx.EVT_BUTTON, self.go_x )
		self.xhome_button.Bind( wx.EVT_BUTTON, self.home_x )
		self.yset_textCtrl.Bind( wx.EVT_TEXT_ENTER, self.go_y )
		self.ygo_button.Bind( wx.EVT_BUTTON, self.go_y )
		self.yhome_button.Bind( wx.EVT_BUTTON, self.home_y )
		self.zset_textCtrl.Bind( wx.EVT_TEXT_ENTER, self.go_z )
		self.zgo_button.Bind( wx.EVT_BUTTON, self.go_z )
		self.zhome_button.Bind( wx.EVT_BUTTON, self.home_z )
		self.stop_button.Bind( wx.EVT_BUTTON, self.stop_all )
		self.allhome_button.Bind( wx.EVT_BUTTON, self.home_all )
		self.gcode_open_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_gcodefile )
		self.gcode_save_button.Bind( wx.EVT_BUTTON, self.save_gcodefile )
		self.gcode_run_button.Bind( wx.EVT_BUTTON, self.run_gcode )
		self.gcode_pause_button.Bind( wx.EVT_BUTTON, self.stop_gcode )
		self.gcode_textCtrl.Bind( wx.EVT_TEXT, self.update_preview )
		self.open_consolecode_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.open_console_code )
		self.save_consolecode_button.Bind( wx.EVT_BUTTON, self.save_console_code )
		self.console_button.Bind( wx.EVT_BUTTON, self.execute_console_code )
		self.Bind(wx.EVT_CHECKBOX, self.load_setting_changed, self.tool_cb )
		self.Bind(wx.EVT_CHECKBOX, self.load_setting_changed, self.offset_cb )
	
		# Global variable stopping the gcode procedure
		self.stopall = False
		
		# Load attributes (tool positions, paths, etc.) from config.ini
		config = SafeConfigParser()
		config.read('../config/config.ini')
		self.cfg_wheelorigin_V_x = config.getfloat('wheel-origin','V_x')
		self.cfg_wheelorigin_V_y = config.getfloat('wheel-origin','V_y')
		self.cfg_wheelorigin_H_x = config.getfloat('wheel-origin','H_x')
		self.cfg_wheelorigin_H_y = config.getfloat('wheel-origin','H_y')
		self.cfg_wheelorigin_z_fly = config.getfloat('wheel-origin','z_fly')
		self.cfg_wheelorigin_z_touch = config.getfloat('wheel-origin','z_touch')		
		self.cfg_scribeorigin_x = config.getfloat('scribe-origin','x')
		self.cfg_scribeorigin_y = config.getfloat('scribe-origin','y')
		self.cfg_scribeorigin_z_fly = config.getfloat('scribe-origin','z_fly')
		self.cfg_scribeorigin_z_touch = config.getfloat('scribe-origin','z_touch')
		self.cfg_minwheellength = config.getfloat('Misc','Min-wheel-length')	
		self.cfg_dxf2gcode_config_path = config.get('Misc','dxf2gcode-config-path')
		self.cfg_dxf2gcode_path = config.get('Misc','dxf2gcode-path')
		
		# Overwrite config of the external dxf2gcode program
		f = open(self.cfg_dxf2gcode_config_path,"r")
		configlines = f.readlines()
		f.close()
		newconfig = ""
		for l in configlines:
			if 'axis3_retract' in l:
				newconfig += "\taxis3_retract = "+str(self.cfg_scribeorigin_z_fly)+"\n"
			elif 'axis3_start_mill_depth' in l:
				newconfig += "\taxis3_start_mill_depth = "+str(self.cfg_scribeorigin_z_touch)+"\n"
			elif 'axis3_mill_depth' in l:
				newconfig += "\taxis3_mill_depth = "+str(self.cfg_scribeorigin_z_touch)+"\n"
			else:
				newconfig += l
		f = open(self.cfg_dxf2gcode_config_path,"w")
		f.write(newconfig)
		f.close()
		
		# Set the default sample thickness
		# Here, all configs relate to a default sample thickness of 2.2mm (standard FTO in our lab)
		self.samplethickness = 2.2
		

	def __del__( self ):
		pass
	
	
	# Connect to the TinyG board
	def connect( self, event ):
		# Automatic connection
		if self.port_comboBox.GetValue() == u"automatic":
			self.autoconnect()
			return
		# Manual connection
		if pyTG.connect(port=self.port_comboBox.GetValue()):
			self.statusBar.SetStatusText("Connection to TinyG established.")
			self.connection_staticText.SetLabel("connected")
			self.show_position()
		# No connection possible
		else:
			self.statusBar.SetStatusText("Failed to establish connection to TinyG. Check physical connection and port name.")
			
	
	# Automatic connection to some standard ports
	def autoconnect( self ):
		portlist = [u"/dev/ttyUSB0",u"/dev/ttyUSB1",u"/dev/ttyUSB2",u"/dev/ttyUSB3",u"/dev/ttyUSB4",u"/dev/ttyUSB5",u"COM1",u"COM2",u"COM3",u"COM4"]
		# Try all the ports in the 'portlist' until one works
		for p in portlist:
			if pyTG.connect(port=p):			
				self.statusBar.SetStatusText("Connection to TinyG established via "+p+".")
				self.connection_staticText.SetLabel("connected")
				self.show_position()
				return
		# Automatic connection failed
		self.statusBar.SetStatusText("Failed to auto-connect to TinyG. Check connection and enter port name manually.")
	
	
	# Disconnect from the TinyG board
	def disconnect( self, event ):
		if pyTG.close():
			self.statusBar.SetStatusText("TinyG connection closed.")
		self.connection_staticText.SetLabel("disconnected")
	
	
	# Readout positions and update display
	def show_position(self):
		output = pyTG.cmd("$posx")
		self.xread_textCtrl.SetValue(str(float(output[18:26])))
		output = pyTG.cmd("$posy")
		self.yread_textCtrl.SetValue(str(float(output[18:26])))
		output = pyTG.cmd("$posz")
		self.zread_textCtrl.SetValue(str(float(output[18:26])))

	
	# Zero x axis (manual control mode)
	def zero_x( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.3X")
		
	# Move x axis to set position (manual control mode)
	def go_x( self, event ):
		if float(self.xset_textCtrl.GetValue()) < 0:
			self.xset_textCtrl.SetValue("0.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if float(self.xset_textCtrl.GetValue()) > 280:
			self.xset_textCtrl.SetValue("280.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		output = pyTG.cmd("G0X"+str(self.xset_textCtrl.GetValue()))
		self.show_position()


	# Home x axis (manual control mode)
	def home_x( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.2X0")
		self.xread_textCtrl.SetValue("0.000")
		self.xset_textCtrl.SetValue("0.000")

	
	# Zero y axis (manual control mode)
	def zero_y( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.3Y")

	
	# Move x axis to set position (manual control mode)
	def go_y( self, event ):
		if float(self.yset_textCtrl.GetValue()) < 0:
			self.yset_textCtrl.SetValue("0.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if float(self.yset_textCtrl.GetValue()) > 280:
			self.yset_textCtrl.SetValue("280.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		output = pyTG.cmd("G0Y"+str(self.yset_textCtrl.GetValue()))
		self.show_position()

	
	# Home y axis (manual control mode)
	def home_y( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.2Y0")
		self.xread_textCtrl.SetValue("0.000")
		self.xset_textCtrl.SetValue("0.000")
	
	
	# Zero y axis (manual control mode)
	def zero_z( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.3Z")
	
	
	# Move x axis to set position (manual control mode)
	def go_z( self, event ):
		if float(self.zset_textCtrl.GetValue()) > 0:
			self.zset_textCtrl.SetValue("0.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if float(self.zset_textCtrl.GetValue()) < -75:
			self.zset_textCtrl.SetValue("-75.000")
			self.statusBar.SetStatusText("Value out of range!")
			return
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		output = pyTG.cmd("G0Z"+str(self.zset_textCtrl.GetValue()))
		self.show_position()


	# Home y axis (manual control mode)
	def home_z( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.2Z0")
		self.xread_textCtrl.SetValue("0.000")
		self.xset_textCtrl.SetValue("0.000")

	
	# Stop everything (manual control mode)
	def stop_all( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("!")
	
	
	# Zero all axes (manual control mode)
	def zero_all( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.3X0Y0Z0")
	
	
	# Home all axes (manual control mode)
	def home_all( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		pyTG.cmd("G28.2X0Y0Z0")
		self.xread_textCtrl.SetValue("0.000")
		self.yread_textCtrl.SetValue("0.000")
		self.zread_textCtrl.SetValue("0.000")
		self.xset_textCtrl.SetValue("0.000")
		self.yset_textCtrl.SetValue("0.000")
		self.zset_textCtrl.SetValue("0.000")
		
	
	# Load a gcode file (gcode mode)
	def load_gcodefile( self, event ):
		path = self.gcode_open_filePicker.GetPath()
		# If a dxf file is selected, convert it using dxf2gcode
		if path[-3:] == "dxf":
			lines = self.dxf2gcode(path)
		# Otherwise open .gcode/.ngc file
		else:
			f = open(path,"r")
			lines = f.readlines()
			f.close()
		# Allow different thicknesses, open thickness dialog
		dlg = pygcgui.ThicknessDialog()
		response = dlg.ShowModal()
		if response == wx.ID_OK:
			self.samplethickness = float(dlg.comboBox1.GetValue()[:3])
		dlg.Destroy()	
		# 'Build up' gcode block
		# The existing gcode has to be changed to glasscutter specific gcode depending on which tool is used, which sample thickness, etc.
		block = ""
		# Change z positions dependent on selected sample thickness
		for l in lines:
			if "Z" in l:
				index = l.find("Z")
				# Find the actual value in gcode line containing a z value
				zstring = re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
				z = float(zstring)
				newz = z + (self.samplethickness-2.2)
				l = l.replace(zstring,str(newz))
			block += l
		# If selected, prepare automatic tool selection (vertical/horizontal lines with wheel, everything else with scribe)
		if self.tool_cb.GetValue():
			block = self.automatic_tool_selection(lines)
		# Update gcode text field
		self.gcode_textCtrl.SetValue(block)
		# Draw preview
		self.update_preview(None)


	# Force the user to reload the file if settings are changed after the file was loaded
	# This is necessary, as most of the 'logic' is in the load_gcodefile function
	def load_setting_changed( self, evt ):
		if self.gcode_textCtrl.GetValue() != "":
			dlg = wx.MessageDialog(self, "You changed the loading settings. Please reload your file to proceed.", "Reload File", wx.OK | wx.ICON_WARNING)
			dlg.ShowModal()
			dlg.Destroy()
			self.gcode_textCtrl.SetValue("")
			self.update_preview(None)


	# Do automatic tool selection (vertical/horizontal lines with wheel cutter, everything else with scribe)
	def automatic_tool_selection( self, lines ):
		# This changes the loaded Gcode and includes custom flag commands for tool changes CTV,CTH (non-standard gcode)!
		block = "F4000\n"
		vblock = "G0 Z-30.0\nG0 X10.0 Y10.0\n> CTV\n"
		hblock = "G0 Z-30.0\nG0 X10.0 Y10.0\n> CTH\n"
		# Vertical straight lines
		xoffset_y = self.cfg_wheelorigin_V_x-self.cfg_scribeorigin_x
		yoffset_y = self.cfg_wheelorigin_V_y-self.cfg_scribeorigin_y
		# Horizontal straight lines
		xoffset_x = self.cfg_wheelorigin_H_x-self.cfg_scribeorigin_x
		yoffset_x = self.cfg_wheelorigin_H_y-self.cfg_scribeorigin_y
		mini = parsegcode.zmin(lines)
		zsafe = str(self.cfg_wheelorigin_z_fly+(self.samplethickness-2.2))
		z=0
		x=0
		y=0
		newx = 0
		newy = 0
		xindex = 0
		yindex = 0
		# This for loop changes the gcode if necessary for the different tools (long straight lines with wheel cutter)
		for i,l in enumerate(lines):
			if l[:2] != "G0" and l[:2] != "G1":
				continue
			if "Z" in l:
				index = l.find("Z")
				z=float(re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0])
			if "X" in l:
				index = l.find("X")
				xindex = index
				newx=float(re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0])
			if "Y" in l:
				index = l.find("Y")
				yindex = index
				newy=float(re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0])
			# vertical lines with wheel cutter
			if abs(newy-y) > self.cfg_minwheellength and newx == x and z == mini:
				vblock += "G0 Z"+zsafe+"\n"
				vblock += "G0 X"+str(x+xoffset_y)+" Y"+str(y+yoffset_y)+"\n"
				vblock += "G0 Z"+str(self.cfg_wheelorigin_z_touch+(self.samplethickness-2.2))+"\n"
				vblock += "G0 X"+str(newx+xoffset_y)+" Y"+str(newy+yoffset_y)+"\n"
				vblock += "G0 Z"+zsafe+"\n"
			# horizontal lines with wheel cutter
			elif abs(newx-x) > self.cfg_minwheellength and newy == y and z == mini:
				hblock += "G0 Z"+zsafe+"\n"
				hblock += "G0 X"+str(x+xoffset_x)+" Y"+str(y+yoffset_x)+"\n"
				hblock += "G0 Z"+str(self.cfg_wheelorigin_z_touch+(self.samplethickness-2.2))+"\n"
				hblock += "G0 X"+str(newx+xoffset_x)+" Y"+str(newy+yoffset_x)+"\n"
				hblock += "G0 Z"+zsafe+"\n"
			else:
				# change z with thickness
				if "Z" in l:
					index = l.find("Z")
					zstring = re.findall(r"[-+]?\d*\.\d+|\d+", l[index:])[0]
					z = float(zstring)
					newz = z + (self.samplethickness-2.2)
					l = l.replace(zstring,str(newz))
				block += l
			x=newx
			y=newy
		block+=vblock
		block+=hblock
		return block
	
	
	# convert dxf files to gcode using external program	dxf2gcode (https://sourceforge.net/projects/dxf2gcode/)
	def dxf2gcode( self, path ):		
		call("python "+cfg_dxf2gcode_path+" -q -f "+path+" -e "+path[:-3]+"ngc", shell=True)
		f = open(path[:-3]+"ngc","r")
		lines = f.readlines()
		f.close()
		return lines


	# Wrapper for preview update
	def update_preview( self, event ):
		block = self.gcode_textCtrl.GetValue()
		lines = block.split("\n")
		self.preview(lines)

	
	# Draw preview, different tools should have different functions (still buggy!!!)
	def preview( self, lines ):
		tooloff = [self.cfg_scribeorigin_x-self.cfg_wheelorigin_V_x, self.cfg_scribeorigin_x-self.cfg_wheelorigin_H_x, self.cfg_scribeorigin_y-self.cfg_wheelorigin_V_y, self.cfg_scribeorigin_y-self.cfg_wheelorigin_H_y]
		layers, layers_z, step = parsegcode.parsedraw(lines,tooloffset=tooloff)
		different_z = sorted(list(set(layers_z)))
		colors=["GREY","GREY","BLUE","GREY","RED","GREY","GREY","BLACK","RED"]
		scal = 2
		w, h = 285*scal, 285*scal
		bmp = wx.EmptyBitmap(w, h)
		bmp.LoadFile( "background.bmp", wx.BITMAP_TYPE_ANY )
		dc = wx.MemoryDC()
		dc.SelectObject(bmp)
		#dc.Clear()
		oldpair=[0,0]
		for s in range(step):
			for pair in layers[s]:
				ind = different_z.index(layers_z[s])
				dc.SetPen(wx.Pen(colors[ind], 1))
				if not colors[ind] == "GREY":
					offx = 56
					offy = -85
					dc.DrawLine(int(float(oldpair[0])*scal)+offx, h-int(float(oldpair[1])*scal)+offy, int(float(pair[0])*scal)+offx, h-int(float(pair[1])*scal)+offy)
				oldpair = pair
		dc.SelectObject(wx.NullBitmap)
		self.gcode_bitmap.SetBitmap(bmp)


    # Save gcode from gcode text field to file
	def save_gcodefile( self, event ):
		saveFileDialog = wx.FileDialog(self, "Save GCode file", "", "",
                                   "GCode files (*.gcode)|*.gcode", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_CANCEL:
			return
		f = open(saveFileDialog.GetPath(),"w")
		f.write(self.gcode_textCtrl.GetValue())
		f.close()

	
	# Run gcode (This runs whatever is in the gcode text field)
	def run_gcode( self, event ):
		# Check connectivity
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		# Remember user to select scriber as the first tool
		dlg = wx.MessageDialog(self, "Change tool to scriber (S)!", "Tool Change", wx.OK | wx.ICON_WARNING)
		dlg.ShowModal()
		dlg.Destroy()
		# If using glass spacers (default), then set the corresponding offset to the origin
		if self.offset_cb.GetValue():
			self.home_all(None)
			pyTG.cmd("G92 X0 Y0 Z0")
			pyTG.cmd("G0 X"+str(self.cfg_scribeorigin_x)+" Y"+str(self.cfg_scribeorigin_y)+" Z0")
			pyTG.cmd("G92 X0 Y0 Z0")
		# Check if there are commands in the gcode text field
		inp = self.gcode_textCtrl.GetValue()
		if inp == "":
			self.statusBar.SetStatusText("No commands to execute.")
			return
		cmdlist = inp.split('\n')
		# Remember user again to select scriber as the first tool
		dlg2 = wx.MessageDialog(self, "Is the tool set to the right position (S)?", "Tool Change", wx.OK | wx.ICON_WARNING)
		dlg2.ShowModal()
		dlg2.Destroy()
		# Run the commands line by line
		for l in cmdlist:
			# Yield keeps the gui responsive
			wx.Yield()
			# Emergency stop (gui button)
			if self.stopall:
				self.stopall = False
				return
			if not l == "":
				# Custom gcode for vertical and horizontal lines (for wheel cutter) start with ">"
				if l[0] == ">":
					msg = ""
					# Commands for horizontal lines are initialised with "> CTH", for vertical lines with "> CTV"
					if l[4] == "H":
						msg = "Change tool to horizontal wheel (H)!"
					else:
						msg = "Change tool to vertical wheel (V)!"
					# Dialog to ask user to change the tool
					dlg = wx.MessageDialog(self, msg, "Tool Change", wx.OK | wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
					# Dialog to make sure the user has changed the tool correctly
					dlg2 = wx.MessageDialog(self, "Is the tool set to the right position?", "Tool Change", wx.OK | wx.ICON_WARNING)
					dlg2.ShowModal()
					dlg2.Destroy()
					# The tool head sometimes moves during tool change, so home again for correct positioning
					self.home_all(None)
					# Go to a safe starting position (which is away from the datum bars)
					pyTG.cmd("G0 X50 Y50 Z0")
				# Ignore comment lines, starting with "#"
				if not l[0] == "#":
					# Run command
					output = pyTG.cmd(l)
					# try to update the position value display during the run (still buggy!)
					if 'pos' in output:
						try:
							self.set_position_control(output.split()[-1])
						except:
							None
		# Bring tool head up (z=0), at the end of run
		pyTG.cmd("G0 Z0")
		self.show_position()


	# Emergency stop (triggered via GUI button)
	def stop_gcode( self, event ):
		self.stopall = True


	# Load text file with console code (e.g. TinyG-scripts .tg)
	def open_console_code( self, event ):
		path = self.open_consolecode_filePicker.GetPath()
		f = open(path,"r")
		lines = f.readlines()
		f.close()
		block = ""
		for l in lines:
			block += l
		self.console_textCtrl.SetValue(block)


	# Save text file with console code (as TinyG-script .tg)
	def save_console_code( self, event ):
		saveFileDialog = wx.FileDialog(self, "Save tg file", "", "",
                                   "TinyG-script files (*.tg)|*.tg", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if saveFileDialog.ShowModal() == wx.ID_CANCEL:
			return
		f = open(saveFileDialog.GetPath(),"w")
		f.write(self.console_textCtrl.GetValue())
		f.close()


	# Run console code on the TinyG
	def execute_console_code( self, event ):
		if self.connection_staticText.GetLabel() == "disconnected":
			self.statusBar.SetStatusText("No TinyG connection.")
			return
		inp = self.console_textCtrl.GetValue()
		cmdlist = inp.split('\n')
		for l in cmdlist:
			self.statusBar.SetStatusText(l)
			if not l == "":
				if not l[0] == "#":
					self.console_output_textCtrl.AppendText(">>>"+l+"\n")
					output = pyTG.cmd(l)
					self.console_output_textCtrl.AppendText(output)
					self.m_panel3.Refresh()
					if 'pos' in output:
						try:
							self.set_position_control(output.split()[-1])
						except:
							None
		self.show_position()
	
	
	# Find positions in the return output of the TinyG and update the x,y,z value display
	def set_position_control(self, output):
		if 'posx:' in output:
			index = output.find('posx:')
			if 'posx:-' in output:
				number = output[index+6:index+12]
			else:
				number = output[index+5:index+11]
			self.xread_textCtrl.SetValue(number)
		if 'posy:' in output:
			index = output.find('posy:')
			if 'posy:-' in output:
				number = output[index+6:index+12]
			else:
				number = output[index+5:index+11]
			self.yread_textCtrl.SetValue(number)
		if 'posz:' in output:
			index = output.find('posz:')
			if 'posz:-' in output:
				number = output[index+6:index+12]
			else:
				number = output[index+6:index+11]
			if number[-1] == ",":
				number = number[:-1]
			if 'posz:-' in output:
				self.zread_textCtrl.SetValue("-"+number)
			else:
				self.zread_textCtrl.SetValue(number)


#---------------------------
# Run the program
app = wx.App(False)
frame = pyGCFrame(None)
frame.Show(True)
app.MainLoop()
#---------------------------
