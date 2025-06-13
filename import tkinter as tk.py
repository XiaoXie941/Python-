import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading  # 添加线程支持
import shutil  # 添加在文件开头的导入部分

def select_py_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    py_entry.delete(0, tk.END)
    py_entry.insert(0, file_path)

def select_icon_file():
    file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
    icon_entry.delete(0, tk.END)
    icon_entry.insert(0, file_path)

def pack():
    py_file = py_entry.get()
    icon_file = icon_entry.get()
    onefile = var_onefile.get()
    noconsole = var_noconsole.get()

    if not py_file or not os.path.isfile(py_file):
        messagebox.showerror("错误", "请选择有效的 Python 文件！")
        return

    cmd = ["pyinstaller"]
    if onefile:
        cmd.append("--onefile")
    if noconsole:
        cmd.append("--noconsole")
    if icon_file and os.path.isfile(icon_file):
        cmd.append(f"--icon={icon_file}")
    cmd += ["--distpath", "ExE"]  # 添加这行修改输出目录
    cmd.append(py_file)

    # 禁用开始按钮防止重复点击
    pack_button.config(state=tk.DISABLED)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "正在打包，请稍候...\n")
    
    # 创建打包线程
    def run_pack():
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            
            # 动态获取脚本名称（新增代码）
            script_name = os.path.splitext(os.path.basename(py_file))[0]
            spec_file = f"{script_name}.spec"
            
            # 打包完成后自动清理（修改后的代码）
            if os.path.exists(spec_file):
                os.remove(spec_file)
            if os.path.exists("build"):
                shutil.rmtree("build")
            
            # 使用after方法更新UI
            root.after(0, lambda: result_text.insert(tk.END, proc.stdout))
            root.after(0, lambda: result_text.insert(tk.END, proc.stderr))
            if proc.returncode == 0:
                root.after(0, lambda: result_text.insert(tk.END, "\n打包完成！请查看 ExE 文件夹。"))
            else:
                root.after(0, lambda: result_text.insert(tk.END, "\n打包失败，请检查上方输出信息。"))
        except Exception as e:
            root.after(0, lambda: result_text.insert(tk.END, f"发生异常：{e}"))
        finally:
            # 重新启用开始按钮
            root.after(0, lambda: pack_button.config(state=tk.NORMAL))
    
    # 启动线程
    threading.Thread(target=run_pack, daemon=True).start()

root = tk.Tk()
root.title("Python 打包工具")
root.configure(bg='#191919')

# 先声明所有变量（必须放在界面元素创建之前）
var_onefile = tk.BooleanVar(value=True)
var_noconsole = tk.BooleanVar(value=True)

# 配置行列权重使内容居中
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(4, weight=1)  # 添加左右边距列
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(7, weight=1)     # 添加上下边距行

# 将主要内容放在中间列（第2列）
main_frame = tk.Frame(root, bg='#191919')
main_frame.grid(row=1, column=2, sticky="nsew")

# 重新排列所有组件到main_frame中
tk.Label(main_frame, text="选择启动的第一个 Python 文件:", 
        bg='#191919', fg='#188afb').grid(row=0, column=0, pady=5, sticky="e")
py_entry = tk.Entry(main_frame, width=40, bg='#333333', fg='#188afb')
py_entry.grid(row=0, column=1, padx=5)
tk.Button(main_frame, text="选择", command=select_py_file, 
        bg='#333333', fg='#188afb').grid(row=0, column=2)

# 图标选择组件（需要移到main_frame中）
tk.Label(main_frame, text="选择软件封面(记得把图片后缀改为ico):", 
        bg='#191919', fg='#188afb').grid(row=1, column=0, pady=5, sticky="e")
icon_entry = tk.Entry(main_frame, width=40, bg='#333333', fg='#188afb')
icon_entry.grid(row=1, column=1, padx=5)
tk.Button(main_frame, text="选择", command=select_icon_file, 
        bg='#333333', fg='#188afb').grid(row=1, column=2)

# 复选框和按钮也需要移到main_frame中...
tk.Checkbutton(main_frame, text="单文件（--onefile）(可以不用管)", 
              variable=var_onefile, bg='#191919', fg='#188afb',
              selectcolor='#333333', activebackground='#191919',
              activeforeground='#188afb').grid(row=2, column=1, sticky="w", pady=5)

tk.Checkbutton(main_frame, text="隐藏命令行窗口（--noconsole）(可以不用管)", 
              variable=var_noconsole, bg='#191919', fg='#188afb',
              selectcolor='#333333', activebackground='#191919',
              activeforeground='#188afb').grid(row=3, column=1, sticky="w", pady=5)

# 在main_frame中添加结果文本框（正确位置）
result_text = tk.Text(main_frame, height=15, width=60, 
                     bg='#333333', fg='#188afb')
result_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# 将开始打包按钮移到main_frame中（删除root中的重复定义）
pack_button = tk.Button(main_frame, text="开始打包", command=pack, 
                       bg="#363636", fg='#188afb')
pack_button.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()