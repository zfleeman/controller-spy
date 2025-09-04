import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    quit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick Name: {joystick.get_name()}")
print(f"Buttons: {joystick.get_numbuttons()}")
print(f"Axes: {joystick.get_numaxes()}")
print(f"Hats: {joystick.get_numhats()}")
print("Press buttons, move sticks, or press the D-Pad (Ctrl+C to quit):\n")

# We store last seen values to only print changes
last_axes = [0.0] * joystick.get_numaxes()
last_buttons = [0] * joystick.get_numbuttons()
last_hats = [(0, 0)] * joystick.get_numhats()
THRESH = 0.05  # Only print axes changes above this threshold

while True:
    pygame.event.pump()
    # Axes
    for i in range(joystick.get_numaxes()):
        val = joystick.get_axis(i)
        if abs(val - last_axes[i]) > THRESH:
            print(f"Axis {i}: {val:.2f}")
            last_axes[i] = val

    # Buttons
    for i in range(joystick.get_numbuttons()):
        val = joystick.get_button(i)
        if val != last_buttons[i]:
            state = "pressed" if val else "released"
            print(f"Button {i}: {state}")
            last_buttons[i] = val

    # Hats (D-pad)
    for i in range(joystick.get_numhats()):
        val = joystick.get_hat(i)
        if val != last_hats[i]:
            print(f"Hat {i}: {val}")
            last_hats[i] = val

    pygame.time.wait(20)
