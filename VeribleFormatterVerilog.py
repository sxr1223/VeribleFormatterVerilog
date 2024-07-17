import sublime
import sublime_plugin
import subprocess
import threading
import time

import sys
import os #temp file removal
import shlex #shell arg escaping
import tempfile
from functools import singledispatch

SETTINGS_FILE = "VeribleFormatterVerilog.sublime-settings"

class FormatWithVeribleCommand(sublime_plugin.TextCommand):
 
    def run(self, edit):
        view = self.view
        # 获取当前文件路径
        file_path = view.file_name()
        view.run_command("save")

        self.add_comment(view, edit)

        settings = sublime.load_settings(SETTINGS_FILE)
        # print(sys.version)
        # print(dir(settings))
        if file_path:
            # 调用 Verible 格式化 Verilog 代码
            flags_file_path = settings.get("flags_file_path","")
            print(flags_file_path)
            if(flags_file_path!=""):
                if(flags_file_path == "example"):
                    flags_file_path = os.path.join(sublime.packages_path(), 'VeribleFormatterVerilog/flags.txt')
                command = ["verible-verilog-format ", "--flagfile", flags_file_path]
            else:
                command = ["verible-verilog-format"]
                command.append("--indentation_spaces="+str(settings.get("tab_size",2)))
                command.append("--column_limit="+str(settings.get("column_limit ",100)))
                command.append("--line_break_penalty="+str(settings.get("line_break_penalty",2)))
                command.append("--over_column_limit_penalty="+str(settings.get("over_column_limit_penalty ",100)))
                command.append("--wrap_spaces="+str(settings.get("line_break_penalty",4)))

                command.append("--assignment_statement_alignment="+str(settings.get("assignment_statement_alignment","flush-left")))
                command.append("--case_items_alignment="+str(settings.get("case_items_alignment","flush-left")))
                command.append("--class_member_variable_alignment="+str(settings.get("class_member_variable_alignment","flush-left")))
                command.append("--compact_indexing_and_selections="+str(settings.get("compact_indexing_and_selections",True)).lower())
                command.append("--distribution_items_alignment="+str(settings.get("distribution_items_alignment","flush-left")))
                command.append("--enum_assignment_statement_alignment="+str(settings.get("enum_assignment_statement_alignment","flush-left")))
                command.append("--expand_coverpoints="+str(settings.get("expand_coverpoints",False)).lower())
                command.append("--formal_parameters_alignment="+str(settings.get("formal_parameters_alignment","flush-left")))
                command.append("--formal_parameters_indentation="+str(settings.get("formal_parameters_indentation","wrap")))
                command.append("--module_net_variable_alignment="+str(settings.get("module_net_variable_alignment","flush-left")))
                command.append("--named_parameter_alignment="+str(settings.get("named_parameter_alignment","flush-left")))
                command.append("--named_parameter_indentation="+str(settings.get("named_parameter_indentation","wrap")))
                command.append("--named_port_alignment="+str(settings.get("named_port_alignment","flush-left")))
                command.append("--named_port_indentation="+str(settings.get("named_port_indentation","wrap")))
                command.append("--port_declarations_alignment="+str(settings.get("port_declarations_alignment","flush-left")))
                command.append("--port_declarations_indentation="+str(settings.get("port_declarations_indentation","wrap")))
                command.append("--port_declarations_right_align_packed_dimensions="+str(settings.get("port_declarations_right_align_packed_dimensions",False)).lower())
                command.append("--port_declarations_right_align_unpacked_dimensions="+str(settings.get("port_declarations_right_align_unpacked_dimensions",False)).lower())
                command.append("--struct_union_members_alignment="+str(settings.get("struct_union_members_alignment","flush-left")))
                command.append("--try_wrap_long_lines="+str(settings.get("try_wrap_long_lines",False)).lower())     
                command.append("--wrap_end_else_clauses="+str(settings.get("wrap_end_else_clauses",True)).lower())
            

            command.append(file_path)

            print(command)
            try:
                # 执行命令
                cmd_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                cmd_output = cmd_process.communicate()
                # print(cmd_output)
                if(cmd_output[1]==""):
                    self.remove_comment(view, edit, cmd_output[0])
                    sublime.message_dialog("Verilog 代码格式化成功")
                else:
                    error_message = cmd_output[1].replace(file_path+":","")[1:]
                    sublime.message_dialog("Verilog 代码格式化失败，存在语法错误：\n{}".format(error_message))
            except subprocess.CalledProcessError as e:
                sublime.error_message("Verilog 代码格式化失败：{}".format(e))
        else:
            sublime.error_message("无法获取当前文件路径")

    def add_comment(self, view, edit):
        region_all = sublime.Region(0, view.size())
        file_text = view.substr(region_all)
        lines=file_text.split('\n')

        processed_text = ""
        for i in lines:
            if(i.find(r'`include')!=-1):
                print(i)
                i="//"+i.lstrip()
            processed_text+=i+'\n'
        processed_text=processed_text[:-1]
        view.replace(edit,region_all,processed_text)
        view.run_command("save")

    def remove_comment(self, view, edit, str_formatted):
        region_all = sublime.Region(0, view.size())
        file_text = str_formatted
        lines=file_text.split('\n')

        processed_text = ""
        for i in lines:
            if(i.find(r"`include")!=-1 and i.find("//")!=-1):
                print(i)
                i=i.replace("//","")
            processed_text+=i+"\n"
        processed_text=processed_text[:-1]
        view.replace(edit,region_all,processed_text)
