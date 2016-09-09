'''
Created on Aug 20, 2014

@author: abi
'''

from threading import current_thread, Lock
import gettext


class DeltaPyTranslation(gettext.NullTranslations):
    def __init__(self, fp):
        gettext.NullTranslations.__init__(self, fp)

        self._encoding = None
        self._locale_dir = None
        self._locale = None
        self._loaded_languages = {}
        self._lock = Lock()
    
    def setup(self, encoding, locale_dir, locale):
        self._encoding = encoding
        self._locale_dir = locale_dir
        self._locale = locale
 
    def get_language(self):
        locale = self.get_current_locale()
        if locale not in self._loaded_languages:
            with self._lock:
                if locale not in self._loaded_languages:
                    language = \
                        gettext.translation("messages",
                                            self._locale_dir,
                                            languages=[locale],
                                            codeset=self._encoding)
                    self._loaded_languages[locale] = language

        return self._loaded_languages[locale]
                
        
    def get_current_locale(self):
        thread = current_thread()
        locale = self._locale
        if hasattr(thread, '__LOCALE__'):
            forced_locale = getattr(thread, '__LOCALE__')
            if forced_locale is not None:
                locale = forced_locale
        return locale
    
    def gettext(self, message):
        language = self.get_language()
        return language.gettext(message)

    def lgettext(self, message):
        language = self.get_language()
        return language.lgettext(message)

    def ngettext(self, msgid1, msgid2, n):
        language = self.get_language()
        return language.ngettext(msgid1, msgid2, n)

    def lngettext(self, msgid1, msgid2, n):
        language = self.get_language()
        return language.lngettext(msgid1, msgid2, n)

    def ugettext(self, message):
        language = self.get_language()
        return language.ugettext(message)

    def ungettext(self, msgid1, msgid2, n):
        language = self.get_language()
        return language.ungettext(msgid1, msgid2, n)
    
