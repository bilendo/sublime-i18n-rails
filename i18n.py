import sublime
import sublime_plugin

from .lib.cache_handler   import CacheHandler
from .lib.document_parser import DocumentParser
from .lib.logger          import Logger
from .lib.popup_builder   import PopupBuilder
from .lib.scope_handler   import ScopeHandler

class I18n(sublime_plugin.EventListener):
    project_dir = ''

    def on_hover(self, view, point, hover_zone):
        scope_handler = ScopeHandler(view, point, hover_zone)

        if not scope_handler.valid_scope():
            return

        # load cach on initial call
        self.manage_cache_state()

        # parse document and find translation key
        document_parser = DocumentParser(view, point, self.project_dir, scope_handler)
        key             = document_parser.find_key()

        if key is None:
            return

        # show popup
        popup_builder = PopupBuilder(view, point)

        try:
            translation_dict = self.lookup(key)
            popup_builder.render_translation(translation_dict)
        except Exception:
            popup_builder.render_warning(key)
            Logger.warn('Cannot find translation for key:', key)


    # def on_post_save_async(self, view):
        # TODO:
        # check if:
        #    - saved file is within locales_dir
        #    - saved file is a YAML file
        # reset cache


    def manage_cache_state(self):
        current_project_dir = sublime.active_window().folders()[0]

        if (self.project_dir == current_project_dir):
            return

        self.set_sublime_settings() # set locales_path, languages
        cache_handler    = CacheHandler(current_project_dir, self.locales_path)

        self.cache       = cache_handler.reset_cache()
        self.project_dir = current_project_dir


    def lookup(self, str_path):
        t = {}

        for lang in self.languages:
            path = [lang] + str_path.split('.')
            dic  = self.cache # reference

            for key in path:
                dic = dic[key]

            t[lang] = dic

        return t


    def set_sublime_settings(self):
        settings = sublime.load_settings('I18n Rails.sublime-settings')

        self.locales_path = settings.get('locales_path')
        self.languages    = settings.get('languages')
