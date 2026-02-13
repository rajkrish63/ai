from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivy.lang import Builder

Builder.load_string("""
<SettingsScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Settings"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.manager.current = 'chat']]

        MDScrollView:
            MDList:
                id: settings_list
                
                OneLineListItem:
                    text: "Theme: Dark"
                    on_release: app.theme_cls.theme_style = "Light" if app.theme_cls.theme_style == "Dark" else "Dark"
                
                OneLineListItem:
                    text: "Clear Cache"
                
                OneLineListItem:
                    text: "About AntiGravity AI"
""")

class SettingsScreen(MDScreen):
    """
    Screen for application settings.
    """
    pass
