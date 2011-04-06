from django.utils import translation
from django.conf import settings

def set_user_language(user):
    try:
        lang = user.get_profile().language
        if lang:
            language = translation.to_locale(lang)
            translation.activate(language)
        else:
            # if user has no language and current is not default, then set the default
            # this is to avoid using the last selected language
            if not translation.get_language() == settings.LANGUAGE_CODE:
                language = translation.to_locale(settings.LANGUAGE_CODE)
                translation.activate(language)
    except:
        # in case of fail do nothing
        pass