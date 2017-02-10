import sublime
import sublime_plugin

def make_context_completion(context):
    contents = 'context=\'{0}\''.format(context)
    return make_completion(context, 'Display Context', contents)

def make_completion(trigger, label, contents):
    full_trigger = '{0}\t{1}'.format(trigger, label)
    return (full_trigger, contents)

class SightlyCompletions(sublime_plugin.EventListener):
    def __init__(self):
        self.option_list_scope = "meta.option-list.sightly"
        self.expression_scope = "meta.block.sightly"

    def on_query_completions(self, view, prefix, locations):
        # Only trigger within a Sightly embedded block
        if not view.match_selector(locations[0], "source.sightly.embedded.html"):
            return []

        in_options = view.match_selector(locations[0], self.option_list_scope)
        in_expression = view.match_selector(locations[0], self.expression_scope)

        return (self.display_context_completions(), sublime.INHIBIT_WORD_COMPLETIONS)

    def display_context_completions(self):
        contexts = [
            'html', 'text', 'elementName', 'attributeName', 'attribute', 'uri',
            'scriptToken', 'scriptString', 'scriptComment', 'scriptRegExp',
            'styleToken', 'styleString', 'styleComment', 'comment', 'number',
            'unsafe'
        ]

        return [make_context_completion(c) for c in contexts]

    def default_completions(self):
        # basic completions for built-in options ie. `context='$1'` or ``prependPath='$1'`
        pass