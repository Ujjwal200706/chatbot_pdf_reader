import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, END
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import main
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def upload_pdfs():
    file_path = filedialog.askopenfilename(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    logging.info("Uploading PDF...")
    pdf_list.delete(0, END)
    pdf_list.insert(0,file_path)
    try:
        main.pdf_loader(pdf_list.get(0))
        logging.info("PDF uploaded successfully.")
    except Exception as e:
        logging.error(f"Error uploading PDF: {e}")


def ask_question():
    logging.info("Asking question...")
    question = question_box.get("1.0", END).strip()
    answer_box.delete("1.0", END)
    try:
        answer=main.answer(question)
        logging.info(f"Answer received from main.py: {answer}")
        answer_box.insert(END, answer)
        answer_box.update()
        logging.info("Answer displayed in UI successfully.")
    except Exception as e:
        logging.error(f"Error updating UI: {e}")


# Main window
root = ttk.Window(themename="darkly")
root.title("PDF QA System")
root.geometry("1000x600")
#root.configure(bg="#F5F5F5")  # Light gray background

# ================= LEFT FRAME (PDF Upload Section) ======================
left_frame = ttk.Frame(root, padding=(20, 10), width=300)
left_frame.grid(row=0, column=0, sticky="ns")

title_label = ttk.Label(left_frame, text="Upload PDFs", font=("Arial", 16, "bold"))
title_label.pack(pady=(0,10))

upload_btn = ttk.Button(left_frame, text="Select PDF Files", command=upload_pdfs, width=20, bootstyle="primary")
upload_btn.pack(pady=(0,10))

pdf_list = tk.Listbox(left_frame, width=40, height=1)
pdf_list.pack(pady=(0,10))


# ================= RIGHT FRAME (Question + Answer Section) ======================
right_frame = ttk.Frame(root, padding=(20, 10))
right_frame.grid(row=0, column=1, sticky="nsew")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Question Label
q_label = ttk.Label(right_frame, text="Write your question:", font=("Arial", 14, "bold"))
q_label.pack(anchor="w",pady=(0,5))

# Question Text Box
question_box = Text(right_frame, height=1, font=("Arial", 12))
question_box.pack(fill="x", pady=(0,5))

# Ask Button
ask_btn = ttk.Button(right_frame, text="Ask", command=ask_question, width=10, bootstyle="primary")
ask_btn.pack(pady=(0,5))

# Answer Label
a_label = ttk.Label(right_frame, text="Answer:", font=("Arial", 14, "bold"))
a_label.pack(anchor="w", pady=(10,5))

# Answer Text Box with Scrollbar
answer_frame = ttk.Frame(right_frame)
answer_frame.pack(fill="both", expand=True)


answer_box = Text(answer_frame, height=5, font=("Arial", 12),  wrap="word")
answer_box.pack(fill="both", expand=True)
answer_box.config(state="normal")



# Run the UI
root.mainloop()

