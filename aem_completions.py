import sublime
import sublime_plugin

from Sightly.sightly_completions import make_completion


class AemCompletions(sublime_plugin.EventListener):
    """docstring for AemCompletions"""

    def on_query_completions(self, view, prefix, locations):
        # Supported scopes for completions
        outside_expr = view.match_selector(locations[0], "text.html.sightly")
        inside_expr = view.match_selector(locations[0], "source.sightly.embedded.html")

        # Return early if we aren't in any supported scopes
        if not (outside_expr or inside_expr):
            return []

        return self.get_completions(view, prefix, locations, outside_expr, inside_expr)

    def get_completions(self, view, prefix, locations, outside_expr, inside_expr):
        if outside_expr:
            return [('hello outside!\tOutside', 'out!')]
        elif inside_expr:
            return [('hello inside!\tInside', 'in!')]