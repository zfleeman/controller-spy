"""
controller_overlay.py

Main entry point for the controller overlay application. Handles argument parsing, profile loading,
and initializes the overlay display using pygame and custom logic modules.
"""

import sys

sys.dont_write_bytecode = True  # Prevent writing __pycache__

import argparse
import os
from pathlib import Path

import pygame

from joystick_utils import get_joystick
from overlay_assets import (
    load_axis_cbutton_overlays,
    load_axis_dpad_overlays,
    load_axis_stick_overlay,
    load_button_overlays,
    load_hat_overlays,
)
from overlay_logic import (
    get_axis_dpad_overlays,
    get_button_overlays,
    get_cbutton_overlays,
    get_hat_overlays,
)
from profiles import PROFILES

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


def main() -> None:
    """
    Main entry point for the controller overlay application. Parses arguments, loads profile, and initializes pygame.
    """
    parser = argparse.ArgumentParser(description="Controller Overlay")
    parser.add_argument(
        "--profile",
        type=str,
        required=True,
        choices=list(PROFILES.keys()),
        help=f"Controller profile to use. Choices: {', '.join(PROFILES.keys())}",
    )
    args = parser.parse_args()

    profile: dict = PROFILES[args.profile]
    assets_dir = Path("assets")

    pygame.init()
    joy = get_joystick(profile)
    if not joy:
        return

    base_path = assets_dir / profile["base"]
    if not base_path.is_file():
        print("Base image not found:", base_path)
        return
    base_raw = pygame.image.load(str(base_path))
    w, h = base_raw.get_size()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(f"{profile['controller_name']} Overlay")
    base_img = base_raw.convert_alpha()

    # every controller should have buttons
    button_surfaces = load_button_overlays(assets_dir=assets_dir, button_overlays=profile.get("button_overlays"))

    # work with hats -- usually a dpad
    hat_overlays = profile.get("hat_overlays", {})
    if hat_overlays:
        hat_surfaces = load_hat_overlays(assets_dir=assets_dir, hat_overlays=hat_overlays)

    # work with axes
    axes: dict = profile.get("axes", {})
    if axes:

        if profile.get("console") == "N64":
            cbutton_cfg = axes.get("c_buttons", {})
            axis_cbutton_surfaces = load_axis_cbutton_overlays(assets_dir, cbutton_cfg)

        axis_dpad_cfg = axes.get("dpad")
        axis_dpad_surfaces = load_axis_dpad_overlays(assets_dir, axis_dpad_cfg)

        l_stick_cfg = axes.get("l_stick", {})
        axis_stick_surfaces = load_axis_stick_overlay(
            assets_dir,
            l_stick_cfg.get("center"),
            l_stick_cfg.get("overlay"),
        )
        l_stick_center = l_stick_cfg.get("center")
        l_stick_radius = l_stick_cfg.get("radius")
        deadzone = l_stick_cfg.get("deadzone")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        overlays = []

        overlays += get_button_overlays(joy, button_surfaces)

        if axes:
            if axis_dpad_cfg:
                overlays += get_axis_dpad_overlays(joy, axis_dpad_cfg, axis_dpad_surfaces)

            if profile.get("console") == "N64":
                overlays += get_cbutton_overlays(joy, profile, axis_cbutton_surfaces)

            if axis_stick_surfaces:
                # Use stick axes from config if present, else default to 0/1
                x_axis = l_stick_cfg.get("x_axis", 0)
                y_axis = l_stick_cfg.get("y_axis", 1)
                x = joy.get_axis(x_axis)
                y = joy.get_axis(y_axis)
                if abs(x) < deadzone:
                    x = 0
                if abs(y) < deadzone:
                    y = 0
                stick_px = int(l_stick_center[0] + x * l_stick_radius)
                stick_py = int(l_stick_center[1] + y * l_stick_radius)
                rect = axis_stick_surfaces.get_rect(center=(stick_px, stick_py))

        if hat_overlays:
            overlays += get_hat_overlays(joy, hat_surfaces)

        screen.fill((0, 0, 0))
        screen.blit(base_img, (0, 0))
        for surface in overlays:
            screen.blit(surface, (0, 0))

        # if axis_stick_surfaces:  # currently bugged for n64
        #     screen.blit(axis_stick_surfaces, rect.topleft)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
