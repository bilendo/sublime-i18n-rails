import sublime
import re

from .logger import Logger

class DocumentParser:
    def __init__(self, view, point, project_dir, scope_handler):
        self.view        = view
        self.point       = point
        self.project_dir = project_dir
        self.scopes      = scope_handler.current_scopes


    def find_key(self):
        line_region = self.view.line(self.point)
        text        = self.view.substr(line_region)
        pattern     = self.find_pattern()
        raw_keys    = re.findall(pattern, text)

        for raw_key in raw_keys:
            pos_l  = text.find(raw_key) + line_region.begin()
            pos_r  = pos_l + len(raw_key)
            region = sublime.Region(pos_l, pos_r)

            if region.contains(self.point):
                parsed_key = self.parse_key(raw_key)
                return parsed_key


    def parse_key(self, raw_key):
        # absolute paths
        if not raw_key.startswith('.'):
            return raw_key

        # relative paths: lazy lookups
        path     = self.view.file_name()
        path_arr = path.replace(self.project_dir, '') \
                       .replace('/_', '/') \
                       .split('.')[0] \
                       .split('/')[3:]

        return '.'.join(path_arr) + raw_key


    def find_pattern(self):
        if any(scope in self.scopes for scope in ['text.html.rails', 'source.js.rails']):
            return re.compile(r't\([\"\']+(?P<key>[a-zA-Z\._]+)[\"\']?.+[\)\,\r\n\r\n]')
        elif ('source.ruby' in self.scopes):
            return re.compile(r'I18n\.t\([\"\']+(?P<key>[a-zA-Z\._]+)[\"\']?.+[\)\,\r\n\r\n]')
