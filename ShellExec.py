import sys, time, sublime, sublime_plugin, re
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

class ShellExecRun(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    self.args = args

    if ShellExec.get_setting('debug', self.args):
      print("\n\n>>>>>>>>>>>>>>>>>> Start Shell Exec Debug:")

    if not args.get("command"):
      args["command"] = ""

    ShellExec.run_shell_command(self.args, self.view, args.get("command"))

class ShellExecOpen(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    self.args = args

    if ShellExec.get_setting('debug', self.args):
      print("\n\n>>>>>>>>>>>>>>>>>> Start Shell Exec Debug:")

    command = ""

    if args.get("command"):
      command = ShellExec.command_variables(args, self.view, args["command"], False)

    def runShellExec(user_command):
      ShellExec.run_shell_command(self.args, self.view, user_command)

    sublime.active_window().show_input_panel(ShellExec.get_setting('title', self.args), command, runShellExec, None, None)

class ShellExecViewInsertCommand(sublime_plugin.TextCommand):
  def run(self, edit, pos, text):
    self.view.insert(edit, pos, text)

class ShellExec:
  def __init__(self):
    self.output_file = None
    self.panel_output = None

  def command_variables(args, view, command, format=True):
    if format and args.get("format"):
      command = args["format"].replace('${input}', command)

    for region in view.sel():
      (row,col) = view.rowcol(view.sel()[0].begin())

      command = command.replace('${row}', str(row+1))
      command = command.replace('${region}', view.substr(region))
      break

    # packages, platform, file, file_path, file_name, file_base_name,
    # file_extension, folder, project, project_path, project_name,
    # project_base_name, project_extension.
    command = sublime.expand_variables(command, sublime.active_window().extract_variables())

    return command

  def load_sh_file(source, path, args):
    if(path):
      try:
        with open(path, encoding='utf-8') as f:
          new_source = f.read()
          source += "\n" + new_source +  "\n"
          if ShellExec.get_setting('debug', args):
            print(path + ' loaded:')
            print('------------------------------------')
            print(new_source)
            print('------------------------------------')
      except:
        if ShellExec.get_setting('debug', args):
          print(path + ' error: ' + str(sys.exc_info()[0]))

    return source

  def run_shell_command(args, view, command):
    command = ShellExec.command_variables(args, view, command)
    if 'folder' in sublime.active_window().extract_variables():
      if sublime.platform() == 'windows':
        pure_command = command.replace(sublime.active_window().extract_variables()['folder'] + '\\', '')
      else:
        pure_command = command.replace(sublime.active_window().extract_variables()['folder'] + '/', '')
    else:
      pure_command = command

    if ShellExec.get_setting('context', args) == 'project_folder':
      if 'folder' in sublime.active_window().extract_variables():
        command = "cd '" + sublime.active_window().extract_variables()['folder'] + "' && " + command
    if ShellExec.get_setting('context', args) == 'file_folder':
      if 'file_path' in sublime.active_window().extract_variables():
        command = "cd '" + sublime.active_window().extract_variables()['file_path'] + "' && " + command

    sublime_shell_source = ''

    sh_file_settings = ShellExec.get_setting('load_sh_file', args, True)
    sh_file_shortcut = ShellExec.get_setting('load_sh_file', args, False)

    sublime_shell_source = ShellExec.load_sh_file(sublime_shell_source, sh_file_settings, args)

    if sh_file_settings != sh_file_shortcut:
      sublime_shell_source = ShellExec.load_sh_file(sublime_shell_source, sh_file_shortcut, args)

    if ShellExec.get_setting('debug', args):
        print('new Thread')

    t = Thread(target=ShellExec.execute_shell_command, args=(sublime_shell_source, command, pure_command, args))
    t.start()

  def new_output_file(args, pure_command):
    if ShellExec.get_setting('debug', args):
      print('open new empty file: ' + pure_command)
    output_file = sublime.active_window().new_file()
    output_file.set_name(pure_command[0:60])
    output_file.set_scratch(True)

    if ShellExec.get_setting('output_syntax', args):
      if ShellExec.get_setting('debug', args):
        print('set output syntax: ' + ShellExec.get_setting('output_syntax', args))

      if sublime.find_resources(ShellExec.get_setting('output_syntax', args) + '.tmLanguage'):
        output_file.set_syntax_file(sublime.find_resources(ShellExec.get_setting('output_syntax', args) + '.tmLanguage')[0])

    if ShellExec.get_setting('output_word_wrap', args):
      output_file.settings().set('word_wrap', True)
    else:
      output_file.settings().set('word_wrap', False)

    return output_file

  def increment_output(self, value, args, pure_command):
    if ShellExec.get_setting('output', args) == "file":
      if not self.output_file:
        self.output_file = ShellExec.new_output_file(args, pure_command)

      self.output_file.run_command('shell_exec_view_insert', {'pos': self.output_file.size(), 'text': value})
    elif ShellExec.get_setting('output', args) == "none":
      self.panel_output = False
    else:
      if not self.panel_output:
        self.panel_output = True
        sublime.active_window().run_command('show_panel', {"panel": "console", "toggle": False})
      sys.stdout.write(value)

  def execute_shell_command(sublime_shell_source, command, pure_command, args, return_error=True):
    code = sublime_shell_source + "\n" + command

    shell_command_do_gui_instance = ShellExec()

    if ShellExec.get_setting('debug', args):
      sublime.active_window().run_command('show_panel', {"panel": "console", "toggle": False})
      print("run command: " + command)

    ShellExec.increment_output(shell_command_do_gui_instance, "> " + pure_command + "\n\n", args, pure_command)

    if return_error:
      stderr = STDOUT
    else:
      stderr = None

    if ShellExec.get_setting('executable_option', args):
      if ShellExec.get_setting('debug', args):
        print('create Popen: executable=' + ShellExec.get_setting('executable', args) + ' ' + ShellExec.get_setting('executable_option', args))
      console_command = Popen([ShellExec.get_setting('executable', args), ShellExec.get_setting('executable_option', args), '-c', code], shell=False, stderr=stderr, stdout=PIPE)
    else:
      if ShellExec.get_setting('debug', args):
        print('create Popen: executable=' + ShellExec.get_setting('executable', args))
      console_command = Popen(code, executable=ShellExec.get_setting('executable', args), shell=True, stderr=stderr, stdout=PIPE)

    if ShellExec.get_setting('debug', args):
      print('waiting for stdout...')

    # TODO: This code is shameful, needs to be improved...
    initial_time = time.time()
    while True:
      diff_time = float(re.sub(r"e-*", '', str(time.time()-initial_time)))
      if diff_time > 0.01:
        char = str(console_command.stdout.read(1)) # last was slow
        initial_time = time.time()
      else:
        char = str(console_command.stdout.read(10)) # last was fast
        initial_time = time.time()

      if not char == "b''":
        if re.search(r"^b('|\")", char):
          char = re.sub(r"^b('|\")|('|\")$", '', char)

        char = bytes(char, "utf-8").decode("unicode_escape")
        ShellExec.increment_output(shell_command_do_gui_instance, char, args, pure_command)

      if console_command.poll() != None:
        if ShellExec.get_setting('debug', args):
          print('stdout complete!')

        output = str(console_command.stdout.read())
        output = re.sub(r"^b('|\")|('|\")$", '', output)
        output = bytes(output, "utf-8").decode("unicode_escape")
        output = re.sub(r"\n$", '', output)

        if ShellExec.get_setting('debug', args):
          print('send result to output file.')
        ShellExec.increment_output(shell_command_do_gui_instance, str(output) + "\n", args, pure_command)
        break

    if ShellExec.get_setting('debug', args):
      print(">>>>>>>>>>>>>>>>>> Shell Exec Debug Finished!")

    sublime.status_message('Shell Exec | Done! > ' + pure_command[0:60])

  def get_setting(config, args, force_default=False):
    if (not force_default) and args.get(config):
      return args[config]

    settings = sublime.load_settings('Preferences.sublime-settings')
    if settings.get('shell_exec_' + config):
      return settings.get('shell_exec_' + config)
    else:
      settings = sublime.load_settings('ShellExec.sublime-settings')
      return settings.get('shell_exec_' + config)
