import sublime
import sublime_plugin

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

        in_options = view.match_selector(locations[0] - 1, self.option_list_scope)
        in_expression = view.match_selector(locations[0], self.expression_scope)
        return self.get_completions(view, prefix, locations, in_options)

    def get_completions(self, view, prefix, locations, in_options):
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))

        # print('prefix:', prefix)
        # print('location0:', locations[0])
        # print('substr:', view.substr(sublime.Region(locations[0], locations[0] + 3)), '!end!')
        # print('ch:', ch)

        if in_options:
            # TODO: check if we need to add a space after a `@` or a `,`
            return (self.default_options(), sublime.INHIBIT_WORD_COMPLETIONS)
        else:
            return []

    def default_options(self):
        # basic completions for built-in options ie. `context='$1'` or ``prependPath='$1'`
        default_completions = []
        default_completions.extend(self.display_context_completions())
        default_completions.extend(self.uri_manipulation_completions())
        return default_completions

    def display_context_completions(self):
        contexts = [
            'html', 'text', 'elementName', 'attributeName', 'attribute', 'uri',
            'scriptToken', 'scriptString', 'scriptComment', 'scriptRegExp',
            'styleToken', 'styleString', 'styleComment', 'comment', 'number',
            'unsafe'
        ]

        return [make_completion(c, 'Display Context', "context='{0}'".format(c)) for c in contexts]

    def uri_manipulation_completions(self):
        options = [
            'scheme', 'domain', 'path', 'prependPath', 'appendPath', 'selectors',
            'addSelectors', 'removeSelectors', 'extension', 'suffix', 'prependSuffix',
            'appendSuffix', 'query', 'addQuery', 'removeQuery', 'fragment'
        ]

        return [make_completion(o, 'URI Options', "{0}='$1'".format(o)) for o in options]