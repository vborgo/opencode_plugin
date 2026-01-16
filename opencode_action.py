import subprocess
import os
import shutil
import pcbnew
import wx

class OpenCodePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Open OpenCode"
        self.category = "Utility"
        self.description = "Launches OpenCode in project directory"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
                os.path.dirname(__file__), 'opencode_logo.png')
        self.dark_icon_file_name = os.path.join(
                os.path.dirname(__file__), 'opencode_logo.png')

    def Run(self):
        try:
            # Get the current board file path
            board = pcbnew.GetBoard()
            board_path = board.GetFileName()
            
            if not board_path:
                wx.MessageBox("No board file open - please save your project first", style=wx.ICON_ERROR)
                return
            
            project_dir = os.path.dirname(board_path)
            
            # Check if opencode is available using bash -i to source .bashrc
            result = subprocess.run(['bash', '-i', '-c', 'which opencode'], capture_output=True, text=True)
            if result.returncode != 0:
                wx.MessageBox("OpenCode not found. Please install it first.", style=wx.ICON_ERROR)
                return

            # Open a terminal and launch OpenCode in the project directory
            subprocess.Popen([
                'gnome-terminal',
                '--working-directory=' + project_dir,
                '--',
                'bash', '-c', '-i', 'opencode; exec bash'
            ])
            
        except Exception as e:
            wx.MessageBox(f"Failed to launch OpenCode: {e}", style=wx.ICON_ERROR)
