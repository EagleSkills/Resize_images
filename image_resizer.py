from PIL import Image, ImageEnhance
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

# Global variables for default size
default_width, default_height = 1400, 800  # Default size

# Default enhancement factors
default_sharpness_factor = 1.5
default_contrast_factor = 1.2
default_brightness_factor = 1.1

# Global variables for current enhancement factors
sharpness_factor = default_sharpness_factor
contrast_factor = default_contrast_factor
brightness_factor = default_brightness_factor

# Global variable for output folder
output_folder = None

def resize_image(image_path, width, height):
    global output_folder
    try:
        img = Image.open(image_path)
        
        print(f"\nOriginal size of {image_path}: {img.width}x{img.height}")
        
        if img.mode == 'P':
            img = img.convert('RGB')
        
        # Apply enhancements
        img = enhance_image(img)
        
        img_resized = img.resize((width, height), Image.LANCZOS)
        
        filename = os.path.basename(image_path)

        # Set the output folder to be the "Resized" folder in the same location as the selected image
        image_folder = os.path.dirname(image_path)
        output_folder = os.path.join(image_folder, "Resized")
        os.makedirs(output_folder, exist_ok=True)

        img_resized.save(os.path.join(output_folder, filename))
        
        print(f"Resized image saved as {os.path.join(output_folder, filename)}")
        
        return True
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False

def enhance_image(img):
    # Enhance sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(sharpness_factor)
    
    # Enhance contrast
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast_factor)
    
    # Enhance brightness
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness_factor)
    
    return img

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

def process_images(listbox, width_entry, height_entry):
    file_paths = listbox.get(0, tk.END)
    if file_paths:
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid width and height values.")
            return
        
        for file_path in file_paths:
            success = resize_image(file_path, width, height)
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

def adjust_sharpness(new_factor_entry):
    global sharpness_factor
    try:
        sharpness_factor = float(new_factor_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for sharpness.")

def adjust_contrast(new_factor_entry):
    global contrast_factor
    try:
        contrast_factor = float(new_factor_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for contrast.")

def adjust_brightness(new_factor_entry):
    global brightness_factor
    try:
        brightness_factor = float(new_factor_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for brightness.")

def reset_values(width_entry, height_entry, sharpness_entry, contrast_entry, brightness_entry):
    global sharpness_factor, contrast_factor, brightness_factor
    width_entry.delete(0, tk.END)
    width_entry.insert(0, str(default_width))
    height_entry.delete(0, tk.END)
    height_entry.insert(0, str(default_height))
    sharpness_entry.delete(0, tk.END)
    sharpness_entry.insert(0, str(default_sharpness_factor))
    contrast_entry.delete(0, tk.END)
    contrast_entry.insert(0, str(default_contrast_factor))
    brightness_entry.delete(0, tk.END)
    brightness_entry.insert(0, str(default_brightness_factor))
    sharpness_factor = default_sharpness_factor
    contrast_factor = default_contrast_factor
    brightness_factor = default_brightness_factor

def close_application(root):
    root.destroy()

def toggle_minimize(root):
    current_state = root.attributes('-fullscreen')
    if current_state:
        root.attributes('-fullscreen', False)
    else:
        root.attributes('-fullscreen', True)

def create_gui():
    root = tk.Tk()
    root.title("Image Resizer")
    root.attributes('-fullscreen', True)  # Open in full screen mode

    # Frame for toggle and close buttons
    top_button_frame = tk.Frame(root)
    top_button_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

    # Minimize/Maximize toggle button
    toggle_button = tk.Button(top_button_frame, text="Min-Max", command=lambda: toggle_minimize(root))
    toggle_button.pack(side=tk.LEFT, padx=5)

    # Close button
    close_button = tk.Button(top_button_frame, text="Close", command=lambda: close_application(root))
    close_button.pack(side=tk.LEFT, padx=5)

    # Program name and creator label
    program_label = tk.Label(root, text='Image Resizer\nCreated by Hesham Abdalla\n for My son "Eyad"', font=("Arial", 12))
    program_label.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=(50, 10))  # Adjusted padding and anchor

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

    process_button = tk.Button(button_frame, text="Process Images", command=lambda: process_images(listbox, width_entry, height_entry))
    process_button.pack(side=tk.RIGHT, padx=5)

    output_folder_button = tk.Button(button_frame, text="Select Output Folder", command=select_output_folder)
    output_folder_button.pack(side=tk.RIGHT, padx=5)

    size_frame = tk.Frame(root)
    size_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(size_frame, text="Width:").pack(side=tk.LEFT, padx=5)
    width_entry = tk.Entry(size_frame, width=5)
    width_entry.pack(side=tk.LEFT, padx=5)
    width_entry.insert(0, str(default_width))

    tk.Label(size_frame, text="Height:").pack(side=tk.LEFT, padx=5)
    height_entry = tk.Entry(size_frame, width=5)
    height_entry.pack(side=tk.LEFT, padx=5)
    height_entry.insert(0, str(default_height))

    enhance_frame = tk.Frame(root)
    enhance_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(enhance_frame, text="Sharpness Factor:").pack(side=tk.LEFT, padx=5)
    sharpness_entry = tk.Entry(enhance_frame, width=5)
    sharpness_entry.pack(side=tk.LEFT, padx=5)
    sharpness_entry.insert(0, str(default_sharpness_factor))

    sharpness_button = tk.Button(enhance_frame, text="Set Sharpness", command=lambda: adjust_sharpness(sharpness_entry))
    sharpness_button.pack(side=tk.LEFT, padx=5)

    tk.Label(enhance_frame, text="Contrast Factor:").pack(side=tk.LEFT, padx=5)
    contrast_entry = tk.Entry(enhance_frame, width=5)
    contrast_entry.pack(side=tk.LEFT, padx=5)
    contrast_entry.insert(0, str(default_contrast_factor))

    contrast_button = tk.Button(enhance_frame, text="Set Contrast", command=lambda: adjust_contrast(contrast_entry))
    contrast_button.pack(side=tk.LEFT, padx=5)

    tk.Label(enhance_frame, text="Brightness Factor:").pack(side=tk.LEFT, padx=5)
    brightness_entry = tk.Entry(enhance_frame, width=5)
    brightness_entry.pack(side=tk.LEFT, padx=5)
    brightness_entry.insert(0, str(default_brightness_factor))

    brightness_button = tk.Button(enhance_frame, text="Set Brightness", command=lambda: adjust_brightness(brightness_entry))
    brightness_button.pack(side=tk.LEFT, padx=5)

    # Reset button
    reset_button = tk.Button(root, text="Reset to Default", command=lambda: reset_values(width_entry, height_entry, sharpness_entry, contrast_entry, brightness_entry))
    reset_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
