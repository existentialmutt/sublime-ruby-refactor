import sublime, sublime_plugin, re

class RubyExtractLocalVariablePromptCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # get the name of the variable
    self.view.window().show_input_panel("Extract to Local Variable:", "", self.continue_with_extract, None, None)

  def continue_with_extract(self, var_name):
    self.view.run_command("ruby_extract_local_variable", {"var_name": var_name})

class RubyExtractLocalVariableCommand(sublime_plugin.TextCommand):
  def run(self, edit, var_name = "var"):
    view = self.view
    for region in view.sel():
      if not region.empty():
        var_value = view.substr(region)

        # replace the selection with a reference to the variable
        view.replace(edit, region, var_name)

        # insert our variable definition line above the current one
        line = view.line(region)
        indentation = re.search("^\s*", view.substr(line)).group()
        line_to_insert = indentation + var_name + " = " + var_value + "\n"
        view.insert(edit, line.begin(), line_to_insert)
    self.view.window().run_command('reindent')