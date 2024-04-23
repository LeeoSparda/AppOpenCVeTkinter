import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess

class ImageProcessorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processor")
        
        self.frame_left = tk.Frame(self.master)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.frame_right = tk.Frame(self.master)
        self.frame_right.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.image_label = tk.Label(self.frame_right)
        self.image_label.pack()
        
        self.image_label_original = tk.Label(self.frame_left)
        self.image_label_original.pack()
        
        self.operations_frame = tk.Frame(self.frame_right)
        self.operations_frame.pack()
        
        self.history_frame = tk.Frame(self.frame_right)
        self.history_frame.pack()
        self.history_label = tk.Label(self.history_frame, text="Operation History:")
        self.history_label.pack(side=tk.TOP)
        
        self.history_text = tk.Text(self.history_frame, height=10, width=50)
        self.history_text.pack(side=tk.LEFT)
        
        self.history_scrollbar = tk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=self.history_scrollbar.set)

        self.operations = {
            "Convert Color": self.convert_color,
            "Apply Filter": self.apply_filter,
            "Detect Edges": self.detect_edges,
            "Binarize": self.binarize,
            "Morphological Operations": self.morphological_operations
        }

        self.operation_variable = tk.StringVar()
        self.operation_variable.set("Select Operation")

        self.operation_dropdown = tk.OptionMenu(self.operations_frame, self.operation_variable, *self.operations.keys())
        self.operation_dropdown.grid(row=0, column=0)

        self.load_button = tk.Button(self.operations_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=1)

        self.apply_button = tk.Button(self.operations_frame, text="Apply", command=self.apply_operation)
        self.apply_button.grid(row=0, column=2)

        self.reset_button = tk.Button(self.operations_frame, text="Reset", command=self.reset_image)
        self.reset_button.grid(row=0, column=3)

        self.save_button = tk.Button(self.operations_frame, text="Save", command=self.save_image_with_history)
        self.save_button.grid(row=0, column=4)

        self.select_roi_button = tk.Button(self.operations_frame, text="Select ROI", command=self.select_roi)
        self.select_roi_button.grid(row=0, column=5)

        self.example_button = tk.Button(self.operations_frame, text="Detectar caracter", command=self.call_example_class)
        self.example_button.grid(row=0, column=6)

        # Botão para chamar a classe EncontrarVeiculo.py
        self.find_vehicle_button = tk.Button(self.operations_frame, text="Detection Car", command=self.call_find_vehicle_class)
        self.find_vehicle_button.grid(row=0, column=7)

        # Botão para chamar a classe EncontrarVeiculo.py
        self.find_vehicle_button = tk.Button(self.operations_frame, text="Encontrar Placa", command=self.call_find_vehicle_class)
        self.find_vehicle_button.grid(row=0, column=7)

        self.image = None
        self.cv_image = None
        self.original_image = None
        self.current_image_path = None
        self.operation_history = []

        self.history_text.bind("<Button-1>", self.reapply_operation)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image_path = file_path
            self.cv_image = cv2.imread(file_path)
            self.original_image = self.cv_image.copy()
            self.display_image()

    def display_image(self):
        if self.cv_image is not None:
            self.image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(self.image)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.image)
            self.image_label.image = self.image
            
            self.original_image_display = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.original_image_display = Image.fromarray(self.original_image_display)
            self.original_image_display = ImageTk.PhotoImage(self.original_image_display)
            self.image_label_original.config(image=self.original_image_display)
            self.image_label_original.image = self.original_image_display

    def apply_operation(self):
        operation = self.operation_variable.get()
        if operation != "Select Operation" and self.cv_image is not None:
            self.operations[operation]()
            self.operation_history.append(operation)
            self.update_history()

    def update_history(self):
        self.history_text.delete('1.0', tk.END)
        for operation in self.operation_history:
            self.history_text.insert(tk.END, operation + "\n")

    def reapply_operation(self, event):
        index = int(self.history_text.index(tk.CURRENT).split('.')[0]) - 1
        self.cv_image = self.original_image.copy()
        for i in range(index + 1):
            self.operations[self.operation_history[i]]()
        self.display_image()

    def reset_image(self):
        self.cv_image = self.original_image.copy()
        self.display_image()
        self.operation_history = []
        self.update_history()

    def convert_color(self):
        conversion_codes = {
            "BGR2GRAY": cv2.COLOR_BGR2GRAY,
            "BGR2RGB": cv2.COLOR_BGR2RGB
        }
        selected_conversion = "BGR2GRAY"
        self.cv_image = cv2.cvtColor(self.cv_image, conversion_codes[selected_conversion])
        self.display_image()

    def apply_filter(self):
        kernel = np.ones((5,5),np.float32)/25
        self.cv_image = cv2.filter2D(self.cv_image, -1, kernel)
        self.display_image()

    def detect_edges(self):
        self.cv_image = cv2.Canny(self.cv_image, 100, 200)
        self.display_image()

    def binarize(self):
        _, self.cv_image = cv2.threshold(self.cv_image, 100, 255, cv2.THRESH_BINARY)
        self.display_image()

    def morphological_operations(self):
        kernel = np.ones((5,5),np.uint8)
        self.cv_image = cv2.erode(self.cv_image, kernel, iterations=1)
        self.display_image()

    def select_roi(self):
        if self.cv_image is not None:
            roi = cv2.selectROI("Select ROI", self.cv_image)
            cv2.destroyWindow("Select ROI")
            if roi[2] > 0 and roi[3] > 0:
                x, y, w, h = roi
                roi_image = self.cv_image[y:y+h, x:x+w]
                save_folder = filedialog.askdirectory()
                if save_folder:
                    file_number = len([name for name in os.listdir(save_folder) if name.startswith("img")]) + 1
                    file_name = f"img{file_number}_roi.png"
                    save_path = os.path.join(save_folder, file_name)
                    cv2.imwrite(save_path, roi_image)
                    with open(os.path.join(save_folder, f"img{file_number}_roi_history.txt"), 'w') as f:
                        f.write("\n".join(self.operation_history))
                    messagebox.showinfo("ROI Selection", f"ROI selected and saved as {file_name} successfully.")
        else:
            messagebox.showwarning("ROI Selection", "No ROI selected.")

    def save_image_with_history(self):
        if self.cv_image is not None and len(self.operation_history) > 0:
            save_folder = filedialog.askdirectory()
            if save_folder:
                file_number = len([name for name in os.listdir(save_folder) if name.startswith("img")]) + 1
                file_name = f"img{file_number}_processed.jpg"
                save_path = os.path.join(save_folder, file_name)
                cv2.imwrite(save_path, cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR))
                with open(os.path.join(save_folder, f"img{file_number}_history.txt"), 'w') as f:
                    f.write("\n".join(self.operation_history))
                messagebox.showinfo("Save", f"Image and history saved as {file_name} successfully.")

    def call_example_class(self):
        subprocess.call(["python", "exemplo.py"])

    def call_find_vehicle_class(self):
        subprocess.call(["python", "DetectionCar.py"])

    def call_find_vehicle_class(self):
        subprocess.call(["python", "EncontrarPlaca.py"])

def main():
    root = tk.Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
