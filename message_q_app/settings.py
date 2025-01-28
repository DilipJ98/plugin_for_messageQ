def plugin_settings(settings):
    pass
    """
    Update the provided settings module with any app-specific settings.
    """
    settings.FEATURES['ENABLE_MESSAGE_Q_APP'] = True  
    if 'message_q_app' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append('message_q_app')
    # settings.MESSAGE_Q_APP_POLICY = 'default_policy'

