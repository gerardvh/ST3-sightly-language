import sublime
import sublime_plugin

def make_completion(trigger, label, contents):
    full_trigger = '{0}\t{1}'.format(trigger, label)
    return (full_trigger, contents)

class SightlyCompletions(sublime_plugin.EventListener):
    def __init__(self):
        self.scopes = {
            'options': 'meta.option-list.sightly',
            'expression': 'meta.block.sightly',
            'data_block': 'text.html.sightly meta.tag - puctuation.definition.tag.end - puctuation.definition.tag.begin - string'
        }
        self.options_completions = self.get_default_options()
        self.block_completions = self.get_sly_block_completions()

    def on_query_completions(self, view, prefix, locations):
        # Return early if we aren't in any supported scopes
        if not self.in_supported_scope(view, locations[0]):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        # print('prefix:', prefix)
        # print('location0:', locations[0])
        # print('substr:', view.substr(sublime.Region(locations[0], locations[0] + 3)), '!end!')
        # print('ch:', ch)
        # print('scope:', view.scope_name(locations[0]))

        scope = None
        if view.match_selector(pt, self.scopes['options']):
            scope = 'options'
        elif view.match_selector(pt, self.scopes['data_block']):
            scope = 'data_block'
        return self.get_completions(view, prefix, locations, scope)

    def in_supported_scope(self, view, point):
        for scope in self.scopes.values():
            # If any of our scopes match the selector
            if view.match_selector(point, scope):
                return True
        # If none of our scopes match the selector
        return False

    # TODO: change `in_options` to an enum-like thing `context` that can be flexible later.
    def get_completions(self, view, prefix, locations, scope=None):
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        completions = None
        
        if scope == 'options':
            # TODO: check if we need to add a space after a `@` or a `,`
            completions = self.options_completions
        elif scope == 'data_block' and ch in [' ', '\t', '\n']:
            completions = self.block_completions
        
        if completions:
            return (completions, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        else:
            return []

    def get_default_options(self):
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

    def get_sly_block_completions(self):
        blocks_no_id = ['text', 'element', 'include', 'resource', 'call', 'unwrap']
        blocks_with_id = ['use', 'attribute', 'test', 'list', 'repeat', 'template']

        contents_no_id = 'data-sly-{0}="\${{$1\}}"'
        contents_id = 'data-sly-{0}.${{1:name}}="\${{$2\}}"'
        # Trigger looks like `slytext` or `slyresource` etc.
        completions = [
            make_completion('sly{}'.format(b), 'HTL Block Attr', 
                contents_no_id.format(b)) for b in blocks_no_id
        ]
        completions.extend([
            make_completion('sly{}'.format(b), 'HTL Block Attr', 
                contents_id.format(b)) for b in blocks_with_id
        ])
        return completions