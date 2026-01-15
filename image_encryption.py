import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.bg_color = "#f0f0f0"
        self.btn_color = "#4a90e2"
        self.text_color = "#333333"
        self.root.configure(bg=self.bg_color)
        self.create_widgets()
    def create_widgets(self):
        title_label = tk.Label(
            self.root, 
            text="Pixel Manipulation Image Encryption", 
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)
        key_frame = tk.Frame(self.root, bg=self.bg_color)
        key_frame.pack(pady=10)
        tk.Label(key_frame, text="Enter Key (0-255):", bg=self.bg_color, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(key_frame, font=("Arial", 12), width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "123")  
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=30)
        encrypt_btn = tk.Button(
            btn_frame, 
            text="Encrypt Image", 
            command=self.encrypt_image,
            font=("Arial", 12, "bold"),
            bg=self.btn_color,
            fg="white",
            width=15,
            height=2,
            relief=tk.FLAT
        )
        encrypt_btn.grid(row=0, column=0, padx=20)
        decrypt_btn = tk.Button(
            btn_frame, 
            text="Decrypt Image", 
            command=self.decrypt_image,
            font=("Arial", 12, "bold"),
            bg="#e24a4a",  
            fg="white",
            width=15,
            height=2,
            relief=tk.FLAT
        )
        decrypt_btn.grid(row=0, column=1, padx=20)
        self.status_label = tk.Label(
            self.root, 
            text="Ready", 
            bg=self.bg_color, 
            fg="#666666",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)
    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if 0 <= key <= 255:
                return key
            else:
                messagebox.showerror("Invalid Key", "Key must be between 0 and 255.")
                return None
        except ValueError:
            messagebox.showerror("Invalid Key", "Please enter a numeric key.")
            return None
    def process_image(self, mode):
        key = self.get_key()
        if key is None:
            return
        file_path = filedialog.askopenfilename(
            title=f"Select Image to {mode}",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not file_path:
            return
        try:
            image = Image.open(file_path)
            image_data = list(image.getdata())
            processed_data = []
            for pixel in image_data:
                new_pixel = []
                for i in range(len(pixel)):
                    if i < 3: 
                        new_pixel.append(pixel[i] ^ key)
                    else:     
                        new_pixel.append(pixel[i])
                processed_data.append(tuple(new_pixel))
            new_image = Image.new(image.mode, image.size)
            new_image.putdata(processed_data)
            dir_name = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            if mode == "Encrypt":
                output_path = os.path.join(dir_name, f"encrypted_{file_name}")
            else:
                output_path = os.path.join(dir_name, f"decrypted_{file_name}")
            new_image.save(output_path)
            self.status_label.config(text=f"Success: Saved as {os.path.basename(output_path)}")
            messagebox.showinfo("Success", f"Image {mode}ed successfully!\nSaved at: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    def encrypt_image(self):
        self.process_image("Encrypt")
    def decrypt_image(self):
        self.process_image("Decrypt")
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    root.mainloop()
