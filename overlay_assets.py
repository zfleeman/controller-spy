"""
overlay_assets.py

Functions for loading controller overlay images and assets from disk using pygame.
"""

from pathlib import Path

import pygame


def load_image(path: Path) -> "pygame.Surface":
    """
    Loads an image from the given path and converts it for alpha transparency.
    Args:
        path (Path): Path to the image file.
    Returns:
        pygame.Surface: The loaded image surface.
    """
    return pygame.image.load(path).convert_alpha()


def load_button_overlays(assets_dir: Path, button_overlays: dict) -> dict:
    """
    Loads button overlay images from the assets directory.
    Args:
        assets_dir (Path): Directory containing assets.
        button_overlays (dict): Mapping of button indices to filenames.
    Returns:
        dict: Mapping of button indices to loaded image surfaces.
    """
    button_surfaces = {}
    for idx, fname in button_overlays.items():
        path = assets_dir / fname
        if path.is_file():
            button_surfaces[idx] = pygame.image.load(str(path)).convert_alpha()
        else:
            print(f"Warning: button overlay missing {path}")
    return button_surfaces


def load_hat_overlays(assets_dir: Path, hat_overlays: dict) -> dict:
    """
    Loads hat overlay images from the assets directory.
    Args:
        assets_dir (Path): Directory containing assets.
        hat_overlays (dict): Mapping of hat positions to filenames.
    Returns:
        dict: Mapping of hat positions to loaded image surfaces.
    """
    hat_surfaces = {}
    for hat, fname in hat_overlays.items():
        path = assets_dir / fname
        if path.is_file():
            hat_surfaces[hat] = pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: hat overlay missing {path}")
    return hat_surfaces


def load_cbutton_overlays(assets_dir: Path, cbutton_cfg: dict) -> dict:
    """
    Loads C button overlay images from the assets directory.
    Args:
        assets_dir (Path): Directory containing assets.
        cbutton_cfg (dict): Configuration for C buttons.
    Returns:
        dict: Mapping of directions to loaded image surfaces.
    """
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


def load_axis_dpad_overlays(assets_dir: Path, axis_dpad_cfg: dict) -> dict:
    """
    Loads axis D-pad overlay images from the assets directory.
    Args:
        assets_dir (Path): Directory containing assets.
        axis_dpad_cfg (dict): Configuration for axis D-pad overlays.
    Returns:
        dict: Mapping of overlay keys to loaded image surfaces.
    """
    axis_dpad_surfaces = {}
    if axis_dpad_cfg:
        for key, fname in axis_dpad_cfg.get("overlays", {}).items():
            path = assets_dir / fname
            if path.is_file():
                axis_dpad_surfaces[key] = load_image(path)
            else:
                print(f"Warning: missing axis-dpad overlay: {path}")
    return axis_dpad_surfaces


def load_stick_overlay(
    assets_dir: Path, stick_center: tuple | None, stick_overlay_file: str | None
) -> "pygame.Surface | None":
    """
    Loads the stick overlay image from the assets directory if specified.
    Args:
        assets_dir (Path): Directory containing assets.
        stick_center (tuple | None): Center position of the stick (unused here).
        stick_overlay_file (str | None): Filename of the stick overlay image.
    Returns:
        pygame.Surface | None: The loaded image surface or None if not found.
    """
    if stick_center and stick_overlay_file:
        path = assets_dir / stick_overlay_file
        if path.is_file():
            return pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: stick overlay missing {path}")
    return None
