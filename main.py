from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from libs.app_theme import AppTheme

# Import screens
from libs.screens.chat_screen import ChatScreen
from libs.screens.model_selection_screen import ModelSelectionScreen
from libs.screens.settings_screen import SettingsScreen
from libs.screens.chat_history_screen import ChatHistoryScreen

# Define Navigation Drawer KV
Builder.load_string("""
<AppNavigationDrawer@MDNavigationDrawer>:
    id: nav_drawer
    radius: (0, 16, 16, 0)

    MDNavigationDrawerMenu:
        MDNavigationDrawerHeader:
            title: "AntiGravity AI"
            text: "Offline & Private"
            spacing: "4dp"
            padding: "12dp", 0, 0, "56dp"

        MDNavigationDrawerLabel:
            text: "Menu"

        DrawerClickableItem:
            icon: "message-text"
            text: "Chat"
            on_release: 
                app.switch_screen("chat")
                root.set_state("close")

        DrawerClickableItem:
            icon: "robot"
            text: "Models"
            on_release: 
                app.switch_screen("models")
                root.set_state("close")

        DrawerClickableItem:
            icon: "history"
            text: "History"
            on_release: 
                app.switch_screen("history")
                root.set_state("close")

        DrawerClickableItem:
            icon: "cog"
            text: "Settings"
            on_release: 
                app.switch_screen("settings")
                root.set_state("close")

<DrawerClickableItem@MDNavigationDrawerItem>:
    focus_color: app.theme_cls.accent_color
    text_color: app.theme_cls.text_color
    icon_color: app.theme_cls.text_color
    ripple_color: app.theme_cls.accent_color
    selected_color: app.theme_cls.accent_color

<MainLayout>:
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            
            ChatScreen:
                name: 'chat'
            
            ModelSelectionScreen:
                name: 'models'

            ChatHistoryScreen:
                name: 'history'

            SettingsScreen:
                name: 'settings'

        AppNavigationDrawer:
            id: nav_drawer
""")

from kivymd.uix.boxlayout import MDBoxLayout

class MainLayout(MDBoxLayout):
    pass

class AntiGravityAI(MDApp):
    """
    Main Application Class for AntiGravity AI.
    """
    def build(self):
        self.title = "AntiGravity AI"
        AppTheme.set_default_theme(self)
        return MainLayout()

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
    
    def open_settings(self):
        self.switch_screen("settings")

if __name__ == "__main__":
    AntiGravityAI().run()
