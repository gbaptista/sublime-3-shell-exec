# Shell Exec

Run shell commands like git, rvm, rspec, ls, etc. with Bash, Zsh and others inside your Sublime Text 3.

![Demo: RSpec inside Sublime](https://raw.githubusercontent.com/gbaptista/sublime-3-shell-exec/master/demo.gif)

* [Command Palette](#command-palette)
* [Default Shortcuts](#default-shortcuts)
* [Settings](#settings)
* [Custom Shortcuts](#custom-shortcuts)
  - [Command Format Syntax](#command-format-syntax)
* [Common Problems](#common-problems)
  - [RVM Command, ~/.bashrc, ~/.bash_profile, ~/.zshrc...](#rvm-command-bashrc-bash_profile-zshrc)
  - [Debugging](#debugging)
* [Some Cool Demos](#some-cool-demos)
  - [Git](#git)
  - [RSpec](#rspec)
  - [Unix](#unix)

### Command Palette

Shell Exec: Open `shell_exec_open`

### Default Shortcuts
* Linux: _ctrl + shift + c_
* Mac: _shift + super + c_
* Windows: _ctrl + shift + c_

### Settings

`User/Preferences.sublime-settings`:
```javascript
// You can use this file to load RVM, ~/.bashrc, custom shell functions...
// "shell_exec_load_sh_file": "your-sh-file-to-load-before-commands.sh",

// Shell executable: "/bin/bash", "/bin/sh", "/usr/bin/zsh"...
"shell_exec_executable": "/bin/bash",

// Shell executable option: --login # Run as login load your ~/.bashrc or other user settings.
"shell_exec_executable_option": "--login", // ["-l"] ["--login"]

// The output of the command can be shown on the Panel or in a New File: "panel", "file" or "none".
"shell_exec_output": "file",

// Set the Output File Syntax. Default is Ruby, because Ruby looks nice. =)
"shell_exec_output_syntax": "Ruby",

// Enable or Disable the  word wrap at the Output File.
"shell_exec_output_word_wrap": true,

// Enable or Disable the Debug infos (for plugin developers).
"shell_exec_debug": false,

// Name of the Shell Exec command box.
"shell_exec_title": "Shell Exec",

// Defines where the command should be executed: false, "project_folder" or "file_folder".
// If "project_folder" is set, will execute: cd project_folder && your_commnad.
"shell_exec_context": "project_folder",
```

### Custom Shortcuts
`shell_exec_open`: Open Shell Exec box to input some command.

`shell_exec_run`: Runs a predefined command.

`User/Default (Linux).sublime-keymap`:
```javascript
{
  // (ctrl+shift+c+o) key binding
  "keys": ["ctrl+shift+c", "ctrl+shift+o"],

  // "shell_exec_open": Open Shell Exec box to input some command.
  // "shell_exec_run": Runs a predefined command.
  "command": "shell_exec_open",

  "args": {
    // Title of the Shell Exec box.
    "title": "Shell Exec",

    // Predefined command.
    "command": "git status",

    // Format the command with variables.
    "format": "git ${input}",

    // You can use this file to load RVM, ~/.bashrc, custom shell functions...
    // "load_sh_file": "your-sh-file-to-load-before-commands.sh",

    // Shell executable: "/bin/bash", "/bin/sh", "/usr/bin/zsh"...
    "executable": "/bin/bash",

    // Shell executable option: --login # Run as login load your ~/.bashrc or other user settings.
    "executable_option": "--login", // ["-l"] ["--login"]

    // The output of the command can be shown on the Panel or in a New File: "panel", "file".
    "output": "file",

    // Set the Output File Syntax. Default is Ruby, because Ruby looks nice. =)
    "output_syntax": "Ruby",

    // Enable or Disable the  word wrap at the Output File.
    "output_word_wrap": true,

    // Enable or Disable the Debug infos (for plugin developers).
    "debug": false,

    // Name of the Shell Exec command box.
    "title": "Shell Exec",

    // Defines where the command should be executed: false, "project_folder" or "file_folder".
    // If "project_folder" is set, will execute: cd project_folder && your_commnad.
    "context": "project_folder",
  }
}
```

#### Command Format Syntax
```javascript
// (ctrl+shift+c+f) key binding
"keys": ["ctrl+shift+c", "ctrl+shift+f"],

// "shell_exec_open": Open Shell Exec box to input some command.
// "shell_exec_run": Runs a predefined command.
"command": "shell_exec_exec",

"args": {
    // Format the command with variables.
    "format": "rspec '${file}:${row}'"
}
```
Available variables:
* `${input}`: _Input from Shell Exec box._
* `${region}`: _Selected text._
* `${row}`: _Selected row number or the cursor position at file._
* `${file_name}`: _ShellExec.py_
* `${file}`: _/home/user/.config/sublime-text-3/Packages/shell-exec/ShellExec.py_
* `${packages}`: _/home/user/.config/sublime-text-3/Packages_
* `${file_base_name}`: _ShellExec_
* `${platform}`: _Linux_
* `${file_extension}`: _py_
* `${file_path}`: _/home/user/.config/sublime-text-3/Packages/shell-exec_
* `${folder}`: _/home/user/.config/sublime-text-3/Packages/shell-exec_

### Common Problems

#### RVM Command, ~/.bashrc, ~/.bash_profile, ~/.zshrc...

You can load RVM and profile files with login mode:
```javascript
// Shell executable: "/bin/bash", "/bin/sh", "/usr/bin/zsh"...
"shell_exec_executable": "/bin/bash",

// Shell executable option: --login # Run as login load your ~/.bashrc or other user settings.
"shell_exec_executable_option": "--login", // ["-l"] ["--login"]
```

Or... You can load a custom sh file:
```javascript
"shell_exec_load_sh_file": "my-config-loader-file.sh"
```

`my-config-loader-file.sh`: Loading ~/.bashrc simulating interactive shell:
```shell
PS1=true # Simulate Interactive Shell
source ~/.bashrc
```

`my-config-loader-file.sh`: Loading RVM command:
```shell
export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"
```

#### Debugging
Just enable the debug to see panel outputs:
`User/Preferences.sublime-settings`:
```javascript
// Enable or Disable the Debug infos (for plugin developers).
"shell_exec_debug": true,
```

### Some Cool Demos
#### Git
```javascript
{
  "keys": ["ctrl+shift+g", "ctrl+shift+g"],
  "command": "shell_exec_open",
  "args": { "title": "Git Command:", "format": "git ${input}" }
},
{
  "keys": ["ctrl+shift+g", "ctrl+shift+c"],
  "command": "shell_exec_open",
  "args": {
    "title": "Git Checkout:",
    "format": "git checkout ${input}",
    "command": "'${file}'"
  }
},
{
  "keys": ["ctrl+shift+g", "ctrl+shift+s"],
  "command": "shell_exec_run",
  "args": { "command": "git status" }
},
{
  "keys": ["ctrl+shift+g", "ctrl+shift+d", "ctrl+shift+a"],
  "command": "shell_exec_run",
  "args": { "command": "git diff", "output_syntax": "Diff" }
},
{
  "keys": ["ctrl+shift+g", "ctrl+shift+d", "ctrl+shift+f"],
  "command": "shell_exec_run",
  "args": { "command": "git diff '${file}'", "output_syntax": "Diff" }
},
{
  "keys": ["ctrl+shift+g", "ctrl+shift+b"],
  "command": "shell_exec_run",
  "args": { "command": "git blame '${file}'", "output_syntax": "Git Blame" }
}
```

#### RSpec
```javascript
{
  "keys": ["ctrl+shift+r", "ctrl+shift+r"],
  "command": "shell_exec_open",
  "args": {
    "title": "RSpec Command:", "format": "rspec ${input} --require spec_helper"
  }
},
{
  "keys": ["ctrl+shift+r", "ctrl+shift+o"],
  "command": "shell_exec_open",
  "args": {
    "title": "RSpec Command:",
    "command": "'${file}:${row}'",
    "format": "rspec ${input} --require spec_helper"
  }
},
{
  "keys": ["ctrl+shift+r", "ctrl+shift+a"],
  "command": "shell_exec_run",
  "args": { "command": "rspec spec --require spec_helper" }
},
{
  "keys": ["ctrl+shift+r", "ctrl+shift+f"],
  "command": "shell_exec_run",
  "args": { "command": "rspec '${file}' --require spec_helper" }
},
{
  "keys": ["ctrl+shift+r", "ctrl+shift+l"],
  "command": "shell_exec_run",
  "args": { "command": "rspec '${file}:${row}' --require spec_helper" }
},
{
  "keys": ["ctrl+shift+r", "ctrl+shift+s"],
  "command": "shell_exec_run",
  "args": { "command": "rspec '${region}' --require spec_helper" }
}
```

#### Unix
```javascript
{
  "keys": ["ctrl+shift+u", "ctrl+shift+p"],
  "command": "shell_exec_open",
  "args": {
    "title": "Find Process",
    "format": "ps aux | grep ${input}"
  }
}
```
