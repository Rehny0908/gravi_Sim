import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Kugel Klasse
class Sphere:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

# Streamlit App
st.title("Kugel-Erstellung")

# Benutzeranpassungen
color = st.color_picker("Wähle die Farbe der Kugeln", "#FF0000")
radius = st.number_input("Radius der Kugel (in px)", min_value=5, value=20)

# Kugel-Array in der Sitzung speichern
if 'spheres' not in st.session_state:
    st.session_state.spheres = []

# Funktion zum Erstellen von Kugeln
def create_sphere(x, y):
    st.session_state.spheres.append(Sphere(x, y, radius, color))

# Benutzeroberfläche für Kugelerstellung
if st.button("Reset"):
    st.session_state.spheres = []

# Zeichne das Diagramm und füge Klick-Funktionalität hinzu
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)

# Erstelle das Diagramm
def draw_spheres():
    ax.clear()
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)
    
    for sphere in st.session_state.spheres:
        circle = plt.Circle((sphere.x, sphere.y), sphere.radius, color=sphere.color, alpha=0.5)
        ax.add_patch(circle)

    plt.axis('off')  # Achsen ausblenden
    st.pyplot(fig)

# Ereignis zum Klicken und Erstellen von Kugeln
if st.button("Klicke hier, um eine Kugel zu erstellen (dann in das Diagramm klicken)"):
    clicked = st.empty()
    
    # Plot wird angezeigt und wartet auf Klicks
    click_placeholder = st.empty()
    click_placeholder.pyplot(fig)

    def onclick(event):
        if event.inaxes == ax:
            create_sphere(event.xdata, event.ydata)
            draw_spheres()

    fig.canvas.mpl_connect('button_press_event', onclick)

    # Initialisiere den Plot
    draw_spheres()
