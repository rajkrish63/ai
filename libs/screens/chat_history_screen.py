from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

Builder.load_string("""
<ChatHistoryScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "History"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.manager.current = 'chat']]

        MDScrollView:
            MDList:
                id: history_list
                OneLineListItem:
                    text: "Previous Chat 1"
                OneLineListItem:
                    text: "Previous Chat 2"
""")

class ChatHistoryScreen(MDScreen):
    """
    Screen for viewing chat history.
    """
    pass
