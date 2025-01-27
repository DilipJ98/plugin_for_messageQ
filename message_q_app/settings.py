def plugin_settings(settings):
    """
    Update the provided settings module with any app-specific settings.
    """
    settings.FEATURES['ENABLE_MESSAGE_Q_APP'] = True  
    settings.MESSAGE_Q_APP_POLICY = 'default_policy'

