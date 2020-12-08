import sublime
import yaml

class ScopeHandler:
    def __init__(self, view, point, hover_zone):
        self.current_scopes = view.scope_name(point)
        self.hover_zone     = hover_zone


    def valid_scope(self):
        valid_scopes   = ['text.html.ruby', 'source.ruby']

        if self.hover_zone == sublime.HOVER_TEXT:
            filtered_scopes = [scope for scope in valid_scopes if scope in self.current_scopes]

            if len(filtered_scopes) >= 1:
                return True

        False
