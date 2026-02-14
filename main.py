import logging
import os
import sys
import traceback

# 1. SETUP RESILIENT LOGGING IMMEDIATELY
def setup_logging():
    try:
        # Standard Kivy/P4A private storage path
        private_dir = os.environ.get('ANDROID_PRIVATE', os.getcwd())
        log_path = os.path.join(private_dir, 'app_debug.log')
        
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        print(f"DEBUG_APP: Logging to {log_path}")
    except Exception as e:
        print(f"CRITICAL: Logging setup failed: {e}")
        logging.basicConfig(level=logging.DEBUG)

setup_logging()
logging.info("--- STARTING BOOTSTRAP ---")
logging.info(f"Python version: {sys.version}")

# 2. HELPER FOR SAFE IMPORTS
def safe_import(module_name, from_list=None):
    try:
        logging.info(f"Importing {module_name}...")
        if from_list:
            mod = __import__(module_name, fromlist=from_list)
        else:
            mod = __import__(module_name)
        logging.info(f"Successfully imported {module_name}")
        return mod
    except Exception as e:
        logging.error(f"FATAL IMPORT ERROR [{module_name}]: {e}")
        logging.error(traceback.format_exc())
        return None

# 3. CORE IMPORTS (Lazy loaded later in MDApp)
kivy = safe_import('kivy')
if kivy:
    kivy.require('2.1.0')

# 4. DEFINE UI CLASSES EARLY (Placeholder components if imports fail)
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class MainLayout(BoxLayout):
    pass

# Placeholder screens if imports fail
class ErrorScreen(BoxLayout):
    pass

# 5. DEFINE THE APP CLASS
class AntiGravityAI(object):
    # This will be replaced by the actual MDApp if import succeeds
    pass

MDApp = safe_import('kivymd.app', ['MDApp'])
if MDApp:
    class AntiGravityAI(MDApp.MDApp):
        def build(self):
            try:
                logging.info("Building Application UI...")
                
                # Import theme and screens inside build to catch errors
                AppTheme = safe_import('libs.app_theme', ['AppTheme'])
                if AppTheme:
                    AppTheme.AppTheme.set_default_theme(self)
                
                # Load UI
                self.load_kv_string()
                
                # Import screens
                safe_import('libs.screens.chat_screen')
                safe_import('libs.screens.model_selection_screen')
                safe_import('libs.screens.settings_screen')
                safe_import('libs.screens.chat_history_screen')
                
                # Create screen manager layout
                from kivymd.uix.boxlayout import MDBoxLayout
                class MainLayout(MDBoxLayout):
                    pass
                
                return MainLayout()
            except Exception as e:
                logging.error(f"CRITICAL ERROR IN BUILD: {e}")
                logging.error(traceback.format_exc())
                # Return a simple label to show the error on screen
                from kivy.uix.label import Label
                return Label(text=f"CRITICAL STARTUP ERROR:\n{e}\nCheck app_debug.log")

        def load_kv_string(self):
            Builder.load_string("""
<MainLayout>:
    orientation: 'vertical'
    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            Screen:
                name: 'chat'
                MDLabel:
                    text: "Chat Screen Placeholder"
                    halign: "center"
            # Actual screens will be added here or replaced
        """)

        def switch_screen(self, screen_name):
            if self.root and 'screen_manager' in self.root.ids:
                self.root.ids.screen_manager.current = screen_name

# 6. APP ENTRY POINT
if __name__ == "__main__":
    try:
        if AntiGravityAI != object:
            app = AntiGravityAI()
            app.run()
        else:
            logging.error("MDApp could not be loaded. Cannot run.")
    except Exception as e:
        logging.error(f"PROCESS CRASHED: {e}")
        logging.error(traceback.format_exc())
