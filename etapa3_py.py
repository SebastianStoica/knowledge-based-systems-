import tkinter as tk
from tkinter import messagebox
import clips
import matplotlib.pyplot as plt
import re
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys


class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        self.text_widget.update_idletasks()


def print_stdout(message):
    print(message, end='')


def process_input(punct_tinta, obstacol):
    try:
        vector_punct_tinta = list(map(float, punct_tinta.split()))
        obstacol_dim = list(map(float, obstacol.split()))

        if len(vector_punct_tinta) != 3 or len(obstacol_dim) != 6:
            raise ValueError("Punctul tinta trebuie sa aiba 3 coordonate si obstacolul trebuie să aiba 6 valori.")

        print(f"punctul tinta este: {vector_punct_tinta}")
        print(f"obstacolul este: {obstacol_dim}")

        definite_facts = f"""
        (deffacts FAPTE
            (stare robot waiting )
            (coordonate finale X {vector_punct_tinta[0]} Y {vector_punct_tinta[1]} Z {vector_punct_tinta[2]})
            (obstacol lungime: {obstacol_dim[0]} latime: {obstacol_dim[1]} inaltime: {obstacol_dim[2]} centru X: {obstacol_dim[3]} Y: {obstacol_dim[4]} Z: {obstacol_dim[5]})
        )
        """

        with open("etapa3.clp", "r") as f:
            existing_content = f.read()

        updated_content = existing_content + "\n" + definite_facts

        with open("etapa3.clp", "w") as f:
            f.write(updated_content)

        return vector_punct_tinta, obstacol_dim

    except ValueError as e:
        messagebox.showerror("Eroare de input", str(e))
        return None, None


def load_and_run_clips(env):
    env.load("etapa3.clp")
    env.reset()
    env.run(1)

    varfuri_obst = []
    for fact in env.facts():
        if 'varf' in str(fact):
            varfuri_obst.append(fact)

    print(varfuri_obst, len(varfuri_obst))

    x_vals = []
    y_vals = []
    z_vals = []

    for f in varfuri_obst:
        match = re.search(r"X: ([\d.-]+) Y: ([\d.-]+) Z: ([\d.-]+)", str(f))
        if match:
            x_vals.append(float(match.group(1)))
            y_vals.append(float(match.group(2)))
            z_vals.append(float(match.group(3)))

    if len(x_vals) < 8 or len(y_vals) < 8 or len(z_vals) < 8:
        print("Nu au fost gasite suficiente varfuri ale obstacolului.")
        return None

    points = [
        [x_vals[0], y_vals[0], z_vals[0]],
        [x_vals[1], y_vals[1], z_vals[1]],
        [x_vals[2], y_vals[2], z_vals[2]],
        [x_vals[3], y_vals[3], z_vals[3]],
        [x_vals[4], y_vals[4], z_vals[4]],
        [x_vals[5], y_vals[5], z_vals[5]],
        [x_vals[6], y_vals[6], z_vals[6]],
        [x_vals[7], y_vals[7], z_vals[7]]
    ]

    return points


def plot_obstacle_and_target(vector_punct_tinta, points):
    faces = [
        [points[0], points[1], points[2], points[3]],
        [points[4], points[5], points[6], points[7]],
        [points[0], points[1], points[5], points[4]],
        [points[2], points[3], points[7], points[6]],
        [points[1], points[2], points[6], points[5]],
        [points[0], points[3], points[7], points[4]]
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    ax.scatter([vector_punct_tinta[0]], [vector_punct_tinta[1]], [vector_punct_tinta[2]], color='red', s=30,
               label='Punct Tinta')

    ax.set_xlim([-0.55, 0.55])
    ax.set_ylim([-0.55, 0.55])
    ax.set_zlim([-0.55, 0.55])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def run():
    punct_tinta = punct_tinta_entry.get()
    obstacol = obstacol_entry.get()
    vector_punct_tinta, obstacol_dim = process_input(punct_tinta, obstacol)
    if vector_punct_tinta and obstacol_dim:
        points = load_and_run_clips(env)
        if points:
            env.run()
            plot_obstacle_and_target(vector_punct_tinta, points)
def print_state():
    global collected_output
    collected_output = output_text.get("1.0", tk.END)



if __name__ == '__main__':
    env = clips.Environment()

    root = tk.Tk()
    root.title("Robot Navigation")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    punct_tinta_label = tk.Label(frame, text="Introduceti punctul tinta pe x y z:")
    punct_tinta_label.grid(row=0, column=0, padx=10, pady=5)
    punct_tinta_entry = tk.Entry(frame, width=50)
    punct_tinta_entry.grid(row=0, column=1, padx=10, pady=5)

    obstacol_label = tk.Label(frame, text="Introduceti datele pentru obstacol lungime latime inaltime centru x y z:")
    obstacol_label.grid(row=1, column=0, padx=10, pady=5)
    obstacol_entry = tk.Entry(frame, width=50)
    obstacol_entry.grid(row=1, column=1, padx=10, pady=5)

    run_button = tk.Button(frame, text="Run", command=run)
    run_button.grid(row=2, column=0, columnspan=2, pady=10)

    do_nothing_button = tk.Button(frame, text="Print state", command=print_state)
    do_nothing_button.grid(row=3, column=0, columnspan=2, pady=10)

    output_text = tk.Text(root, height=10, width=80)
    output_text.pack(pady=10)

    sys.stdout = StdoutRedirector(output_text)
    sys.stderr = StdoutRedirector(output_text)
    root.mainloop()
