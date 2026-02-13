from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from libs.components.chat_bubble import ChatBubble
from kivy.properties import ObjectProperty

Builder.load_string("""
<ChatScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.bg_normal

        MDTopAppBar:
            title: "AntiGravity AI"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]
            right_action_items: [["dots-vertical", lambda x: app.open_settings()]]

        MDScrollView:
            padding: [0, "10dp", 0, "10dp"]
            MDList:
                id: chat_list
                spacing: "12dp"
                padding: "12dp"

        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: "8dp"
            spacing: "8dp"
            md_bg_color: app.theme_cls.bg_dark

            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                pos_hint: {"center_y": .5}

            MDTextField:
                id: message_input
                hint_text: "Type a message..."
                mode: "round"
                fill_color_normal: app.theme_cls.bg_light
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            MDIconButton:
                icon: "send"
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                on_release: root.send_message()
                pos_hint: {"center_y": .5}
""")

class ChatScreen(MDScreen):
    """
    Main chat interface.
    """
    def send_message(self):
        text = self.ids.message_input.text
        if text.strip():
            # Add user message
            self.ids.chat_list.add_widget(ChatBubble(text=text, is_user=True))
            self.ids.message_input.text = ""
            
            # Simulate AI response (placeholder)
            # In Phase 4, this will connect to the backend
            self.ids.chat_list.add_widget(ChatBubble(text="I'm a placeholder AI. Logic coming soon!", is_user=False))
