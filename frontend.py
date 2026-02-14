import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import backend


# -------------------------------------------------
# CustomTkinter global setup
# -------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SteganoApp(TkinterDnD.Tk):
    def __init__(self):
        # IMPORTANT: TkinterDnD must be the root
        TkinterDnD.Tk.__init__(self)

        # Window setup
        self.title("SteganoShield Ultimate")
        self.geometry("1000x750")

        # Fonts
        self.font_header = ctk.CTkFont(size=28, weight="bold")
        self.font_body = ctk.CTkFont(size=18)
        self.font_button = ctk.CTkFont(size=20, weight="bold")

        # Theme toggle
        self.switch_var = ctk.StringVar(value="on")
        self.switch_theme = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            command=self.toggle_theme,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            font=self.font_body
        )
        self.switch_theme.place(relx=0.95, rely=0.03, anchor="ne")

        # Title
        self.lbl_title = ctk.CTkLabel(
            self,
            text="SteganoShield: Multi-Media Security",
            font=self.font_header
        )
        self.lbl_title.pack(pady=(30, 20))

        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=40, pady=20, fill="both", expand=True)
        self.tabview._segmented_button.configure(font=self.font_button)

        self.tab_img_enc = self.tabview.add("    Image Encode    ")
        self.tab_img_dec = self.tabview.add("    Image Decode    ")
        self.tab_aud = self.tabview.add("    Audio Steganography    ")

        self.setup_image_encode()
        self.setup_image_decode()
        self.setup_audio_tab()

    # -------------------------------------------------
    # Theme
    # -------------------------------------------------

    def toggle_theme(self):
        if self.switch_var.get() == 'on':
            ctk.set_appearance_mode("Dark")
            self.configure(bg="Black")
        else:
            ctk.set_appearance_mode("light")
            self.configure(bg="white")
    
    # -------------------------------------------------
    # Drag & Drop handler
    # -------------------------------------------------
    def handle_drop(self, event, target):
        path = event.data.strip("{}").split()[0]

        if not os.path.isfile(path):
            return

        if target == "img_enc":
            self.file_path_enc = path
            self.lbl_file_enc.configure(text=path)

        elif target == "img_dec":
            self.file_path_dec = path
            self.lbl_file_dec.configure(text=path)

        elif target == "aud_enc":
            self.aud_path_enc = path
            self.lbl_aud_enc.configure(text=os.path.basename(path))

        elif target == "aud_dec":
            self.aud_path_dec = path
            self.lbl_aud_dec.configure(text=os.path.basename(path))

    # -------------------------------------------------
    # Image Encode
    # -------------------------------------------------
    def setup_image_encode(self):
        container = ctk.CTkFrame(self.tab_img_enc, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=50, pady=20)

        ctk.CTkButton(
            container,
            text="Step 1: Select Source Image",
            font=self.font_button,
            height=50,
            command=self.select_file_enc
        ).pack(fill="x", pady=20)

        self.lbl_file_enc = ctk.CTkLabel(
            container,
            text="Drop image here or click above",
            font=self.font_body,
            text_color="gray"
        )
        self.lbl_file_enc.pack()

        self.lbl_file_enc.drop_target_register(DND_FILES)
        self.lbl_file_enc.dnd_bind(
            "<<Drop>>", lambda e: self.handle_drop(e, "img_enc")
        )

        ctk.CTkLabel(
            container,
            text="Step 2: Enter Secret Message",
            font=self.font_body
        ).pack(pady=(30, 10), anchor="w")

        self.txt_msg_enc = ctk.CTkTextbox(container, font=self.font_body)
        self.txt_msg_enc.pack(fill="both", expand=True, pady=10)

        ctk.CTkButton(
            container,
            text="Step 3: ENCRYPT & HIDE",
            font=self.font_button,
            fg_color="green",
            height=60,
            command=self.run_img_encode
        ).pack(fill="x", pady=30)

    # -------------------------------------------------
    # Image Decode
    # -------------------------------------------------
    def setup_image_decode(self):
        container = ctk.CTkFrame(self.tab_img_dec, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=50, pady=20)

        ctk.CTkButton(
            container,
            text="Select Stego Image",
            font=self.font_button,
            height=50,
            command=self.select_file_dec
        ).pack(fill="x", pady=20)

        self.lbl_file_dec = ctk.CTkLabel(
            container,
            text="Drop stego image here",
            font=self.font_body,
            text_color="gray"
        )
        self.lbl_file_dec.pack()

        self.lbl_file_dec.drop_target_register(DND_FILES)
        self.lbl_file_dec.dnd_bind(
            "<<Drop>>", lambda e: self.handle_drop(e, "img_dec")
        )

        ctk.CTkButton(
            container,
            text="REVEAL MESSAGE",
            font=self.font_button,
            fg_color="orange",
            height=60,
            command=self.run_img_decode
        ).pack(fill="x", pady=30)

        ctk.CTkLabel(
            container,
            text="Hidden Message:",
            font=self.font_body,
            anchor="w"
        ).pack(fill="x")

        self.txt_res_dec = ctk.CTkTextbox(container, font=self.font_body)
        self.txt_res_dec.pack(fill="both", expand=True, pady=10)

    # -------------------------------------------------
    # Audio Tab
    # -------------------------------------------------
    def setup_audio_tab(self):
        self.tab_aud.columnconfigure((0, 1), weight=1)

        enc = ctk.CTkFrame(self.tab_aud)
        enc.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        dec = ctk.CTkFrame(self.tab_aud)
        dec.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Encode
        ctk.CTkLabel(enc, text="ENCODE AUDIO", font=self.font_header).pack(pady=30)

        ctk.CTkButton(
            enc,
            text="Select .WAV",
            font=self.font_button,
            height=40,
            command=self.select_audio_enc
        ).pack(fill="x", padx=30, pady=20)

        self.lbl_aud_enc = ctk.CTkLabel(enc, text="Drop WAV here", font=self.font_body)
        self.lbl_aud_enc.pack()

        self.lbl_aud_enc.drop_target_register(DND_FILES)
        self.lbl_aud_enc.dnd_bind(
            "<<Drop>>", lambda e: self.handle_drop(e, "aud_enc")
        )

        self.txt_aud_msg = ctk.CTkEntry(
            enc,
            placeholder_text="Secret Text",
            font=self.font_body,
            height=40
        )
        self.txt_aud_msg.pack(fill="x", padx=30, pady=30)

        ctk.CTkButton(
            enc,
            text="HIDE IN AUDIO",
            font=self.font_button,
            fg_color="green",
            height=50,
            command=self.run_aud_encode
        ).pack(fill="x", padx=30, pady=20)

        # Decode
        ctk.CTkLabel(dec, text="DECODE AUDIO", font=self.font_header).pack(pady=30)

        ctk.CTkButton(
            dec,
            text="Select .WAV",
            font=self.font_button,
            height=40,
            command=self.select_audio_dec
        ).pack(fill="x", padx=30, pady=20)

        self.lbl_aud_dec = ctk.CTkLabel(dec, text="Drop WAV here", font=self.font_body)
        self.lbl_aud_dec.pack()

        self.lbl_aud_dec.drop_target_register(DND_FILES)
        self.lbl_aud_dec.dnd_bind(
            "<<Drop>>", lambda e: self.handle_drop(e, "aud_dec")
        )

        self.lbl_aud_result = ctk.CTkLabel(
            dec,
            text="Hidden text will show here",
            font=self.font_body,
            wraplength=300
        )
        self.lbl_aud_result.pack(pady=20)

        ctk.CTkButton(
            dec,
            text="REVEAL AUDIO",
            font=self.font_button,
            fg_color="orange",
            height=50,
            command=self.run_aud_decode
        ).pack(fill="x", padx=30, pady=(10, 20))

    # -------------------------------------------------
    # Logic
    # -------------------------------------------------
    def select_file_enc(self):
        self.file_path_enc = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg")]
        )
        if self.file_path_enc:
            self.lbl_file_enc.configure(text=self.file_path_enc)

    def select_file_dec(self):
        self.file_path_dec = filedialog.askopenfilename(
            filetypes=[("Images", "*.png")]
        )
        if self.file_path_dec:
            self.lbl_file_dec.configure(text=self.file_path_dec)

    def run_img_encode(self):
        msg = self.txt_msg_enc.get("0.0", "end").strip()
        if hasattr(self, "file_path_enc") and msg:
            messagebox.showinfo(
                "Result",
                backend.encode_image(self.file_path_enc, msg)
            )

    def run_img_decode(self):
        if hasattr(self, "file_path_dec"):
            self.txt_res_dec.delete("0.0", "end")
            self.txt_res_dec.insert(
                "0.0", backend.decode_image(self.file_path_dec)
            )

    def select_audio_enc(self):
        self.aud_path_enc = filedialog.askopenfilename(
            filetypes=[("WAV Audio", "*.wav")]
        )
        if self.aud_path_enc:
            self.lbl_aud_enc.configure(text=os.path.basename(self.aud_path_enc))

    def select_audio_dec(self):
        self.aud_path_dec = filedialog.askopenfilename(
            filetypes=[("WAV Audio", "*.wav")]
        )
        if self.aud_path_dec:
            self.lbl_aud_dec.configure(text=os.path.basename(self.aud_path_dec))

    def run_aud_encode(self):
        msg = self.txt_aud_msg.get()
        if hasattr(self, "aud_path_enc") and msg:
            messagebox.showinfo(
                "Result",
                backend.encode_audio(self.aud_path_enc, msg)
            )

    def run_aud_decode(self):
        if hasattr(self, "aud_path_dec"):
            self.lbl_aud_result.configure(
                text=backend.decode_audio(self.aud_path_dec)
            )


if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()
