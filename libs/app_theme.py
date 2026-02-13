from kivymd.app import MDApp

class AppTheme:
    """
    Handles the theme configuration for the AntiGravity AI application.
    """
    @staticmethod
    def set_default_theme(app: MDApp):
        """
        Sets the default theme settings for the application.
        """
        app.theme_cls.theme_style = "Dark"
        app.theme_cls.primary_palette = "DeepPurple"
        app.theme_cls.accent_palette = "Teal"
        app.theme_cls.material_style = "M3"
