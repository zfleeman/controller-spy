"""
controller_overlay.py

Main entry point for the controller overlay application. Handles argument parsing, profile loading,
and initializes the overlay display using pygame and custom logic modules.
"""

import argparse
import json
import os
from pathlib import Path

import pygame

from joystick_utils import get_joystick
from overlay_assets import (
    load_axis_dpad_overlays,
    load_button_overlays,
    load_cbutton_overlays,
    load_hat_overlays,
    load_stick_overlay,
)
from overlay_logic import (
    get_axis_dpad_overlays,
    get_button_overlays,
    get_cbutton_overlays,
    get_hat_overlays,
)


def parse_tuple_key(key: str | tuple | int) -> tuple | int:
    """
    Converts a string like '(0,1)' to a tuple (0, 1). Returns the key unchanged if not a tuple string.
    Args:
        key (str | tuple | int): The key to parse.
    Returns:
        tuple | int: The parsed tuple or the original key.
    """
    if isinstance(key, str) and key.startswith("(") and key.endswith(")"):
        return tuple(int(x) for x in key[1:-1].split(","))
    return key


def load_profiles(json_path: Path) -> dict:
    """
    Loads controller profiles from a JSON file and normalizes key types.
    Args:
        json_path (str | Path): Path to the JSON file.
    Returns:
        dict: Dictionary of profiles with normalized keys.
    """
    with json_path.open("r", encoding="UTF-8") as f:
        raw = json.load(f)
    profiles = {}
    for name, prof in raw.items():
        prof = dict(prof)
        # Convert button_overlays keys to int
        if "button_overlays" in prof:
            prof["button_overlays"] = {int(k): v for k, v in prof["button_overlays"].items()}
        # Convert hat_overlays keys to tuple
        if "hat_overlays" in prof:
            prof["hat_overlays"] = {parse_tuple_key(k): v for k, v in prof["hat_overlays"].items()}
        # Convert stick_center to tuple if present
        if "stick_center" in prof and isinstance(prof["stick_center"], list):
            prof["stick_center"] = tuple(prof["stick_center"])
        # Convert c_buttons threshold to float if present
        if "c_buttons" in prof and "threshold" in prof["c_buttons"]:
            prof["c_buttons"]["threshold"] = float(prof["c_buttons"]["threshold"])
        # Convert axis_dpad overlays keys if present
        if "axis_dpad" in prof and "overlays" in prof["axis_dpad"]:
            prof["axis_dpad"]["overlays"] = {k: v for k, v in prof["axis_dpad"]["overlays"].items()}
        profiles[name] = prof
    return profiles


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
PROFILES = load_profiles(Path("profiles.json"))


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
    pygame.display.set_caption("Controller Overlay")
    base_img = base_raw.convert_alpha()

    button_surfaces = load_button_overlays(assets_dir, profile.get("button_overlays", {}))
    hat_surfaces = load_hat_overlays(assets_dir, profile.get("hat_overlays", {}))
    cbutton_surfaces = load_cbutton_overlays(assets_dir, profile.get("c_buttons"))
    axis_dpad_cfg = profile.get("axis_dpad")
    axis_dpad_surfaces = load_axis_dpad_overlays(assets_dir, axis_dpad_cfg)
    stick_surf = load_stick_overlay(assets_dir, profile.get("stick_center"), profile.get("stick_overlay"))
    stick_center = profile.get("stick_center")
    stick_radius = profile.get("stick_radius", 0)
    deadzone = profile.get("deadzone", 0.15)

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
        overlays += get_hat_overlays(joy, hat_surfaces)
        overlays += get_axis_dpad_overlays(joy, axis_dpad_cfg, axis_dpad_surfaces)
        overlays += get_cbutton_overlays(joy, profile, cbutton_surfaces)

        screen.fill((0, 0, 0))
        screen.blit(base_img, (0, 0))
        for surf in overlays:
            screen.blit(surf, (0, 0))

        if stick_center:
            x = joy.get_axis(0)
            y = joy.get_axis(1)
            if abs(x) < deadzone:
                x = 0
            if abs(y) < deadzone:
                y = 0
            stick_px = int(stick_center[0] + x * stick_radius)
            stick_py = int(stick_center[1] + y * stick_radius)
            if stick_surf:
                rect = stick_surf.get_rect(center=(stick_px, stick_py))
                screen.blit(stick_surf, rect.topleft)
            else:
                pygame.draw.circle(screen, (255, 0, 0), (stick_px, stick_py), 6)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
