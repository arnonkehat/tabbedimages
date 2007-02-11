import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import ArgumentException
from System.Drawing import Bitmap
from System.Windows.Forms import (
    Application, DialogResult, DockStyle, Form, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, PictureBox, PictureBoxSizeMode, 
    TabControl, TabAlignment, 
    TabPage, ToolBar, ToolStripMenuItem    
)
from System.IO import Path


class MainForm(Form):
    
    def __init__(self):
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        
        self.initTabControl()
        self.initMenu()
        

    def initTabControl(self):
        self.tabControl = TabControl(
            Dock = DockStyle.Fill,
            Alignment = TabAlignment.Bottom
        )
        self.Controls.Add(self.tabControl)
        
    
    def initMenu(self):
        menuStrip = MenuStrip(
            Name = "Main MenuStrip",
            Dock = DockStyle.Top
        )        
        fileMenu = ToolStripMenuItem(
            Name = 'File Menu',
            Text = '&File'
        )        
        openMenuItem = ToolStripMenuItem(
            Name = 'Open',
            Text = '&Open...'
        )
        openMenuItem.Click += self.onOpen
        
        fileMenu.DropDownItems.Add(openMenuItem)        
        menuStrip.Items.Add(fileMenu)
        
        self.Controls.Add(menuStrip)

    
    def getImage(self, fileName):        
        try:
            return Bitmap(fileName)
        except ArgumentException:
            MessageBox.Show(fileName + " doesnt't appear to be a valid image file", 
                            "Invalid image format",
                            MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
            return None
    
    
    def getPictureBox(self, image):    
        return PictureBox(
            Dock = DockStyle.Fill,
            Image = image,                
            SizeMode = PictureBoxSizeMode.StretchImage
        )
        
        
    def createTab(self, fileName):
        image = self.getImage(fileName)
        if not image:
            return
        
        tabPage = TabPage()
        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage
        tabPage.Text = Path.GetFileName(fileName)
        pictureBox = self.getPictureBox(image)
        tabPage.Controls.Add(pictureBox)        
            
            
    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog(
            Filter = "Images (*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*",
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:                
            for fileName in openFileDialog.FileNames:
                self.createTab(fileName)
        

Application.EnableVisualStyles()
Application.Run(MainForm())