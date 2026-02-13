from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from libs.components.model_card import ModelCard

Builder.load_string("""
<ModelSelectionScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Select Model"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.manager.current = 'chat']]

        MDScrollView:
            MDList:
                id: model_list
                padding: "16dp"
                spacing: "16dp"
""")

class ModelSelectionScreen(MDScreen):
    """
    Screen for selecting and managing AI models.
    """
    def on_enter(self):
        # Mock data for demonstration
        self.load_models()

    def load_models(self):
        self.ids.model_list.clear_widgets()
        models = [
            {"name": "SmolLM2-135M", "desc": "Lightweight, fast.", "size": "95 MB", "ram": "2 GB", "dl": True},
            {"name": "Gemma-2B", "desc": "Balanced performance.", "size": "1.2 GB", "ram": "4 GB", "dl": False},
        ]
        
        for model in models:
            card = ModelCard(
                model_name=model["name"],
                description=model["desc"],
                model_size=model["size"],
                ram_req=model["ram"],
                is_downloaded=model["dl"]
            )
            self.ids.model_list.add_widget(card)
