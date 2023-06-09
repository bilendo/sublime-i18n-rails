import sublime

class PopupBuilder:
    def __init__(self, view, point):
        self.view  = view
        self.point = point


    def render_translation(self, translation_dict):
        content = ''

        for language, translation_str in translation_dict.items():
            content += '<div style="margin: 0.2rem; padding-bottom: 0.2rem; border-bottom: 1px solid color(var(--foreground) alpha(0.25);">'
            content += '<span style="color: var(--greenish); padding-right: 0.5rem;">'
            content += '<strong>' + language.upper() + ':</strong>'
            content += '</span>'
            content += translation_str
            content += '</div>'

        self.render_popup(content)


    def render_warning(self, key):
        content  = '<div><strong style="color: var(--redish)">WARNING: Missing translation</strong></div>'
        content += '<div style="margin-top: 0.2rem;">' + key + '</div>'

        self.render_popup(content)


    def render_popup(self, content):
        html = '<html><body>' + content + '</body></html>'
        self.view.show_popup(
            html,
            flags      = sublime.HIDE_ON_MOUSE_MOVE_AWAY,
            location   = self.point,
            max_width  = 700,
            max_height = 400
        )
