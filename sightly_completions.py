import sublime
import sublime_plugin

from HTML.html_completions import make_completion as make_tag_completion

# NOTE: This completion engine borrows heavily from the built-in HTML completion engine
# which can be found at `Packages/HTML/html_completions.py`.


class SightlyCompletions(HTML.html_completions.HtmlTagCompletions):
    
    def on_query_completions(self, view, prefix, locations):
        # Return early unless we are in a Sightly file
        if not view.match_selector(locations[0], "text.html.sightly"):
            return []
        
        # TODO: Set of completions for `data-sly-...`
        #   Would be part of an html tag attribute
        # 
        # TODO: Set of completions for inside a scope of source.sightly.embedded, ie. for standard global objects 
        # 

        # pt = locations[0] - len(prefix) - 1
        # ch = view.substr(sublime.Region(pt, pt + 1))
        # print('prefix:', prefix)
        # print('location0:', locations[0])
        # print('substr:', view.substr(sublime.Region(locations[0], locations[0] + 3)), '!end!')
        # print('ch:', ch)
        # return [["hello\tHi!", "Why hello there!"]]
