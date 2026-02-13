from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_string("""
<ModelCard>:
    orientation: "vertical"
    padding: "16dp"
    size_hint_y: None
    height: "140dp"
    radius: 12
    elevation: 2
    md_bg_color: app.theme_cls.bg_dark

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "40dp"
        spacing: "12dp"

        MDIcon:
            icon: "robot"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            pos_hint: {"center_y": .5}

        MDLabel:
            text: root.model_name
            font_style: "H6"
            bold: True
            pos_hint: {"center_y": .5}

    MDLabel:
        text: root.description
        theme_text_color: "Secondary"
        font_style: "Body2"
        size_hint_y: None
        height: "40dp"

    MDBoxLayout:
        orientation: "horizontal"
        spacing: "8dp"
        
        MDLabel:
            text: f"Size: {root.model_size}"
            theme_text_color: "Hint"
            font_style: "Caption"

        MDLabel:
            text: f"RAM: {root.ram_req}"
            theme_text_color: "Hint"
            font_style: "Caption"
            
        Widget:
            size_hint_x: 1

        MDRaisedButton:
            text: "Download" if not root.is_downloaded else "Select"
            md_bg_color: app.theme_cls.primary_color if not root.is_downloaded else app.theme_cls.accent_color
            on_release: root.on_action()
""")

class ModelCard(MDCard):
    """
    A card component to display AI model details and actions.
    """
    model_name = StringProperty("")
    description = StringProperty("")
    model_size = StringProperty("")
    ram_req = StringProperty("")
    is_downloaded = BooleanProperty(False)
    
    def on_action(self):
        # Placeholder for action handler
        print(f"Action triggered for {self.model_name}")
