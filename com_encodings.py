import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import face_recognition
import pickle
import os
import imghdr
from multiprocessing import Pool
import subprocess
import configparser

CONFIG_FILE_PATH = "Config_Encodings.ini"


def save_config(directory):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Directory': directory}
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)


def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        if 'DEFAULT' in config and 'Directory' in config['DEFAULT']:
            return config['DEFAULT']['Directory']
    print("Config file not found or directory not specified.")
    return ""


def encode_face(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        return encoding, os.path.basename(image_path)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def encode_faces(folder_path, progress_var, progress_label, progress_window):
    image_paths = [os.path.join(folder_path, image_file) for image_file in os.listdir(folder_path)
                   if imghdr.what(os.path.join(folder_path, image_file)) in ['jpeg', 'png', 'gif']]
    total_images = len(image_paths)
    progress_step = 100 / total_images

    progress_value = 0
    progress_var.set(progress_value)

    results = []
    known_face_encodings = []
    known_face_names = []

    # Check if face encodings are already present in the pickle file
    if os.path.exists("face_encodings.pickle"):
        with open("face_encodings.pickle", "rb") as f:
            try:
                existing_face_encodings, existing_face_names = pickle.load(f)
                known_face_encodings.extend(existing_face_encodings)
                known_face_names.extend(existing_face_names)
            except Exception as e:
                
                print(f"Error loading existing face encodings: {e}")

    with Pool() as pool:
        for image_path in image_paths:
            # Check if image has already been encoded
            if os.path.basename(image_path) in known_face_names:
                continue

            try:
                result = encode_face(image_path)
                if result is not None:
                    results.append(result)
                else:
                    print(f"Error encoding {image_path}")
            except Exception as e:
                print(f"Error encoding {image_path}: {e}")

            progress_value += progress_step
            progress_var.set(progress_value)
            progress_label.config(text=f"Encoding {len(results)} of {total_images} images")
            progress_window.update_idletasks()

    progress_label.config(text="Finished")
    progress_window.update_idletasks()
    progress_window.after(1500, progress_window.destroy)

    # Add newly encoded face encodings to the existing ones
    new_face_encodings = [res[0] for res in results if res]
    new_face_names = [res[1] for res in results if res]
    known_face_encodings.extend(new_face_encodings)
    known_face_names.extend(new_face_names)

    # Save all face encodings to the pickle file
    save_encodings(known_face_encodings, known_face_names)

    return known_face_encodings, known_face_names


def save_encodings(known_face_encodings, known_face_names):
    with open("face_encodings.pickle", "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)


def select_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        directory_label.config(text=folder_path)
        save_config(folder_path)  # Save selected directory to config file
        update_info_label(folder_path)  # Update info label


def run_encoding():
    folder_path = directory_label.cget("text")
    if folder_path:
        progress_window = tk.Toplevel(root)
        progress_window.title("Encoding Progress")
        progress_label = tk.Label(progress_window, text="Encoding images...", padx=10, pady=10)
        progress_label.pack()
        progress_bar = ttk.Progressbar(progress_window, mode='determinate')
        progress_bar.pack(pady=5, fill='x')
        progress_var = tk.DoubleVar()
        progress_bar.config(variable=progress_var)

        try:
            known_face_encodings, known_face_names = encode_faces(folder_path, progress_var, progress_label,
                                                                  progress_window)
            save_encodings(known_face_encodings, known_face_names)
            messagebox.showinfo("Success", "Encoding completed and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please select a directory before running encoding.")


def run_face_recognition():
    try:
        subprocess.Popen(["python", "com_facerecognition.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running face recognition: {e}")


def update_info_label(folder_path):
    if folder_path:
        image_paths = [file for file in os.listdir(folder_path)
                       if imghdr.what(os.path.join(folder_path, file)) in ['jpeg', 'png', 'gif']]
        num_images = len(image_paths)
        if num_images == 0:
            example_files_str = "No images found."
        else:
            example_files = ", ".join(image_paths[:5])  # List first 5 files as examples
            example_files_str = f"Example files: {example_files}"

        info_label.config(text=f"Number of images: {num_images}\n{example_files_str}")
    else:
        info_label.config(text="No directory selected.")


# GUI setup
root = tk.Tk()
root.title("Face Encoding and Recognition GUI")

# Calculate the position to center the window
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Label for "Directory"
directory_text_label = tk.Label(root, text="Directory:")
directory_text_label.pack(side="top", pady=10)

directory_label = tk.Label(root, text=load_config())
directory_label.pack(pady=5)

select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack(pady=5)

run_encoding_button = tk.Button(root, text="Run Encoding", command=run_encoding)
run_encoding_button.pack(pady=5)

run_face_rec_button = tk.Button(root, text="Run FaceRecognition", command=run_face_recognition)
run_face_rec_button.pack(pady=5)

# Label for showing information about images in the directory
info_label = tk.Label(root, text="")
info_label.pack(pady=10)

# Usage instructions (footer)
instructions_label = tk.Label(root, text="Instructions:\n1. Click 'Select Directory' to choose a folder containing images.\n2. Click 'Run Encoding' to encode faces in the selected directory.\n3. After encoding, click 'Run FaceRec' to start face recognition.")
instructions_label.pack(side="bottom", pady=10)

# Call update_info_label to update the info label when the application starts
update_info_label(load_config())

root.mainloop()
