import rawpy
import os
import threading
import json
from PIL import Image, ImageTk
from tkinter import (
    Tk, Label, Button, filedialog, messagebox, Text, Scrollbar, END, StringVar,
    Frame, Toplevel, Canvas, simpledialog
)
from tkinter.ttk import Progressbar, Combobox
import platform
import queue
import time

# ----------- 初始化窗口 -----------
window = Tk()
window.title("[Anamorphic Lens Photo Restoration Tool] 变形镜头照片还原 - Produced By Michael Chen")
window.geometry("980x700")
window.resizable(False, False)

# ----------- 变量与文件 -----------
input_folder = ""
last_output_folder = ""
scale_data_file = "scales.txt"
cancel_event = threading.Event()
processing_thread = None

default_scales = ['1.25', '1.3', '1.33', '1.5', '1.6', '2.0']

supported_exts = [".arw", ".nef", ".rw2", ".jpg", ".jpeg", ".png"]

# ----------- 工具函数 -----------

def load_scale_options():
    if not os.path.exists(scale_data_file):
        return default_scales.copy()
    try:
        with open(scale_data_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
            if isinstance(saved, list):
                all_scales = sorted(set(default_scales + saved), key=lambda x: float(x))
                return all_scales
    except:
        pass
    return default_scales.copy()

def save_custom_scale(scale_value):
    try:
        if scale_value in default_scales:
            return
        custom_scales = []
        if os.path.exists(scale_data_file):
            with open(scale_data_file, 'r', encoding='utf-8') as f:
                custom_scales = json.load(f)
        if scale_value not in custom_scales:
            custom_scales.append(scale_value)
            with open(scale_data_file, 'w', encoding='utf-8') as f:
                json.dump(custom_scales, f)
    except Exception as e:
        log(f"⚠ 无法保存自定义倍率: {e}")

def detect_aspect_ratio(width, height):
    ratio = width / height
    if abs(ratio - 4/3) < 0.05:
        return "4:3"
    elif abs(ratio - 3/2) < 0.05:
        return "3:2"
    elif abs(ratio - 16/9) < 0.05:
        return "16:9"
    else:
        return "unknown"

def log(text):
    timestamp = time.strftime("[%H:%M:%S] ")
    log_frame.insert(END, timestamp + text + '\n')
    log_frame.see(END)
    window.update_idletasks()


def open_folder(path):
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            os.system(f'open "{path}"')
        elif system == "Linux":
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件夹：{e}")

def reset_buttons():
    btn_start.config(state="normal")
    btn_choose.config(state="normal")
    btn_open_input_folder.config(state="normal")
    btn_open_output_folder.config(state="normal")
    btn_cancel.config(state="disabled")

# ----------- 主界面布局 -----------

main_frame = Frame(window)
main_frame.pack(fill='both', expand=True)

left_frame = Frame(main_frame, width=620)
left_frame.pack(side='left', fill='y', padx=10, pady=10)

right_frame = Frame(main_frame, width=340)
right_frame.pack(side='right', fill='y', padx=10, pady=10)

# 支持格式显示
supported_formats_display = "、".join([ext[1:].upper() for ext in supported_exts])
label_supported = Label(left_frame, text=f"支持的图像格式：{supported_formats_display}", font=("Arial", 10, "bold"), fg="blue")
label_supported.pack(pady=(5, 2))

label_status = Label(left_frame, text="请选择包含图像的文件夹", wraplength=580)
label_status.pack(pady=10)

frame_selection = Frame(left_frame)
frame_selection.pack(pady=5)

# 变形倍率选择框 + 自定义按钮
Label(frame_selection, text="变形倍率:").pack(side="left", padx=(10, 5))
scale_var = StringVar()
combo_scale = Combobox(frame_selection, textvariable=scale_var, state="readonly", width=8)
scale_options = load_scale_options()
combo_scale['values'] = scale_options
default_index = scale_options.index('1.5') if '1.5' in scale_options else 0
combo_scale.current(default_index)
combo_scale.pack(side="left", padx=(0, 10))

def open_custom_scale_dialog():
    custom = simpledialog.askstring("添加自定义倍率", "请输入新的变形倍率（如 1.42）:")
    if custom:
        try:
            float_val = float(custom)
            if custom not in combo_scale['values']:
                save_custom_scale(custom)
                all_scales = load_scale_options()
                combo_scale['values'] = all_scales
            combo_scale.set(custom)
        except:
            messagebox.showerror("错误", "无效的倍率格式")

btn_custom_scale = Button(frame_selection, text="自定义", width=6, command=open_custom_scale_dialog)
btn_custom_scale.pack(side="left", padx=(0, 10))

# 输出格式选择
output_format_var = StringVar()
combo_format = Combobox(frame_selection, textvariable=output_format_var, state="readonly", width=10)
combo_format['values'] = ['PNG', 'JPEG', 'TIFF']
combo_format.current(0)
Label(frame_selection, text="输出格式:").pack(side="left", padx=(10, 5))
combo_format.pack(side="left")

# 日志框及滚动条
log_frame = Text(left_frame, height=15, width=75, wrap='word')
log_frame.pack(pady=(20, 10))
scrollbar = Scrollbar(left_frame, command=log_frame.yview)
scrollbar.place(in_=log_frame, relx=1.0, rely=0, relheight=1.0, anchor='ne')
log_frame.configure(yscrollcommand=scrollbar.set)

# 进度条
progress_bar = Progressbar(left_frame, length=580, mode='determinate')
progress_bar.pack(pady=10)

# ----------- 取消按钮 -----------

def cancel_processing():
    if processing_thread and processing_thread.is_alive():
        cancel_event.set()
        log("❗ 用户已请求取消处理，程序将尽快停止。")
        label_status.config(text="❗ 用户已请求取消处理，程序将尽快停止。")
        btn_cancel.config(state="disabled")



btn_cancel = Button(left_frame, text="取消处理", width=20, fg="red", command=cancel_processing, state="disabled")
btn_cancel.pack(pady=5)

# ----------- 左侧按钮 -----------

def choose_input_folder():
    global input_folder
    folder = filedialog.askdirectory()
    if folder:
        input_folder = folder
        label_status.config(text=f"已选择文件夹：{input_folder}")
        btn_open_input_folder.config(state="normal")

def open_input_folder():
    if input_folder:
        open_folder(input_folder)

def open_output_folder():
    global last_output_folder
    if last_output_folder and os.path.exists(last_output_folder):
        open_folder(last_output_folder)
    else:
        messagebox.showinfo("提示", "当前未处理任何图像，无法打开输出文件夹。")

btn_choose = Button(left_frame, text="选择输入文件夹", width=20, command=choose_input_folder)
btn_choose.pack(pady=5)

btn_open_input_folder = Button(left_frame, text="打开输入文件夹", width=20, state="disabled", command=open_input_folder)
btn_open_input_folder.pack(pady=5)

btn_start = Button(
    left_frame,
    text="开始处理图像",
    width=20,
    fg="red",
    font=("Arial", 11, "bold"),
    command=lambda: threading.Thread(target=process_images, daemon=True).start()
)
btn_start.pack(pady=10)

btn_open_output_folder = Button(left_frame, text="打开输出文件夹", width=20, state="disabled", command=open_output_folder)
btn_open_output_folder.pack(pady=5)

# 使用说明和版权
Label(left_frame, text="本软件免费提供使用，严禁商业分发", font=("Arial", 10), fg="gray").pack(pady=(10, 0))
Label(left_frame, text="软件版本 V1.1", font=("Arial", 10), fg="gray").pack()
Label(left_frame, text="© 2025 Michael Chen. All rights reserved.", font=("Arial", 10), fg="gray").pack()

# ----------- 镜头倍率选择弹窗 -----------

def ask_lens_scale(aspect_ratio):
    result = {"value": None}

    def on_custom():
        val = simpledialog.askstring("自定义倍率", "请输入自定义的镜头变形倍率（如 1.42）:")
        if val:
            try:
                f = float(val)
                combo.set(val)
            except:
                messagebox.showerror("错误", "无效的倍率格式")

    def on_confirm():
        sel = combo.get()
        if sel:
            result["value"] = sel
            dialog.destroy()
        else:
            messagebox.showwarning("提示", "请选择或输入有效倍率")

    dialog = Toplevel(window)
    dialog.title("选择镜头变形倍率")
    dialog.geometry("300x200")
    dialog.grab_set()

    Label(dialog, text=f"检测到图像比例为 {aspect_ratio}", font=("Arial", 11)).pack(pady=10)
    Label(dialog, text="请选择镜头变形倍率类型:", font=("Arial", 10)).pack()

    lens_options = ['1.25', '1.3', '1.33', '1.5', '1.6', '2.0']
    combo_var = StringVar()
    combo = Combobox(dialog, textvariable=combo_var, state="readonly", values=lens_options, width=10)
    combo.current(0)
    combo.pack(pady=5)

    btn_custom = Button(dialog, text="自定义倍率", command=on_custom)
    btn_custom.pack(pady=5)

    btn_confirm = Button(dialog, text="确认", command=on_confirm)
    btn_confirm.pack(pady=5)

    dialog.wait_window()
    return result["value"]

# ----------- 处理图像函数 -----------

def process_images():
    global last_output_folder, processing_thread

    cancel_event.clear()
    btn_cancel.config(state="normal")
    btn_start.config(state="disabled")
    btn_choose.config(state="disabled")
    btn_open_input_folder.config(state="disabled")
    btn_open_output_folder.config(state="disabled")
    progress_bar['value'] = 0
    label_status.config(text="正在处理图像...")
    log_frame.delete(1.0, END)
    log("作者：michaelchen2025@163.com")
    log("程序启动，开始处理图像...\n")

    if not input_folder:
        messagebox.showwarning("提示", "请先选择一个文件夹")
        reset_buttons()
        return

    # 快速扫描文件夹首张图像比例给用户建议
    preview_file = None
    for root, dirs, filenames in os.walk(input_folder):
        for f in filenames:
            if os.path.splitext(f)[1].lower() in supported_exts:
                preview_file = os.path.join(root, f)
                break
        if preview_file:
            break

    if preview_file:
        try:
            ext = os.path.splitext(preview_file)[1].lower()
            if ext in ['.arw', '.nef', '.rw2']:
                with rawpy.imread(preview_file) as raw:
                    rgb = raw.postprocess()
                img = Image.fromarray(rgb)
            else:
                img = Image.open(preview_file)
            aspect = detect_aspect_ratio(*img.size)

            chosen_scale = ask_lens_scale(aspect)
            if not chosen_scale:
                log("用户取消了倍率选择，处理已终止。")
                label_status.config(text="已取消：用户关闭倍率选择窗口")
                reset_buttons()
                return
            scale_var.set(chosen_scale)
            log(f"用户选择倍率: {chosen_scale} （图像比例 {aspect}）")
        except Exception as e:
            log(f"分辨率检测失败：{e}")

    try:
        horizontal_scale = float(scale_var.get())
    except Exception:
        messagebox.showwarning("提示", "请选择有效的变形倍率")
        reset_buttons()
        return

    log_queue = queue.Queue()

    def log_writer():
        while True:
            try:
                text = log_queue.get(timeout=0.1)
                log(text)
            except queue.Empty:
                if cancel_event.is_set() and log_queue.empty():
                    break

    def worker():
        global last_output_folder
        count = 0
        files = []
        for root, dirs, filenames in os.walk(input_folder):
            for f in filenames:
                if cancel_event.is_set():
                    log_queue.put(f"❗ 图像处理已取消，已处理 {count} 张图像。")
                    label_status.config(text=f"❗ 已取消，已处理 {count} 张图像")
                    btn_open_output_folder.config(state="normal" if count > 0 else "disabled")
                    reset_buttons()
                    return
                if os.path.splitext(f)[1].lower() in supported_exts:
                    files.append((root, f))

        total = len(files)
        if total == 0:
            log_queue.put("未找到支持的图像文件。")
            label_status.config(text="未找到支持的图像文件。")
            reset_buttons()
            return

        save_format = output_format_var.get().lower()
        ext_map = {"jpeg": ".jpg", "png": ".png", "tiff": ".tiff"}
        ext = ext_map.get(save_format, ".png")

        for i, (root, filename) in enumerate(files):
            if cancel_event.is_set():
                log_queue.put(f"图像处理已取消，已处理 {count} 张图像。")
                label_status.config(text=f"已取消，已处理 {count} 张图像")
                btn_open_output_folder.config(state="normal" if count > 0 else "disabled")
                reset_buttons()
                return
            try:
                input_path = os.path.join(root, filename)
                output_dir = os.path.join(root, "Output")
                os.makedirs(output_dir, exist_ok=True)

                output_name = os.path.splitext(filename)[0] + "_stretched" + ext
                output_path = os.path.join(output_dir, output_name)

                log_queue.put(f"[{i + 1}/{total}] 处理：{filename}")

                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in ['.arw', '.nef', '.rw2']:
                    with rawpy.imread(input_path) as raw:
                        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True)
                    img = Image.fromarray(rgb)
                else:
                    img = Image.open(input_path)

                width, height = img.size
                new_width = int(width * horizontal_scale)
                img_stretched = img.resize((new_width, height), Image.LANCZOS)

                if save_format == "jpeg":
                    img_stretched.save(output_path, format="JPEG", quality=95)
                elif save_format == "png":
                    img_stretched.save(output_path, format="PNG", compress_level=0)
                elif save_format == "tiff":
                    img_stretched.save(output_path, format="TIFF")
                else:
                    img_stretched.save(output_path, format="PNG", compress_level=0)

                count += 1
                last_output_folder = output_dir
                progress_bar['value'] = ((i + 1) / total) * 100
            except Exception as e:
                log_queue.put(f"处理失败：{filename}，错误信息：{e}")

        log_queue.put(f"\n成功处理 {count} 张图像。")
        label_status.config(text=f"处理完成：共 {count} 张图像")
        btn_open_output_folder.config(state="normal")
        reset_buttons()
        btn_cancel.config(state="disabled")

    threading.Thread(target=log_writer, daemon=True).start()
    processing_thread = threading.Thread(target=worker, daemon=True)
    processing_thread.start()


