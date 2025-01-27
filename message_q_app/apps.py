from django.apps import AppConfig

class MessageQAppConfig(AppConfig):
    """
    Configuration for the my_app Django application.
    """

    name = 'message_q_app'

    plugin_app = {
        # Configuration for Plugin URLs
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'message_q_app',  # The namespace for your app's URLs
                # 'regex': '^message_q_app/',  # Regex for URL routing
                'relative_path': 'urls',  # Path to the URLs module within the app
            }
        },
        
        # Configuration for Plugin Settings
        'settings_config': {
            'lms.djangoapp': {
                'production': {
                    'relative_path': 'settings',  # Path to production settings
                },
                'common': {
                    'relative_path': 'settings',  # Path to common settings
                },
            }
        },
    }
