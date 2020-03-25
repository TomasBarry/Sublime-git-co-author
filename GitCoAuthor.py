import sublime
import sublime_plugin

class GitCoAuthorCommand(sublime_plugin.ViewEventListener):
    def on_query_completions(self, prefix, locations):
        """on_query_completions

            Allow for auto-completion of the Git co-authorship message

            The domain_string and prompts are fetched from the .sublime-settings
            file which defines defaults if they are not overwritten

            The auto-completion is only provided when in the appropriate scope (
            a commit message)
        """
        matches = list(map(lambda x: self.view.match_selector(locations[0], x), self.relevant_scopes()))

        if True not in matches:
            return None

        domain_string = self.domain_string()
        prompts = self.prompts()

        template = "Co-authored-by: {name} <{email}@{domain_string}>".format(name='${1:name}', email='${2:email}', domain_string=domain_string)
        mapped_prompts = list(map(lambda x: [x, template], prompts))

        return mapped_prompts

    def settings(self):
        return sublime.load_settings('GitCoAuthor.sublime-settings')

    def prompts(self):
        return self.settings().get('prompts')

    def relevant_scopes(self):
        return self.settings().get('relevant_scopes')

    def domain_string(self):
        default_domain = self.settings().get('default_domain')
        if default_domain != '' and default_domain != None:
            return default_domain
        else:
            return '${3:domain}'
