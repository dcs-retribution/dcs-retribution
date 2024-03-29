from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QTextEdit,
)

from qt_ui.windows.preferences.QLiberationPreferences import QLiberationPreferences


class QLiberationFirstStartWindow(QDialog):
    def __init__(self):
        super(QLiberationFirstStartWindow, self).__init__()

        self.setModal(True)
        self.setWindowTitle("First start configuration")
        self.setMinimumSize(500, 200)
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
        )
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.preferences = QLiberationPreferences()

        WARN_TEXT = """
        <strong>Welcome to DCS Retribution !</strong>
        <br/><br>
        <strong>Please take 30 seconds to read this :</strong>
        
        <p>DCS Retribution will modify this file in your DCS installation directory :</p>
        <br/>
        <strong>&lt;dcs_installation_directory&gt;/Scripts/MissionScripting.lua</strong><br/> 
        
        <p>
        This will disable some security limits of the DCS World Lua scripting environment, in order to allow communication between DCS World and DCS Retribution.
        However, the modification of this file could potentially grant access to your filesystem to malicious DCS mission files.
        </p>
        
        <p>So, you should not join untrusted servers or open untrusted mission files within DCS world while DCS Retribution is running.</p>
        
        <p>
        DCS Retribution will restore your original MissionScripting file when it closes.        
        </p>
        
        <p>
        However, should DCS Retribution encounter an unexpected crash (which should not happen), the MissionScripting file might not be restored.
        If that occurs, you can use the backup file saved in the DCS Retribution directory there :
        </p>
        
        <br/>
        <strong>./resources/scripts/MissionScripting.original.lua</strong><br/>
        
        <p>Then copy it to your DCS installation directory to replace this file :</p>
        
        <br/>
        <strong>&lt;dcs_installation_directory&gt;/Scripts/MissionScripting.lua</strong><br/>
        
        <p>As you click on the button below, the file will be replaced in your DCS installation directory.</p>
        
        <br/>
        <p>If you leave the DCS Installation Directory empty, DCS Retribution can not automatically replace the MissionScripting.lua and will therefore not work correctly!
        In this case, you need to edit the file yourself. The easiest way to do it is to replace the original file with the file in dcs-retribution distribution (&lt;dcs_retribution_installation&gt;/resources/scripts/MissionScripting.lua).
        <br/><br/>You can find more information on how to manually change this file in the Retribution Wiki (Page: Dedicated Server Guide) on GitHub.</p>

        
        <br/><br/>
        
        <strong>Thank you for reading !</strong>
        """
        self.warning_text = QTextEdit(WARN_TEXT)
        self.warning_text.setReadOnly(True)
        self.apply_button = QPushButton("I have read everything and I Accept")
        self.apply_button.clicked.connect(lambda: self.apply())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.preferences)
        layout.addWidget(self.warning_text)
        layout.addStretch()
        apply_btn_layout = QHBoxLayout()
        apply_btn_layout.addStretch()
        apply_btn_layout.addWidget(self.apply_button)
        layout.addLayout(apply_btn_layout)
        self.setLayout(layout)

    def apply(self):
        print("Applying changes")
        if self.preferences.apply():
            self.close()
