import tkinter as tk
from tkinter import filedialog
from processing import process_file

def select_file():
    file_path = filedialog.askopenfilename(
        title="Pasirink Excel failą",
        filetypes=[("Excel files", "*.xlsx")]
    )
    
    if file_path:
        print("Pasirinktas failas:", file_path)
        process_file(file_path)

def main():
    root = tk.Tk()
    root.title("Wire-set")

    root.geometry("300x150")

    btn = tk.Button(root, text="Pasirink Excel failą", command=select_file)
    btn.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
