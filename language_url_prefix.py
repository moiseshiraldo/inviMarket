# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.conf.urls import patterns
from django.core.urlresolvers import LocaleRegexURLResolver
from django.utils.translation import get_language

class CustomPrefixLocaleRegexURLResolver(LocaleRegexURLResolver):

    @property
    def regex(self):
        language_code = get_language()

        if language_code not in self._regex_dict:
            if language_code[:2] == settings.LANGUAGE_CODE:
                regex_compiled = re.compile('', re.UNICODE)
            else:
                regex_compiled = re.compile('^%s/' % language_code, re.UNICODE)

            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]


def custom_i18n_patterns(prefix, *args):
    """
    Adds the language code prefix to every URL pattern within this
    function, when the language not is the default language.
    This may only be used in the root URLconf, not in an included URLconf.

    """
    pattern_list = patterns(prefix, *args)
    if not settings.USE_I18N:
        return pattern_list
    return [CustomPrefixLocaleRegexURLResolver(pattern_list)]