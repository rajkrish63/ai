from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivymd.utils.fitimage import FitImage

Builder.load_string("""
<ChatBubble>:
    size_hint_y: None
    height: self.minimum_height
    padding: "12dp"
    radius: [18, 18, 18, 0] if self.is_user else [18, 18, 0, 18]
    md_bg_color: 
        app.theme_cls.primary_color if self.is_user else app.theme_cls.bg_darkest
    elevation: 1 if self.is_user else 0
    pos_hint: {"right": 1} if self.is_user else {"left": 1}
    anchor_x: "right" if self.is_user else "left"
    
    MDLabel:
        text: root.text
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1] if root.is_user else app.theme_cls.text_color
        size_hint_y: None
        height: self.texture_size[1]
        markup: True
""")

class ChatBubble(MDCard):
    """
    A chat bubble component to display messages.
    """
    text = StringProperty("")
    is_user = BooleanProperty(True)
