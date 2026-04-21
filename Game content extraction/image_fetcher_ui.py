import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def select_folder1():
    """打开文件夹选择对话框，并自动填充到输入框1"""
    path = filedialog.askdirectory(title="选择文件夹1 (参考目录)")
    if path:
        entry_folder1.delete(0, tk.END)
        entry_folder1.insert(0, path)

def select_folder2():
    """打开文件夹选择对话框，并自动填充到输入框2"""
    path = filedialog.askdirectory(title="选择文件夹2 (目标抓取目录)")
    if path:
        entry_folder2.delete(0, tk.END)
        entry_folder2.insert(0, path)

def log_message(msg):
    """在文本框中输出日志，并自动滚动到底部"""
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)
    root.update()

def start_fetching():
    """执行抓取逻辑"""
    folder1_path = entry_folder1.get()
    folder2_path = entry_folder2.get()

    # 校验是否已选择路径
    if not folder1_path or not folder2_path:
        messagebox.showwarning("警告", "请先选择文件夹1和文件夹2的路径！")
        return

    # 清空之前的日志并禁用按钮防误触
    text_log.delete(1.0, tk.END)
    btn_run.config(state=tk.DISABLED)

    try:
        desktop_path = Path.home() / "Desktop"
        folder3_path = desktop_path / "图像抓取"
        folder3_path.mkdir(parents=True, exist_ok=True)

        log_message(f"准备抓取...\n文件将保存至: {folder3_path}\n" + "-"*30)

        # 获取并过滤文件夹1的文件
        files_in_folder1 = sorted(os.listdir(folder1_path))
        valid_files = [f for f in files_in_folder1 if not f.startswith('.')]
        
        # 提取奇数位置
        odd_files = valid_files[::2]

        log_message(f"文件夹1中共发现 {len(valid_files)} 个文件。")
        log_message(f"准备抓取 {len(odd_files)} 个奇数位置的文件...\n")

        success_count = 0
        not_found_count = 0

        # 遍历执行复制
        for filename in odd_files:
            source_file = Path(folder2_path) / filename
            destination_file = folder3_path / filename

            if source_file.exists() and source_file.is_file():
                shutil.copy2(source_file, destination_file)
                log_message(f"✅ 成功抓取: {filename}")
                success_count += 1
            else:
                log_message(f"❌ 未找到: {filename}")
                not_found_count += 1

        # 结束汇报
        log_message("-" * 30)
        log_message("抓取任务完成！")
        log_message(f"成功: {success_count} 张 | 未找到: {not_found_count} 张")
        messagebox.showinfo("任务完成", f"图像抓取完毕！\n成功: {success_count} 张\n失败: {not_found_count} 张\n\n已保存至桌面【图像抓取】文件夹。")

    except Exception as e:
        log_message(f"发生错误: {str(e)}")
        messagebox.showerror("运行错误", f"发生了一个错误:\n{str(e)}")
    
    finally:
        # 恢复按钮状态
        btn_run.config(state=tk.NORMAL)

# ================= UI 界面搭建 =================
root = tk.Tk()
root.title("图像奇数抓取工具")
root.geometry("550x450")
root.resizable(False, False) # 固定窗口大小

# --- 文件夹1 区域 ---
frame1 = tk.Frame(root)
frame1.pack(pady=10, padx=15, fill=tk.X)
tk.Label(frame1, text="文件夹1 (参考名单):").pack(side=tk.LEFT)
entry_folder1 = tk.Entry(frame1, width=40)
entry_folder1.pack(side=tk.LEFT, padx=10)
tk.Button(frame1, text="浏览...", command=select_folder1).pack(side=tk.LEFT)

# --- 文件夹2 区域 ---
frame2 = tk.Frame(root)
frame2.pack(pady=10, padx=15, fill=tk.X)
tk.Label(frame2, text="文件夹2 (目标图库):").pack(side=tk.LEFT)
entry_folder2 = tk.Entry(frame2, width=40)
entry_folder2.pack(side=tk.LEFT, padx=10)
tk.Button(frame2, text="浏览...", command=select_folder2).pack(side=tk.LEFT)

# --- 执行按钮 ---
btn_run = tk.Button(root, text="开始抓取", command=start_fetching, bg="#4CAF50", fg="black", font=("Arial", 12, "bold"), width=20)
btn_run.pack(pady=10)

# --- 日志输出区域 ---
tk.Label(root, text="运行日志:").pack(anchor=tk.W, padx=15)
text_log = tk.Text(root, height=13, width=70, bg="#f4f4f4")
text_log.pack(padx=15, pady=5)

# 启动窗口主循环
if __name__ == "__main__":
    root.mainloop()