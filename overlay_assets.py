import pygame
from pathlib import Path

def load_image(path: Path):
    return pygame.image.load(path).convert_alpha()

def load_button_overlays(assets_dir, button_overlays):
    button_surfaces = {}
    for idx, fname in button_overlays.items():
        path = assets_dir / fname
        if path.is_file():
            button_surfaces[idx] = pygame.image.load(str(path)).convert_alpha()
        else:
            print(f"Warning: button overlay missing {path}")
    return button_surfaces

def load_hat_overlays(assets_dir, hat_overlays):
    hat_surfaces = {}
    for hat, fname in hat_overlays.items():
        path = assets_dir / fname
        if path.is_file():
            hat_surfaces[hat] = pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: hat overlay missing {path}")
    return hat_surfaces

def load_cbutton_overlays(assets_dir, cbutton_cfg):
    cbutton_surfaces = {}
    if cbutton_cfg:
        for direction in ["up", "down", "left", "right"]:
            mapping = cbutton_cfg.get(direction)
            if mapping:
                path = assets_dir / mapping["image"]
                if path.is_file():
                    cbutton_surfaces[direction] = pygame.image.load(path).convert_alpha()
                else:
                    print(f"Warning: missing C button overlay: {path}")
    return cbutton_surfaces

def load_axis_dpad_overlays(assets_dir, axis_dpad_cfg):
    axis_dpad_surfaces = {}
    if axis_dpad_cfg:
        for key, fname in axis_dpad_cfg.get("overlays", {}).items():
            path = assets_dir / fname
            if path.is_file():
                axis_dpad_surfaces[key] = load_image(path)
            else:
                print(f"Warning: missing axis-dpad overlay: {path}")
    return axis_dpad_surfaces

def load_stick_overlay(assets_dir, stick_center, stick_overlay_file):
    if stick_center and stick_overlay_file:
        path = assets_dir / stick_overlay_file
        if path.is_file():
            return pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: stick overlay missing {path}")
    return None
