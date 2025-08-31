def load_image(path: Path):
def main():

# --- Refactored version ---
import argparse
import os
import json
from pathlib import Path
import pygame
from overlay_assets import (
    load_button_overlays, load_hat_overlays, load_cbutton_overlays,
    load_axis_dpad_overlays, load_stick_overlay
)
from joystick_utils import get_joystick
from overlay_logic import (
    handle_debug_events, get_button_overlays, get_hat_overlays,
    get_axis_dpad_overlays, get_cbutton_overlays
)

def parse_tuple_key(key):
    # Converts string like '(0,1)' to tuple (0,1)
    if isinstance(key, str) and key.startswith('(') and key.endswith(')'):
        return tuple(int(x) for x in key[1:-1].split(','))
    return key

def load_profiles(json_path):
    with open(json_path, 'r') as f:
        raw = json.load(f)
    profiles = {}
    for name, prof in raw.items():
        prof = dict(prof)
        # Convert button_overlays keys to int
        if 'button_overlays' in prof:
            prof['button_overlays'] = {int(k): v for k, v in prof['button_overlays'].items()}
        # Convert hat_overlays keys to tuple
        if 'hat_overlays' in prof:
            prof['hat_overlays'] = {parse_tuple_key(k): v for k, v in prof['hat_overlays'].items()}
        # Convert stick_center to tuple if present
        if 'stick_center' in prof and isinstance(prof['stick_center'], list):
            prof['stick_center'] = tuple(prof['stick_center'])
        # Convert c_buttons threshold to float if present
        if 'c_buttons' in prof and 'threshold' in prof['c_buttons']:
            prof['c_buttons']['threshold'] = float(prof['c_buttons']['threshold'])
        # Convert axis_dpad overlays keys if present
        if 'axis_dpad' in prof and 'overlays' in prof['axis_dpad']:
            prof['axis_dpad']['overlays'] = {k: v for k, v in prof['axis_dpad']['overlays'].items()}
        profiles[name] = prof
    return profiles


os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
PROFILES = load_profiles("profiles.json")

def main():
    parser = argparse.ArgumentParser(description="Controller Overlay")
    parser.add_argument(
        "--profile", choices=PROFILES.keys(), default="N64", help="Controller profile to use (NES, SNES, N64, etc.)"
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info for mapping discovery")
    args = parser.parse_args()

    profile = PROFILES[args.profile]
    ASSETS_DIR = Path("assets")

    pygame.init()
    joy = get_joystick(profile)
    if not joy:
        return

    base_path = ASSETS_DIR / profile["base"]
    if not base_path.is_file():
        print("Base image not found:", base_path)
        return
    base_raw = pygame.image.load(str(base_path))
    w, h = base_raw.get_size()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Controller Overlay")
    base_img = base_raw.convert_alpha()

    button_surfaces = load_button_overlays(ASSETS_DIR, profile.get("button_overlays", {}))
    hat_surfaces = load_hat_overlays(ASSETS_DIR, profile.get("hat_overlays", {}))
    cbutton_surfaces = load_cbutton_overlays(ASSETS_DIR, profile.get("c_buttons"))
    axis_dpad_cfg = profile.get("axis_dpad")
    axis_dpad_surfaces = load_axis_dpad_overlays(ASSETS_DIR, axis_dpad_cfg)
    stick_surf = load_stick_overlay(ASSETS_DIR, profile.get("stick_center"), profile.get("stick_overlay"))
    STICK_CENTER = profile.get("stick_center")
    STICK_RADIUS = profile.get("stick_radius", 0)
    DEADZONE = profile.get("deadzone", 0.15)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif args.debug:
                handle_debug_events(event)

        overlays = []
        overlays += get_button_overlays(joy, button_surfaces)
        overlays += get_hat_overlays(joy, hat_surfaces)
        overlays += get_axis_dpad_overlays(joy, axis_dpad_cfg, axis_dpad_surfaces)
        overlays += get_cbutton_overlays(joy, profile, cbutton_surfaces)

        screen.fill((0, 0, 0))
        screen.blit(base_img, (0, 0))
        for surf in overlays:
            screen.blit(surf, (0, 0))

        if STICK_CENTER:
            x = joy.get_axis(0)
            y = joy.get_axis(1)
            if abs(x) < DEADZONE:
                x = 0
            if abs(y) < DEADZONE:
                y = 0
            stick_px = int(STICK_CENTER[0] + x * STICK_RADIUS)
            stick_py = int(STICK_CENTER[1] + y * STICK_RADIUS)
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
