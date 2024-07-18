from PIL import Image, ImageEnhance
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

# Default desired size
new_size = (1400, 800)

# Global variable for output folder
output_folder = r"C:\Users\Sayed\OneDrive\Desktop\Resize_pic\Resized"
os.makedirs(output_folder, exist_ok=True)

def resize_image(image_path):
    try:
        img = Image.open(image_path)
        
        print(f"\nOriginal size of {image_path}: {img.width}x{img.height}")
        
        if img.mode == 'P':
            img = img.convert('RGB')
        
        img_resized = img.resize(new_size, Image.LANCZOS)
        
        sharpness_enhancer = ImageEnhance.Sharpness(img_resized)
        img_resized = sharpness_enhancer.enhance(1.5)
        
        contrast_enhancer = ImageEnhance.Contrast(img_resized)
        img_resized = contrast_enhancer.enhance(1.2)
        
        brightness_enhancer = ImageEnhance.Brightness(img_resized)
        img_resized = brightness_enhancer.enhance(1.1)
        
        filename = os.path.basename(image_path)
        img_resized.save(os.path.join(output_folder, filename))
        
        print(f"Resized image saved as {os.path.join(output_folder, filename)}")
        
        return True
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False

def select_files(listbox):
    file_paths = filedialog.askopenfilenames(
        title="Select Images to Resize",
        filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*"))
    )
    if file_paths:
        for file_path in file_paths:
            listbox.insert(tk.END, file_path)

def remove_selected(listbox):
    selected_indices = listbox.curselection()
    for index in reversed(selected_indices):
        listbox.delete(index)

def process_images(listbox):
    file_paths = listbox.get(0, tk.END)
    if file_paths:
        for file_path in file_paths:
            success = resize_image(file_path)
            if not success:
                messagebox.showerror("Error", f"Failed to resize {file_path}")
        messagebox.showinfo("Completed", "All images have been resized.")
    else:
        messagebox.showwarning("Warning", "No images selected.")

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        print(f"Output folder set to: {output_folder}")

def create_gui():
    root = tk.Tk()
    root.title("Image Resizer")
    root.geometry("500x400")

    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    listbox = Listbox(frame, selectmode=tk.MULTIPLE)
    listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    add_button = tk.Button(button_frame, text="Add Images", command=lambda: select_files(listbox))
    add_button.pack(side=tk.LEFT, padx=5)

    remove_button = tk.Button(button_frame, text="Remove Selected", command=lambda: remove_selected(listbox))
    remove_button.pack(side=tk.LEFT, padx=5)

    process_button = tk.Button(button_frame, text="Process Images", command=lambda: process_images(listbox))
    process_button.pack(side=tk.RIGHT, padx=5)

    output_folder_button = tk.Button(button_frame, text="Select Output Folder", command=select_output_folder)
    output_folder_button.pack(side=tk.RIGHT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()






