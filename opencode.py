import sys
import os
import logging

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    filename="plugin.log",
    filemode="w",
)

identifier = "opencode_action"

try:
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        version = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
        venv_site_packages = os.path.join(venv, "lib", version, "site-packages")

        if venv_site_packages in sys.path:
            sys.path.remove(venv_site_packages)

        sys.path.insert(0, venv_site_packages)

    import subprocess
    import shutil
    import wx
    from kipy import KiCad
except Exception as e:
    logging.exception("Import Module")

class OpenCodePlugin(wx.Dialog):
    def __init__(self):
        super(OpenCodePlugin, self).__init__(None)
        self.kicad = KiCad()
        self.board = self.kicad.get_board()
        self.board_path = self.board.document.board_filename
        self.identifier = identifier
    
    def run(self):
        try:
            if not self.board_path:
                wx.MessageBox("No board file open - please save your project first", style=wx.ICON_ERROR)
                return

            project_dir = os.path.dirname(self.board_path)

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

if __name__ == "__main__":
    oc = OpenCodePlugin()
    oc.ShowModal()
    oc.Destroy()