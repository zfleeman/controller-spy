"""
joystick_utils.py

Utility functions for initializing and retrieving pygame joystick objects based on controller profiles.
"""

import pygame


def get_joystick(profile: dict) -> "pygame.joystick.Joystick | None":
    """
    Initializes and returns a pygame joystick matching the controller name in the profile.
    Args:
        profile (dict): The controller profile containing 'controller_name'.
    Returns:
        pygame.joystick.Joystick | None: The joystick object if found, else None.
    """
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
