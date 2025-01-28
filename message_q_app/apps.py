# message_q_app/apps.py
from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginURLs, PluginSettings

class MessageQAppConfig(AppConfig):
    name = 'message_q_app'  # Python path to your app

    plugin_app = {
        # Register URLs for your plugin
        PluginURLs.CONFIG: {
            'lms.djangoapp': {
                PluginURLs.NAMESPACE: 'message_q_app',
                PluginURLs.REGEX: r'^api/message_q/',
                PluginURLs.RELATIVE_PATH: 'urls',
            }
        },
        # Register settings for your plugin (optional)
        PluginSettings.CONFIG: {
            'lms.djangoapp': {
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings',
                },
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings',
                },
            },
        },
    }