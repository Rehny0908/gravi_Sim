import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Kugel Klasse
class Sphere:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.vx = 0
        self.vy = 0

    def apply_gravity(self, spheres, dt):
        for other in spheres:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = np.sqrt(dx**2 + dy**2)
                if distance > self.radius + other.radius:
                    force = self.mass * other.mass / (distance ** 2)
                    angle = np.arctan2(dy, dx)
                    self.vx += force * np.cos(angle) / self.mass * dt
                    self.vy += force * np.sin(angle) / self.mass * dt

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

# Streamlit App
st.title("Gravitationsfeld-Simulation")
st.write("Klicke im Diagramm, um Kugeln zu erstellen. Sie ziehen sich gegenseitig an und addieren ihre Masse, wenn sie überlappen.")

# Benutzeranpassungen
color = st.color_picker("Wähle die Farbe der Kugeln", "#FF0000")
mass = st.number_input("Masse der Kugel (in kg)", min_value=1.0, value=1.0)
radius = st.number_input("Radius der Kugel (in px)", min_value=5, value=20)
sim_time = st.slider("Simulationszeit (in Sekunden)", min_value=0.1, max_value=5.0, value=1.0)

# Kugel-Array in der Sitzung speichern
if 'spheres' not in st.session_state:
    st.session_state.spheres = []

# Funktion für das Erstellen von Kugeln
def create_sphere(x, y):
    if 0 <= x <= 800 and 0 <= y <= 600:
        st.session_state.spheres.append(Sphere(x, y, radius, mass, color))

# Benutzeroberfläche für Kugelerstellung
if st.button("Reset"):
    st.session_state.spheres = []
    st.experimental_rerun()

# Graphik erstellen
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)

# Event zum Erstellen von Kugeln via Maus-Click
clicked = st.button("Klicke hier, um Kugel zu erstellen (dann in das Diagramm klicken)")

if clicked:
    # Ein `st.empty()`-Platzhalter, um die Chart-Daten zu aktualisieren
    placeholder = st.empty()
    
    # Interakiver Bereich für das Diagramm
    # Nutzer wird aufgefordert, im Diagramm zu klicken
    st.write("Klicke im Diagramm, um eine Kugel zu erstellen.")
    
    # Matplotlib-Interaktion
    def onclick(event):
        x, y = event.xdata, event.ydata
        if event.inaxes is not None:
            create_sphere(int(x), int(y))
            update_plot()

    def update_plot():
        ax.clear()
        ax.set_xlim(0, 800)
        ax.set_ylim(0, 600)
        
        for sphere in st.session_state.spheres:
            sphere.apply_gravity(st.session_state.spheres, sim_time)
            sphere.update_position(sim_time)

            # Überlappende Kugeln kombinieren
            for other in st.session_state.spheres:
                if other != sphere:
                    distance = np.sqrt((sphere.x - other.x) ** 2 + (sphere.y - other.y) ** 2)
                    if distance < sphere.radius + other.radius:
                        sphere.mass += other.mass
                        st.session_state.spheres.remove(other)
            
            # Zeichne die Kugel
            circle = plt.Circle((sphere.x, sphere.y), sphere.radius, color=sphere.color, alpha=0.5)
            ax.add_patch(circle)
        
        placeholder.pyplot(fig)

    # Erstelle ein Matplotlib-Diagramm
    fig.canvas.mpl_connect('button_press_event', onclick)

    # Initiale Plot-Ausgabe
    update_plot()

# Zeichne die Animation in Streamlit
st.pyplot(fig)