# ----------- 右侧打赏模块 -----------

donate_img_path = None
for ext in ["jpg", "png", "webp"]:
    candidate = f"donate.{ext}"
    if os.path.exists(candidate):
        donate_img_path = candidate
        break

if donate_img_path:
    qr_img_raw = Image.open(donate_img_path)
    max_width, max_height = 340, 580
    w, h = qr_img_raw.size
    scale = min(max_width / w, max_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    qr_img_small = qr_img_raw.resize(new_size, Image.Resampling.LANCZOS)
    qr_img = ImageTk.PhotoImage(qr_img_small)

    def show_large_preview():
        preview_win = Toplevel()
        preview_win.title("扫码支持作者")
        canvas = Canvas(preview_win, width=min(w, 900), height=min(h, 1200))
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = Scrollbar(preview_win, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)
        img_large = ImageTk.PhotoImage(qr_img_raw)
        canvas.create_image(0, 0, anchor='nw', image=img_large)
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.image = img_large

    qr_label = Label(right_frame, image=qr_img, cursor="hand2")
    qr_label.pack(pady=10)
    qr_label.bind("<Button-1>", lambda e: show_large_preview())
else:
    qr_label = Label(right_frame, text="(找不到收款码图片)", fg="red")
    qr_label.pack(pady=10)

Label(right_frame, text="感谢支持作者开发\nThanks for supporting the author\nEmail: michaelchen2025@163.com", justify="center", font=("Arial", 11)).pack(pady=10)
Label(right_frame, text="© 2025 Michael Chen. All rights reserved.", font=("Arial", 10), fg="gray").pack()

# ----------- 关闭事件，确保取消线程 -----------

def on_closing():
    if messagebox.askokcancel("退出", "确定要退出程序吗？"):
        cancel_processing()
        time.sleep(0.2)  # 等待线程响应
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# ----------- 启动主循环 -----------
window.mainloop()
