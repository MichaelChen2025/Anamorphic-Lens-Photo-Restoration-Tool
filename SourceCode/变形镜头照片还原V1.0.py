import rawpy
import os
import threading
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, filedialog, messagebox, Text, Scrollbar, END, StringVar, Frame, Toplevel, Canvas
from tkinter.ttk import Progressbar, Combobox
import platform

window = Tk()
window.title("[Anamorphic Lens Photo Restoration Tool] 变形镜头照片还原 - Produced By Michael Chen")
window.geometry("980x630")
window.resizable(False, False)

input_folder = ""
last_output_folder = ""

# 主布局
main_frame = Frame(window)
main_frame.pack(fill='both', expand=True)

left_frame = Frame(main_frame, width=620)
left_frame.pack(side='left', fill='y', padx=10, pady=10)

right_frame = Frame(main_frame, width=340)
right_frame.pack(side='right', fill='y', padx=10, pady=10)

label_status = Label(left_frame, text="请选择包含图像的文件夹（支持 ARW/NEF/RW2/JPG/PNG）", wraplength=580)
label_status.pack(pady=10)

frame_selection = Frame(left_frame)
frame_selection.pack(pady=5)

# 变形倍率下拉框
scale_var = StringVar()
combo_scale = Combobox(frame_selection, textvariable=scale_var, state="readonly", width=10)
combo_scale['values'] = ['1.33', '1.5', '1.55', '2.0']
combo_scale.current(1)
Label(frame_selection, text="变形倍率:").pack(side="left", padx=(10, 5))
combo_scale.pack(side="left", padx=(0, 20))

# 输出格式下拉框
output_format_var = StringVar()
combo_format = Combobox(frame_selection, textvariable=output_format_var, state="readonly", width=10)
combo_format['values'] = ['PNG', 'JPEG', 'TIFF']
combo_format.current(0)
Label(frame_selection, text="输出格式:").pack(side="left", padx=(10, 5))
combo_format.pack(side="left")

# 日志框
log_frame = Text(left_frame, height=15, width=75, wrap='word')
log_frame.pack(pady=(20, 10))
scrollbar = Scrollbar(left_frame, command=log_frame.yview)
scrollbar.place(in_=log_frame, relx=1.0, rely=0, relheight=1.0, anchor='ne')
log_frame.configure(yscrollcommand=scrollbar.set)

def log(text):
    log_frame.insert(END, text + '\n')
    log_frame.see(END)
    window.update_idletasks()

# 进度条
progress_bar = Progressbar(left_frame, length=580, mode='determinate')
progress_bar.pack(pady=10)

# 功能函数区域
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

def process_images():
    global last_output_folder
    if not input_folder:
        messagebox.showwarning("提示", "请先选择一个文件夹")
        return

    try:
        horizontal_scale = float(scale_var.get())
    except Exception:
        messagebox.showwarning("提示", "请选择有效的变形倍率")
        return

    btn_start.config(state="disabled")
    btn_choose.config(state="disabled")
    btn_open_input_folder.config(state="disabled")
    btn_open_output_folder.config(state="disabled")
    progress_bar['value'] = 0
    label_status.config(text="正在处理图像...")
    log_frame.delete(1.0, END)
    log("作者：michaelchen2025@163.com")
    log("程序启动，开始处理图像...\n")

    def task():
        global last_output_folder
        count = 0
        supported_exts = [".arw", ".nef", ".rw2", ".jpg", ".jpeg", ".png"]
        files = []
        for root, dirs, filenames in os.walk(input_folder):
            for f in filenames:
                if os.path.splitext(f)[1].lower() in supported_exts:
                    files.append((root, f))

        total = len(files)
        if total == 0:
            label_status.config(text="未找到支持的图像文件。")
            reset_buttons()
            return

        save_format = output_format_var.get().lower()
        ext_map = {"jpeg": ".jpg", "png": ".png", "tiff": ".tiff"}
        ext = ext_map.get(save_format, ".png")

        for i, (root, filename) in enumerate(files):
            try:
                input_path = os.path.join(root, filename)
                output_dir = os.path.join(root, "Output")
                os.makedirs(output_dir, exist_ok=True)

                output_name = os.path.splitext(filename)[0] + "_stretched" + ext
                output_path = os.path.join(output_dir, output_name)

                log(f"[{i + 1}/{total}] 处理：{filename}")

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
                log(f"❌ 处理失败：{filename}，错误信息：{e}")

        label_status.config(text=f"✅ 处理完成：共 {count} 张图像")
        log(f"\n✅ 成功处理 {count} 张图像。")
        btn_open_output_folder.config(state="normal")
        reset_buttons()

    threading.Thread(target=task).start()

def reset_buttons():
    btn_start.config(state="normal")
    btn_choose.config(state="normal")
    btn_open_input_folder.config(state="normal")

# 左侧按钮
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
    command=process_images
)

btn_start.pack(pady=10)

btn_open_output_folder = Button(left_frame, text="打开输出文件夹", width=20, state="disabled", command=open_output_folder)
btn_open_output_folder.pack(pady=5)

# 使用说明和版权
Label(left_frame, text="本软件免费提供使用，严禁商业分发", font=("Arial", 10), fg="gray").pack(pady=(10, 0))
Label(left_frame, text="软件版本 V1.0", font=("Arial", 10), fg="gray").pack()
Label(left_frame, text="© 2025 Michael Chen. All rights reserved.", font=("Arial", 10), fg="gray").pack()

# -------------------- 右侧打赏模块 --------------------
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
        preview_win.title("扫码支持作者 ❤️")
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

# 启动主循环
window.mainloop()
