import pygame

def get_joystick(profile):
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joysticks detected.")
        return None
    joystick_index = 0
    found = False
    for i in range(pygame.joystick.get_count()):
        name = pygame.joystick.Joystick(i).get_name()
        if name.lower() == profile["controller_name"].lower():
            joystick_index = i
            found = True
            break
    if not found:
        print(f"Joystick named '{profile['controller_name']}' not found. Available devices:")
        for i in range(pygame.joystick.get_count()):
            print(f"  {i}: {pygame.joystick.Joystick(i).get_name()}")
        return None
    joy = pygame.joystick.Joystick(joystick_index)
    joy.init()
    print(f"Using joystick: {joy.get_name()}")
    return joy
