import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Path to the images folder
image_folder = "images"

# Get list of image filenames in the folder (including .webp)
valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
all_images = [f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]

# List to keep track of disabled images
disabled_images = []

# Function to update enabled images based on disabled ones
def get_enabled_images():
    return [image for image in all_images if image not in disabled_images]

# Function to select a random image from enabled ones
def select_image():
    enabled_images = get_enabled_images()
    if not enabled_images:
        messagebox.showerror("No Images Left", "There are no enabled images to select from.")
        return
    selected_image = random.choice(enabled_images)
    display_image(selected_image)

# Function to display the selected image
def display_image(image_path):
    try:
        img = Image.open(os.path.join(image_folder, image_path))
        img = img.resize((300, 300))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the label with the selected image
        label.config(image=img_tk)
        label.image = img_tk
        messagebox.showinfo("Selected Image", f"The selected image is: {image_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

# Function to disable a specific image
def toggle_disable_image(image_name):
    if image_name in disabled_images:
        disabled_images.remove(image_name)
        status_label.config(text=f"{image_name} has been ENABLED.")
    else:
        disabled_images.append(image_name)
        status_label.config(text=f"{image_name} has been DISABLED.")
    update_disabled_images()

# Update the list of disabled images
def update_disabled_images():
    disabled_images_list.config(state="normal")  # Enable editing
    disabled_images_list.delete(1.0, "end")  # Clear current list
    disabled_images_list.insert("insert", "\n".join(disabled_images))  # Update list
    disabled_images_list.config(state="disabled")  # Disable editing

# Set up the GUI
root = tk.Tk()
root.title("Random Image Selector with Disable Feature")

# Create a label to display the image
label = tk.Label(root)
label.pack(pady=20)

# Button to pick a random image
button = tk.Button(root, text="Pick Random Image", command=select_image)
button.pack(pady=10)

# Dropdown menu to choose an image to disable or enable
image_to_disable = tk.StringVar()
image_to_disable.set(all_images[0])  # Default value if available

disable_menu = tk.OptionMenu(root, image_to_disable, *all_images)
disable_menu.pack(pady=10)

# Button to disable/enable the selected image
toggle_button = tk.Button(root, text="Disable/Enable Image", command=lambda: toggle_disable_image(image_to_disable.get()))
toggle_button.pack(pady=10)

# Label to show the status of the disabled/disabled image
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Textbox to show the list of disabled images
disabled_images_list = tk.Text(root, height=5, width=40, wrap="word", state="disabled")
disabled_images_list.pack(pady=10)

# Initial update of the disabled images list
update_disabled_images()

# Run the GUI
root.mainloop()
