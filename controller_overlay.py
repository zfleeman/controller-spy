"""
controller_overlay.py

Main entry point for the controller overlay application. Handles argument parsing, profile loading,
and initializes the overlay display using pygame and custom logic modules.
"""

import sys

sys.dont_write_bytecode = True  # Prevent writing __pycache__

import argparse
import os
from argparse import Namespace
from pathlib import Path

import pygame

from controller_profile import ControllerProfile
from joystick_utils import get_joystick
from profiles import PROFILES

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


def get_args() -> Namespace:
    """
    Parse arguments/get profile.
    """
    parser = argparse.ArgumentParser(description="Controller Overlay")
    parser.add_argument(
        "--profile",
        type=str,
        required=True,
        choices=list(PROFILES.keys()),
        help=f"Controller profile to use. Choices: {', '.join(PROFILES.keys())}",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the controller overlay application. Parses arguments, loads profile, and initializes pygame.
    """
    args = get_args()
    profile: dict = PROFILES[args.profile]
    assets_dir = Path("assets")
    pygame.init()
    joy = get_joystick(profile)

    if not joy:
        raise RuntimeError(f"Joystick not found: {profile['controller_name']}")

    base_path = assets_dir / profile["base"]
    if not base_path.is_file():
        raise FileNotFoundError(f"Base image not found: {base_path}")

    base_raw = pygame.image.load(str(base_path))
    w, h = base_raw.get_size()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Game Controller Overlay")
    base_img = base_raw.convert_alpha()

    # Use the new ControllerProfile abstraction
    controller_profile = ControllerProfile(profile, assets_dir)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        overlays = controller_profile.get_active_overlays(joy)

        screen.fill((0, 0, 0))
        screen.blit(base_img, (0, 0))
        for surface in overlays:
            screen.blit(surface, (0, 0))

        # Draw all stick overlays (l_stick, r_stick, etc.)
        for stick_name in controller_profile.stick_cfgs:
            surface, rect = controller_profile.get_stick_rect(joy, stick_name)
            if surface and rect:
                screen.blit(surface, rect.topleft)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
