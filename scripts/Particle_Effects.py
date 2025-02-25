from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QEasingCurve
from PyQt5.QtGui import QPixmap
import random

PARTICLE_IMAGE = "assets/particle.png"
PARTICLE_SIZE_RANGE = (30, 50) 
ANIMATION_DURATION = 1200 
SPAWN_OFFSET = 15  
FLOAT_DISTANCE = 60 

def spawn_particle(game):
    """Spawns a floating particle effect with fade-out."""
    if not game.isVisible():
        return

    pixmap = QPixmap(PARTICLE_IMAGE)
    if pixmap.isNull():
        print(f"Error: {PARTICLE_IMAGE} not found.")
        return

    particle = QLabel(game)
    particle.setPixmap(pixmap)
    particle.setScaledContents(True)


    size = random.randint(*PARTICLE_SIZE_RANGE)
    particle.setFixedSize(size, size)


    opacity_effect = QGraphicsOpacityEffect()
    particle.setGraphicsEffect(opacity_effect)
    particle.setAttribute(Qt.WA_TranslucentBackground)


    button_pos = game.click_button.mapToGlobal(game.click_button.rect().center())
    x = button_pos.x() + random.randint(-SPAWN_OFFSET, SPAWN_OFFSET) - game.geometry().x()
    y = button_pos.y() + random.randint(-SPAWN_OFFSET, SPAWN_OFFSET) - game.geometry().y()

    particle.move(x, y)
    particle.show()


    float_anim = QPropertyAnimation(particle, b"pos")
    float_anim.setDuration(ANIMATION_DURATION)
    float_anim.setStartValue(QPoint(x, y))
    float_anim.setEndValue(QPoint(x, y - FLOAT_DISTANCE))
    float_anim.setEasingCurve(QEasingCurve.InOutQuad)


    fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
    fade_anim.setDuration(ANIMATION_DURATION)
    fade_anim.setStartValue(1.0)
    fade_anim.setEndValue(0.0)


    float_anim.start()
    fade_anim.start()


    QTimer.singleShot(ANIMATION_DURATION, particle.deleteLater)

def load_once(game):
    """Attaches the particle effect to the main click button."""
    game.click_button.clicked.connect(lambda: spawn_particle(game))
    print("✨ Particle mod loaded!")
