"""
message_q_app Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins.constants import (
    PluginURLs, PluginSettings, PluginSignals
)



class MessageQAppConfig(AppConfig):
    """
    Configuration for the message_q_app Django application.
    """

    name = 'message_q_app'

    
 # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {

        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {

            # Configure the Plugin URLs for each project type, as needed. The full list of project types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L14 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: 'message_q_app',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: 'message_q_app',

                # The regex to provide to django's urls.url.
                # Optional; Defaults to r''.
                # PluginURLs.REGEX: r'^/message_q_app/',

                # The python path (relative to this app) to the URLs module to be plugged into the project.
                # Optional; Defaults to 'urls'.
                PluginURLs.RELATIVE_PATH: 'urls',
            }
        },

        # Configuration setting for Plugin Settings for this app.
        PluginSettings.CONFIG: {

            # Configure the Plugin Settings for each Project Type, as needed. The full list of setting types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L25 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # Configure each settings, as needed.
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings',
                },
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings',
                },
            }
        },
        
        # PluginSignals.CONFIG: {
        #     'lms.djangoapp': {
        #         PluginSignals.RELATIVE_PATH: 'signals',
        #     }
        # }        
    }
