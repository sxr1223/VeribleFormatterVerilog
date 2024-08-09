# VeribleFormatterVerilog

**VeribleFormatterVerilog: A formatter for sublime using verible and some modify to easier use**

## Overview
It's a simple plugin for sublime which is a formatter for verilog using verible. To avoid format fail, it also auto comment and uncomment `` `include``.

## Features

Format verilog and SystemVerilog file through verible.

For some code like:

```verilog
reg [32-1:0] test[0:1024-1] ={`include "res.dat"};
```

Verible will show an error and refuse formatting. This plugin will auto comment out these code and uncomment them afer formatting.

You can specify verible setting form flag file or plugin setting. Flag file under project `project_flags_file_name` take precedence, then global flag file `global_flags_file_path`, the last one is plugin setting.

## Installation

Befor using this plugin, you have to install verible and add that to your `PATH`. Please make sure you can use `verible-verilog-format` directly in shell.

VeribleFormatterVerilog can be installed via Package Control in Sublime Text. Simply search for "VeribleFormatterVerilog" and then install this plugin. Alternatively, you can download the released file and place it in Sublime Text > Settings > Browse Packages > User.

## Usage

After installation, configure a keybinding to trigger the plugin:
1. Open `Preferences > Key Bindings` in Sublime Text.
2. Add keybinding for the following commands, I use `F11` here:

For formatting current file:
```json
 {
     "keys": ["f11"],
     "command": "format_with_verible"
 }
```

Then you can triger format by `F11` or `Edit->Line->Format with Verible`

## Contributing

Contributions to VeribleFormatterVerilog are welcome! If you have any suggestions, bug reports, or want to contribute code, please feel free to open an issue or submit a pull request.

## Support

For support, questions, or feature requests, please open an issue in this repository.
If you like, you can also contract me through 1173368667@qq.com.

## License

MPL-2.0
