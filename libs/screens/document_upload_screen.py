from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

Builder.load_string("""
<DocumentUploadScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Upload Documents"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.manager.current = 'chat']]

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "16dp"
                adaptive_height: True
                
                MDCard:
                    orientation: 'vertical'
                    padding: "16dp"
                    size_hint_y: None
                    height: "200dp"
                    radius: 12
                    md_bg_color: app.theme_cls.bg_dark
                    
                    MDIcon:
                        icon: "file-upload"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        font_size: "64sp"
                    
                    MDLabel:
                        text: "Upload PDF, DOCX, or TXT"
                        halign: "center"
                        theme_text_color: "Secondary"
                        font_style: "Body1"
                    
                    MDRaisedButton:
                        text: "Choose File"
                        pos_hint: {"center_x": .5}
                        md_bg_color: app.theme_cls.primary_color
                        on_release: root.choose_file()
                
                MDLabel:
                    text: "Uploaded Documents"
                    font_style: "H6"
                    bold: True
                    size_hint_y: None
                    height: "40dp"
                
                MDList:
                    id: document_list
                    
                    OneLineListItem:
                        text: "No documents uploaded yet"
                        theme_text_color: "Hint"
""")

class DocumentUploadScreen(MDScreen):
    """
    Screen for uploading and managing documents for RAG.
    """
    
    def choose_file(self):
        """Open file chooser dialog."""
        # This is a placeholder - actual file picker requires platform-specific code
        print("File chooser opened (implement with plyer or file picker)")
        # On Android, use plyer or android.permissions + jnius
        # For now, just show a message
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text="File picker not yet implemented").open()
    
    def on_enter(self):
        """Load document list when screen is entered."""
        self.load_documents()
    
    def load_documents(self):
        """Load and display uploaded documents."""
        # Placeholder - will be connected to DocumentService
        pass
