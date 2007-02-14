import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from icons import (
    CloseIcon, CopyIcon, NewIcon,
    OpenIcon, PasteIcon, SaveIcon
)
from cPickle import loads
from System import ArgumentException
from System.Drawing import Bitmap, Color
from System.Drawing.Imaging import ImageFormat
from System.Windows.Forms import (
    Application, Clipboard, DataObject, DialogResult, 
    DockStyle, Form, ImageList, MenuStrip,
    MessageBox, MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog, PictureBox, PictureBoxSizeMode, 
    SaveFileDialog, TabControl, TabAlignment, 
    TabPage, ToolStrip, ToolStripButton, 
    ToolStripMenuItem, ToolStripItemDisplayStyle
)
from System.IO import Path

FILTER = "Images (*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*"

class MainForm(Form):
    
    def __init__(self):
        Form.__init__(self)
        self.Text = 'Tabbed Image Viewer'
        self.Width = 350
        self.Height = 200
        
        self.initTabControl()
        self.initToolBar()
        self.initMenu()
        

    def initTabControl(self):
        self.tabControl = TabControl(
            Dock = DockStyle.Fill,
            Alignment = TabAlignment.Bottom
        )
        self.Controls.Add(self.tabControl)
        
    
    def createMenuItem(self, name, text, clickHandler=None):
        menuItem = ToolStripMenuItem(
            Name = name,
            Text = text
        )
        if clickHandler:
            menuItem.Click += clickHandler
        return menuItem
    
    
    def initMenu(self):
        menuStrip = MenuStrip(
            Name = "Main MenuStrip",
            Dock = DockStyle.Top
        )        
        fileMenu      = self.createMenuItem('File Menu', '&File')
        openMenuItem  = self.createMenuItem('Open', '&Open...', self.onOpen)
        saveMenuItem  = self.createMenuItem('Save', '&Save...', self.onSave)
        closeMenuItem = self.createMenuItem('Close', '&Close', self.onClose)
        exitMenuItem  = self.createMenuItem('Exit', 'E&xit', lambda *_: Application.Exit())
        
        fileMenu.DropDownItems.Add(openMenuItem)
        fileMenu.DropDownItems.Add(saveMenuItem)        
        fileMenu.DropDownItems.Add(closeMenuItem)   
        fileMenu.DropDownItems.Add(exitMenuItem)
        
        editMenu = self.createMenuItem('Edit Menu', '&Edit')
        copy =  self.createMenuItem('Copy', '&Copy', self.onCopy)
        paste = self.createMenuItem('Paste', '&Paste', self.onPaste)
        editMenu.DropDownItems.Add(copy)
        editMenu.DropDownItems.Add(paste)
        
        menuStrip.Items.Add(fileMenu)
        menuStrip.Items.Add(editMenu)
        
        self.Controls.Add(menuStrip)

    
    def initToolBar(self):
        toolBar = ToolStrip(
            Dock = DockStyle.Top
        )
        
        def addToolBarIcon(pickledIcon, clickHandler):
            icon = loads(pickledIcon)     
            button = ToolStripButton()
            button.ImageTransparentColor = Color.Magenta
            button.Image = icon
            button.DisplayStyle = ToolStripItemDisplayStyle.Image
            if clickHandler:
                button.Click += clickHandler
            toolBar.Items.Add(button)
        
        addToolBarIcon(NewIcon, None)
        addToolBarIcon(OpenIcon, self.onOpen)
        addToolBarIcon(SaveIcon, self.onSave)
        addToolBarIcon(CloseIcon, self.onClose)
        addToolBarIcon(CopyIcon, self.onCopy)
        addToolBarIcon(PasteIcon, self.onPaste)
                
        self.Controls.Add(toolBar)
        
        
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
            Image = image,                
            SizeMode = PictureBoxSizeMode.AutoSize
        )
        
        
    def createTab(self, image, label):        
        tabPage = TabPage()
        tabPage.Text = label
        pictureBox = self.getPictureBox(image)
        tabPage.Dock = DockStyle.Fill
        tabPage.AutoScroll = True
        tabPage.Controls.Add(pictureBox)
        
        self.tabControl.TabPages.Add(tabPage)
        self.tabControl.SelectedTab = tabPage
            
            
    def onOpen(self, _, __):
        openFileDialog = OpenFileDialog(
            Filter = FILTER,
            Multiselect = True
        )
        if openFileDialog.ShowDialog() == DialogResult.OK:                
            for fileName in openFileDialog.FileNames:                                
                image = self.getImage(fileName)
                if image:
                   self.createTab(image, Path.GetFileName(fileName))
        
                
    def onClose(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            self.tabControl.TabPages.Remove(selectedTab)
    
    
    def onCopy(self, _, __):
        dataObject = DataObject()
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            dataObject.SetImage(selectedTab.Controls[0].Image)
            Clipboard.SetDataObject(dataObject)
            
            
    def onPaste(self, _, __):
        dataObject = Clipboard.GetDataObject()
        if dataObject.ContainsImage():
            self.createTab(dataObject.GetImage(), "CLIPBOARD")
        
    def onSave(self, _, __):
        selectedTab = self.tabControl.SelectedTab
        if selectedTab:
            image = selectedTab.Controls[0].Image
            saveFileDialog = SaveFileDialog()
            saveFileDialog.Filter = FILTER
            if saveFileDialog.ShowDialog() == DialogResult.OK:
                extension = Path.GetExtension(saveFileDialog.FileName)
                format = ImageFormat.Jpeg
                if extension.lower() == "bmp":
                    format = ImageFormat.Bmp
                elif extension.lower() == "jpg":
                    format = ImageFormat.Jpeg                    
                elif extension.lower() == "gif":
                    format = ImageFormat.Gif
                image.Save(saveFileDialog.FileName, format)
                
                
        
Application.EnableVisualStyles()
Application.Run(MainForm())
