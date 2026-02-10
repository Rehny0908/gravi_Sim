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
st.write("Klicke, um Kugeln zu erstellen. Die Kugeln ziehen sich gegenseitig an und addieren ihre Masse, wenn sie überlappen.")

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
    if 0 <= x <= 800 and 0 <= y <= 600:  # Sicherstellen, dass die Kugel im Sichtbereich liegt.
        st.session_state.spheres.append(Sphere(x, y, radius, mass, color))

# Benutzeroberfläche für Kugelerstellung
if st.button("Reset"):
    st.session_state.spheres = []
    st.experimental_rerun()

# Graphik erstellen
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)

def update(frame):
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
                    sphere.mass += other.mass  # Masse addieren
                    st.session_state.spheres.remove(other)  # Andere Kugel entfernen
        
        # Zeichne die Kugel
        circle = plt.Circle((sphere.x, sphere.y), sphere.radius, color=sphere.color, alpha=0.5)
        ax.add_patch(circle)

# Animation mit Funktionsaufruf
ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100)

# Zeichne die Animation in Streamlit
st.pyplot(fig)

# Event zum Erstellen von Kugeln (Klick-Event)
x_click = st.number_input("X-Position (in px)", min_value=0, max_value=800, value=400)
y_click = st.number_input("Y-Position (in px)", min_value=0, max_value=600, value=300)
if st.button("Klick hier, um eine Kugel zu erstellen"):
    create_sphere(x_click, y_click)
