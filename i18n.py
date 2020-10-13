import sublime
import sublime_plugin
import os
import re
import yaml

class I18n(sublime_plugin.EventListener):
    sublime_settings = {}
    languages        = []
    project_dir      = ''

    # EVENT METHODS
    def on_hover(self, view, point, hover_zone):
        current_scopes = view.scope_name(point)

        if not (self.scope_valid(hover_zone, current_scopes)):
            return

        # init cache on first trigger
        self.manage_cache_state()

        # parse line
        line_region = view.line(point)
        text        = view.substr(line_region)
        pattern     = self.find_pattern(current_scopes)
        matches     = list(re.finditer(pattern, text))

        for match in re.finditer(pattern, text):
            key    = match.groupdict()['key']
            pos_l  = text.find(key) + line_region.begin()
            pos_r  = pos_l + len(key)
            region = sublime.Region(pos_l, pos_r)

            if region.contains(point):
                translation = self.get_translation(match.groupdict()['key'])
                self.log(translation)
                return

    # def on_post_save_async(self, view):
        # if file inside local path => reload cache
        # self.reset_cache()

    # CACHE METHODS
    def reset_cache(self):
        self.log('Cache reloading...')

        self.sublime_settings = sublime.load_settings('I18n Rails.sublime-settings')
        self.languages        = self.sublime_settings.get('languages')
        self.cache            = {}

        for subdir, dirs, files in os.walk(self.locales_dir()):
            for file in files:
                if file.lower().endswith('yml'):
                    file_name = os.path.join(subdir, file)

                    with open(file_name, encoding='utf-8') as stream:
                        locale = yaml.safe_load(stream)
                        self.add_to_cache(locale)

        self.log('Cache reloaded.')

    def add_to_cache(self, locale, base_dict = None, origin = []):
        if base_dict is None:
            base_dict = self.cache

        for key in locale:
            if key in base_dict:
                current_origin = origin + [key]

                if isinstance(base_dict[key], dict) and isinstance(locale[key], dict):
                    self.add_to_cache(locale[key], base_dict = base_dict[key], origin = current_origin)
                elif base_dict[key] == locale[key]:
                    continue
                else:
                    self.log('conflict:', '.'.join(current_origin))
            else:
                base_dict[key] = locale[key]

    def manage_cache_state(self):
        if (self.project_dir == sublime.active_window().folders()[0]):
            return

        self.project_dir = sublime.active_window().folders()[0]
        self.reset_cache()

    # TODO: support keys that start with .
    def get_translation(self, str_path):
        t = []

        for lang in self.languages:
            path = [lang] + str_path.split('.')
            sublime.active_window().folders()[0]

            dic  = self.cache # reference
            for key in path:
                dic = dic[key]
            t.append([lang, dic])

        return t

    def locales_dir(self):
        return os.path.join(self.project_dir, self.sublime_settings.get('locales_path'))

    # PATTERNS AND STR PROCESSING
    @staticmethod
    def find_pattern(current_scopes):
        if ('text.html.ruby' in current_scopes):
            return re.compile(r't\(["\']+(?P<key>[a-z._]+)["\']+\)')
        elif ('source.ruby' in current_scopes):
            return re.compile(r'I18n\.t\(("|\')(?P<key>[a-zA-Z\._]*)("|\')\)')

    # GENERAL METHODS
    @staticmethod
    def scope_valid(hover_zone, current_scopes):
        valid_scopes   = ['text.html.ruby', 'source.ruby']

        if (hover_zone == sublime.HOVER_TEXT) and (len([scope for scope in valid_scopes if scope in current_scopes]) >= 1):
            return True

        False

    @staticmethod
    def log(*args):
        print('[Rails I18n]', *args)
