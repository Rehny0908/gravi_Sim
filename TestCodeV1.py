import streamlit as st
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
    
# Reset-Button
if st.button("Reset"):
    st.session_state.spheres = []

# Matplotlib Plot erstellen
fig, ax = plt.subplots()
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)

# Zeichne die Kugeln
def draw_spheres():
    ax.clear()
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)
    
    for sphere in st.session_state.spheres:
        circle = plt.Circle((sphere.x, sphere.y), sphere.radius, color=sphere.color, alpha=0.5)
        ax.add_patch(circle)

    plt.axis('off')  # Achsen ausblenden
    st.pyplot(fig)

# Platzierung der Kugel beim Mausklick
if st.button("Klicke hier, um Kugel im Diagramm zu erstellen"):
    # Platzhalter für das Diagramm
    click_placeholder = st.empty()
    
    # Klicke auf das Diagramm
    click_placeholder.pyplot(fig)
    
    # Warte auf Klicks
    def onclick(event):
        if event.inaxes == ax:
            create_sphere(event.xdata, event.ydata)
            draw_spheres()

    # Event zum Klicken auf das Diagramm
    fig.canvas.mpl_connect('button_press_event', onclick)
    
    # Zeichne initiale Kugeln
    draw_spheres()
