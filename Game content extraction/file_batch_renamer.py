import os
import re
import json
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from datetime import datetime


class FileRenamerApp:
    """文件批量重命名工具 - 支持文档和图像重命名"""
    
    # 支持的图片格式
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
    # 配置文件路径 - 自动检测exe或源代码目录
    CONFIG_FILE = os.path.join(
        os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__),
        'config.json'
    )
    
    def __init__(self, root):
        """初始化应用程序"""
        self.root = root
        self.root.title("文件批量重命名工具")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # 加载配置
        self.config = self.load_config()
        
        # 工作目录变量（初始为程序所在目录）
        self.work_dir_var = tk.StringVar(value=self.config.get('work_dir', os.getcwd()))
        
        # ===== 在这里先初始化所有变量（防止 AttributeError）=====
        
        # Tab 1 - 文档命名 变量
        self.txt_start_number_var = tk.StringVar(value=self.config.get('txt_start_number', '33'))
        self.txt_prefix_var = tk.StringVar(value=self.config.get('txt_prefix', 'kkx3_'))
        self.txt_digits_var = tk.StringVar(value=self.config.get('txt_digits', '3'))
        
        # Tab 2 - 图像命名 变量
        self.img_start_number_var = tk.StringVar(value=self.config.get('img_start_number', '33'))
        self.img_prefix_var = tk.StringVar(value=self.config.get('img_prefix', 'kkx3_'))
        self.img_group_size_var = tk.StringVar(value=self.config.get('img_group_size', '4'))
        self.img_digits_var = tk.StringVar(value=self.config.get('img_digits', '3'))
        
        # =====================================================
        
        # 设置样式
        self.setup_styles()
        
        # 创建主界面
        self.create_main_ui()
        
        # 监听变量变化，自动保存配置
        self.setup_config_listeners()
        
        # 窗口关闭时保存配置
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        """从配置文件加载设置"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {e}")
        return {}
    
    def save_config(self):
        """保存配置到文件"""
        config = {
            'work_dir': self.work_dir_var.get(),
            'txt_start_number': self.txt_start_number_var.get(),
            'txt_prefix': self.txt_prefix_var.get(),
            'txt_digits': self.txt_digits_var.get(),
            'img_start_number': self.img_start_number_var.get(),
            'img_prefix': self.img_prefix_var.get(),
            'img_group_size': self.img_group_size_var.get(),
            'img_digits': self.img_digits_var.get(),
        }
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def setup_config_listeners(self):
        """为所有变量设置变化监听，实时保存配置"""
        self.work_dir_var.trace('w', lambda *args: self.save_config())
        self.txt_start_number_var.trace('w', lambda *args: self.save_config())
        self.txt_prefix_var.trace('w', lambda *args: self.save_config())
        self.txt_digits_var.trace('w', lambda *args: self.save_config())
        self.img_start_number_var.trace('w', lambda *args: self.save_config())
        self.img_prefix_var.trace('w', lambda *args: self.save_config())
        self.img_group_size_var.trace('w', lambda *args: self.save_config())
        self.img_digits_var.trace('w', lambda *args: self.save_config())
    
    def on_closing(self):
        """窗口关闭前保存配置"""
        self.save_config()
        self.root.destroy()
    
    def setup_styles(self):
        """设置 ttk 样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义颜色
        style.configure('Title.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Normal.TLabel', font=('Arial', 10))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def create_main_ui(self):
        """创建主界面"""
        # 顶部文件夹路径选择栏
        path_frame = ttk.LabelFrame(self.root, text="工作目录", padding=10)
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 路径输入框
        ttk.Label(path_frame, text="文件夹路径:", style='Normal.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.work_dir_var, width=60)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 浏览按钮
        ttk.Button(
            path_frame,
            text="浏览",
            command=self.browse_folder
        ).pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        ttk.Button(
            path_frame,
            text="刷新",
            command=self.refresh_path
        ).pack(side=tk.LEFT, padx=5)
        
        # 创建 Notebook（选项卡）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Tab 1: 文档命名
        self.tab1_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1_frame, text="文档命名 (Txt)")
        self.create_tab1_ui()
        
        # Tab 2: 图像命名
        self.tab2_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2_frame, text="图像命名 (Images)")
        self.create_tab2_ui()
        
        # 底部日志区域
        log_frame = ttk.LabelFrame(self.root, text="运行日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=100,
            height=12,
            font=('Courier New', 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 日志的标签配置（用于彩色输出）
        self.log_text.tag_config('success', foreground='green')
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('info', foreground='blue')
        self.log_text.tag_config('warning', foreground='orange')
        
        # 初始日志
        self.log(f"系统已就绪，当前工作目录: {self.work_dir_var.get()}", 'info')
        self.log("=" * 80, 'info')
    
    def create_tab1_ui(self):
        """创建 Tab 1: 文档命名 UI"""
        # 内容框架
        content_frame = ttk.Frame(self.tab1_frame, padding=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(
            content_frame,
            text="文档命名配置 (.txt 文件)",
            style='Title.TLabel'
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # 参数框架
        params_frame = ttk.LabelFrame(content_frame, text="参数设置", padding=15)
        params_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 起始编号
        ttk.Label(params_frame, text="起始编号:", style='Normal.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.txt_start_number_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 重命名前缀
        ttk.Label(params_frame, text="重命名前缀:", style='Normal.TLabel').grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.txt_prefix_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # 后缀编号位数
        ttk.Label(params_frame, text="后缀编号位数:", style='Normal.TLabel').grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.txt_digits_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # 说明信息
        info_text = "说明: 程序将扫描当前目录下的 .txt 文件，按文件名中括号内的数字自然排序后重命名。\n重命名格式: [前缀][编号].txt"
        ttk.Label(
            content_frame,
            text=info_text,
            style='Normal.TLabel',
            justify=tk.LEFT,
            foreground='gray'
        ).pack(fill=tk.X, pady=(0, 15))
        
        # 执行按钮
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="开始重命名文档",
            command=self.execute_txt_rename,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="清除日志",
            command=self.clear_log
        ).pack(side=tk.LEFT, padx=5)
    
    def create_tab2_ui(self):
        """创建 Tab 2: 图像命名 UI"""
        # 内容框架
        content_frame = ttk.Frame(self.tab2_frame, padding=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(
            content_frame,
            text="图像命名配置 (.png, .jpg, .jpeg, .webp, .bmp, .gif)",
            style='Title.TLabel'
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # 参数框架
        params_frame = ttk.LabelFrame(content_frame, text="参数设置", padding=15)
        params_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 起始编号
        ttk.Label(params_frame, text="起始编号:", style='Normal.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.img_start_number_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 重命名前缀
        ttk.Label(params_frame, text="重命名前缀:", style='Normal.TLabel').grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.img_prefix_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # 每组图像数量
        ttk.Label(params_frame, text="每组图像数量:", style='Normal.TLabel').grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.img_group_size_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # 后缀编号位数
        ttk.Label(params_frame, text="后缀编号位数:", style='Normal.TLabel').grid(row=3, column=0, sticky=tk.W, pady=8)
        ttk.Entry(params_frame, textvariable=self.img_digits_var, width=20).grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        # 说明信息
        info_text = "说明: 程序将扫描当前目录下的图像文件，按文件名中的数字自然排序后进行分组重命名。\n重命名格式: [前缀][组编号]_([组内序号]).[扩展名]\n当每组数量=1时，格式为: [前缀][编号].[扩展名]\n例如(每组4张): kkx3_033_(1).png, kkx3_033_(2).png, kkx3_033_(3).png, kkx3_033_(4).png, kkx3_034_(1).png\n例如(每组1张): kkx3_033.png, kkx3_034.png, kkx3_035.png"
        ttk.Label(
            content_frame,
            text=info_text,
            style='Normal.TLabel',
            justify=tk.LEFT,
            foreground='gray'
        ).pack(fill=tk.X, pady=(0, 15))
        
        # 执行按钮
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="开始重命名图像",
            command=self.execute_img_rename,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="清除日志",
            command=self.clear_log
        ).pack(side=tk.LEFT, padx=5)
    
    def log(self, message, tag='normal'):
        """向日志框添加消息"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        
        if tag == 'normal':
            self.log_text.insert(tk.END, log_message)
        else:
            self.log_text.insert(tk.END, log_message, tag)
        
        self.log_text.see(tk.END)  # 自动滚动到底部
        self.root.update()
    
    def clear_log(self):
        """清除日志"""
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清除", 'info')
    
    def browse_folder(self):
        """打开文件夹浏览对话框"""
        folder = filedialog.askdirectory(title="选择工作目录")
        if folder:
            self.work_dir_var.set(folder)
            self.log(f"已选择工作目录: {folder}", 'info')
    
    def refresh_path(self):
        """刷新路径显示"""
        path = self.work_dir_var.get()
        if os.path.isdir(path):
            self.log(f"路径有效，已刷新: {path}", 'info')
        else:
            self.log(f"错误: 路径不存在 - {path}", 'error')
    
    def natural_sort_key(self, filename):
        """
        从文件名中提取括号内的数字用于排序。
        例如: "1 (10).txt" -> 10
        """
        match = re.search(r'\((\d+)\)', filename)
        if match:
            return int(match.group(1))
        
        # 如果没有括号，尝试提取文件名中的任何数字
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(numbers[0])
        
        return -1
    
    def image_sort_key(self, filename):
        """
        从图像文件名中提取数字用于排序。
        例如: "image_10.png" -> 10
        """
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(numbers[0])
        return -1
    
    def validate_input(self, start_num_str, digits_str, group_size_str=None):
        """验证用户输入"""
        try:
            start_num = int(start_num_str)
            digits = int(digits_str)
            
            if start_num < 0:
                self.log("错误: 起始编号必须为非负整数", 'error')
                return False
            
            if digits < 1 or digits > 10:
                self.log("错误: 后缀编号位数必须在 1-10 之间", 'error')
                return False
            
            if group_size_str is not None:
                group_size = int(group_size_str)
                if group_size < 1:
                    self.log("错误: 每组图像数量必须大于 0", 'error')
                    return False
            
            return True
        except ValueError:
            self.log("错误: 请输入有效的整数", 'error')
            return False
    
    def execute_txt_rename(self):
        """执行文档重命名"""
        self.log("=" * 80, 'info')
        self.log("开始执行文档重命名任务...", 'info')
        
        # 获取工作目录并验证
        work_dir = self.work_dir_var.get().strip()
        if not os.path.isdir(work_dir):
            self.log(f"错误: 工作目录不存在 - {work_dir}", 'error')
            return
        
        # 验证输入
        if not self.validate_input(
            self.txt_start_number_var.get(),
            self.txt_digits_var.get()
        ):
            return
        
        # 获取参数
        start_num = int(self.txt_start_number_var.get())
        prefix = self.txt_prefix_var.get()
        digits = int(self.txt_digits_var.get())
        
        self.log(f"工作目录: {work_dir}", 'info')
        self.log(f"参数: 起始编号={start_num}, 前缀='{prefix}', 位数={digits}", 'info')
        
        # 获取所有 .txt 文件
        try:
            txt_files = [f for f in os.listdir(work_dir) 
                        if f.lower().endswith('.txt') and os.path.isfile(os.path.join(work_dir, f))]
            
            if not txt_files:
                self.log("⚠️  在指定目录中没有找到任何 .txt 文件", 'warning')
                return
            
            # 按自然排序
            txt_files.sort(key=self.natural_sort_key)
            self.log(f"找到 {len(txt_files)} 个 .txt 文件，开始按自然顺序重命名...", 'info')
            self.log("")
            
            success_count = 0
            skip_count = 0
            error_count = 0
            current_num = start_num
            
            # 执行重命名
            for idx, old_name in enumerate(txt_files, 1):
                try:
                    # 构建新文件名
                    format_str = f"{{:0{digits}d}}"
                    new_name = f"{prefix}{format_str.format(current_num)}.txt"
                    
                    old_path = os.path.join(work_dir, old_name)
                    new_path = os.path.join(work_dir, new_name)
                    
                    # 检查目标文件是否已存在
                    if os.path.exists(new_path) and old_path != new_path:
                        self.log(f"[{idx}] ⊘ 跳过 '{old_name}' -> '{new_name}' (目标文件已存在)", 'warning')
                        skip_count += 1
                    else:
                        os.rename(old_path, new_path)
                        self.log(f"[{idx}] ✓ '{old_name}' -> '{new_name}'", 'success')
                        success_count += 1
                    
                    current_num += 1
                
                except OSError as e:
                    self.log(f"[{idx}] ✗ 重命名 '{old_name}' 失败: {str(e)}", 'error')
                    error_count += 1
                    current_num += 1
            
            # 完成总结
            self.log("")
            self.log("=" * 80, 'info')
            summary = f"文档重命名完成! 成功: {success_count}, 跳过: {skip_count}, 失败: {error_count}"
            self.log(summary, 'info')
            self.log("=" * 80, 'info')
        
        except Exception as e:
            self.log(f"执行过程中发生错误: {str(e)}", 'error')
    
    def execute_img_rename(self):
        """执行图像重命名"""
        self.log("=" * 80, 'info')
        self.log("开始执行图像重命名任务...", 'info')
        
        # 获取工作目录并验证
        work_dir = self.work_dir_var.get().strip()
        if not os.path.isdir(work_dir):
            self.log(f"错误: 工作目录不存在 - {work_dir}", 'error')
            return
        
        # 验证输入
        if not self.validate_input(
            self.img_start_number_var.get(),
            self.img_digits_var.get(),
            self.img_group_size_var.get()
        ):
            return
        
        # 获取参数
        start_num = int(self.img_start_number_var.get())
        prefix = self.img_prefix_var.get()
        group_size = int(self.img_group_size_var.get())
        digits = int(self.img_digits_var.get())
        
        self.log(f"工作目录: {work_dir}", 'info')
        self.log(f"参数: 起始编号={start_num}, 前缀='{prefix}', 每组数量={group_size}, 位数={digits}", 'info')
        
        # 获取所有图像文件
        try:
            img_files = [f for f in os.listdir(work_dir)
                        if os.path.splitext(f)[1].lower() in self.IMAGE_EXTENSIONS
                        and os.path.isfile(os.path.join(work_dir, f))]
            
            if not img_files:
                self.log("⚠️  在指定目录中没有找到任何图像文件", 'warning')
                return
            
            # 按自然排序
            img_files.sort(key=self.image_sort_key)
            self.log(f"找到 {len(img_files)} 个图像文件，开始按自然顺序重命名...", 'info')
            self.log("")
            
            success_count = 0
            skip_count = 0
            error_count = 0
            
            # 执行重命名
            for idx, old_name in enumerate(img_files):
                try:
                    # 计算组编号和组内序号
                    group_num = start_num + (idx // group_size)
                    item_in_group = (idx % group_size) + 1
                    
                    # 获取文件扩展名
                    _, ext = os.path.splitext(old_name)
                    
                    # 构建新文件名
                    format_str = f"{{:0{digits}d}}"
                    # 当每组只有1张图像时，不显示组内序号
                    if group_size == 1:
                        new_name = f"{prefix}{format_str.format(group_num)}{ext}"
                    else:
                        new_name = f"{prefix}{format_str.format(group_num)}_({item_in_group}){ext}"
                    
                    old_path = os.path.join(work_dir, old_name)
                    new_path = os.path.join(work_dir, new_name)
                    
                    # 检查目标文件是否已存在
                    if os.path.exists(new_path) and old_path != new_path:
                        self.log(f"[{idx + 1}] ⊘ 跳过 '{old_name}' -> '{new_name}' (目标文件已存在)", 'warning')
                        skip_count += 1
                    else:
                        os.rename(old_path, new_path)
                        self.log(f"[{idx + 1}] ✓ '{old_name}' -> '{new_name}'", 'success')
                        success_count += 1
                
                except OSError as e:
                    self.log(f"[{idx + 1}] ✗ 重命名 '{old_name}' 失败: {str(e)}", 'error')
                    error_count += 1
            
            # 完成总结
            self.log("")
            self.log("=" * 80, 'info')
            summary = f"图像重命名完成! 成功: {success_count}, 跳过: {skip_count}, 失败: {error_count}"
            self.log(summary, 'info')
            self.log("=" * 80, 'info')
        
        except Exception as e:
            self.log(f"执行过程中发生错误: {str(e)}", 'error')


def main():
    """主函数"""
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
