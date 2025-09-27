import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

class BinaryFileViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("二进制文件查看器")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 设置图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        title_label = tk.Label(main_frame, text="二进制文件查看器", 
                              font=('Arial', 16, 'bold'), 
                              bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=(0, 10))
        
        # 文件选择区域
        file_frame = tk.Frame(main_frame, bg='#f0f0f0')
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("未选择文件")
        
        file_label = tk.Label(file_frame, text="文件路径:", 
                             font=('Arial', 10), bg='#f0f0f0')
        file_label.pack(side=tk.LEFT)
        
        self.file_path_label = tk.Label(file_frame, textvariable=self.file_path_var,
                                       font=('Arial', 10), bg='#f0f0f0', 
                                       fg='#666666', wraplength=500)
        self.file_path_label.pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=10)
        
        select_button = tk.Button(button_frame, text="选择文件", 
                                 command=self.select_file,
                                 font=('Arial', 10), 
                                 bg='#4CAF50', fg='white',
                                 padx=15, pady=5)
        select_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(button_frame, text="清空显示", 
                                command=self.clear_display,
                                font=('Arial', 10), 
                                bg='#f44336', fg='white',
                                padx=15, pady=5)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 显示选项
        options_frame = tk.Frame(main_frame, bg='#f0f0f0')
        options_frame.pack(fill=tk.X, pady=5)
        
        self.show_ascii_var = tk.BooleanVar(value=True)
        ascii_check = tk.Checkbutton(options_frame, text="显示ASCII字符",
                                    variable=self.show_ascii_var,
                                    command=self.update_display,
                                    font=('Arial', 9), bg='#f0f0f0')
        ascii_check.pack(side=tk.LEFT, padx=5)
        
        self.bytes_per_line_var = tk.IntVar(value=16)
        bytes_label = tk.Label(options_frame, text="每行字节数:",
                              font=('Arial', 9), bg='#f0f0f0')
        bytes_label.pack(side=tk.LEFT, padx=(20, 5))
        
        bytes_spinbox = tk.Spinbox(options_frame, from_=8, to=32, 
                                  increment=8, textvariable=self.bytes_per_line_var,
                                  command=self.update_display,
                                  width=5, font=('Arial', 9))
        bytes_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 二进制显示区域
        display_frame = tk.Frame(main_frame, bg='#f0f0f0')
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建带滚动条的文本框
        self.text_area = scrolledtext.ScrolledText(display_frame, 
                                                  wrap=tk.NONE,
                                                  font=('Courier New', 10),
                                                  bg='#2b2b2b', 
                                                  fg='#ffffff',
                                                  insertbackground='white')
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             relief=tk.SUNKEN, anchor=tk.W,
                             font=('Arial', 9), bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_file(self):
        """选择文件并显示二进制内容"""
        file_path = filedialog.askopenfilename(
            title="选择要查看的文件",
            filetypes=[("所有文件", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.display_binary_content(file_path)
    
    def display_binary_content(self, file_path):
        """显示文件的二进制内容"""
        try:
            file_size = os.path.getsize(file_path)
            
            if file_size > 10 * 1024 * 1024:  # 10MB限制
                if not messagebox.askyesno("文件过大", 
                                         f"文件大小: {file_size:,} 字节\n"
                                         f"文件较大，可能影响性能。\n"
                                         f"是否继续显示？"):
                    return
            
            self.status_var.set("正在读取文件...")
            self.root.update()
            
            with open(file_path, 'rb') as file:
                content = file.read()
            
            self.status_var.set("正在格式化显示...")
            self.root.update()
            
            self.format_binary_display(content)
            self.status_var.set(f"文件大小: {file_size:,} 字节")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时出错: {str(e)}")
            self.status_var.set("读取文件失败")
    
    def format_binary_display(self, content):
        """格式化二进制数据显示"""
        self.text_area.delete(1.0, tk.END)
        
        bytes_per_line = self.bytes_per_line_var.get()
        show_ascii = self.show_ascii_var.get()
        
        for i in range(0, len(content), bytes_per_line):
            chunk = content[i:i + bytes_per_line]
            
            # 地址偏移量
            offset = f"{i:08X}"
            
            # 十六进制显示
            hex_part = ' '.join(f"{b:02X}" for b in chunk)
            
            # ASCII显示
            ascii_part = ''
            if show_ascii:
                ascii_chars = ''.join(
                    chr(b) if 32 <= b <= 126 else '.' 
                    for b in chunk
                )
                ascii_part = f" | {ascii_chars}"
            
            # 填充对齐
            hex_part = hex_part.ljust(bytes_per_line * 3 - 1)
            
            line = f"{offset}:  {hex_part}{ascii_part}\n"
            self.text_area.insert(tk.END, line)
        
        self.text_area.see(1.0)  # 滚动到顶部
    
    def update_display(self):
        """更新显示格式"""
        if self.file_path_var.get() != "未选择文件":
            self.display_binary_content(self.file_path_var.get())
    
    def clear_display(self):
        """清空显示"""
        self.text_area.delete(1.0, tk.END)
        self.file_path_var.set("未选择文件")
        self.status_var.set("就绪")

def main():
    root = tk.Tk()
    app = BinaryFileViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()