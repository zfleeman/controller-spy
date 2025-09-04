"""
controller_profile.py

Encapsulates all logic and assets for a controller profile, enabling data-driven overlays and input handling.
"""

from pathlib import Path
from typing import Any, Dict

from pygame import Surface
from pygame.joystick import JoystickType
from pygame.rect import Rect

from overlay_assets import (
    load_axis_cbutton_overlays,
    load_axis_dpad_overlays,
    load_axis_stick_overlay,
    load_axis_triggers_overlays,
    load_button_overlays,
    load_hat_overlays,
)
from overlay_logic import (
    get_axis_dpad_overlays,
    get_axis_trigger_overlays,
    get_button_overlays,
    get_cbutton_overlays,
    get_hat_overlays,
)


class ControllerProfile:
    """
    Encapsulates all logic and assets for a controller profile.
    Loads overlays and provides methods to retrieve active overlays and stick positions
    based on the current joystick state. Enables data-driven, extensible controller support.
    Supports multiple analog sticks (e.g., l_stick, r_stick, etc.).
    """

    def __init__(self, profile: dict, assets_dir: Path):
        self.profile = profile
        self.assets_dir = assets_dir

        # buttons
        self.button_surfaces = load_button_overlays(
            assets_dir=assets_dir, button_overlays=profile.get("button_overlays", {})
        )

        # hat
        self.hat_surfaces = load_hat_overlays(assets_dir=assets_dir, hat_overlays=profile.get("hat_overlays", {}))

        # axes
        self.axis_dpad_cfg = profile.get("axes", {}).get("dpad")
        self.axis_dpad_surfaces = (
            load_axis_dpad_overlays(assets_dir=assets_dir, axis_dpad_cfg=self.axis_dpad_cfg)
            if self.axis_dpad_cfg
            else None
        )
        self.cbutton_cfg = profile.get("axes", {}).get("c_buttons")
        self.cbutton_surfaces = (
            load_axis_cbutton_overlays(assets_dir=assets_dir, cbutton_cfg=self.cbutton_cfg)
            if self.cbutton_cfg
            else None
        )
        self.axis_triggers_cfg = profile.get("axes", {}).get("triggers")
        self.axis_triggers_surfaces = (
            load_axis_triggers_overlays(assets_dir=assets_dir, axis_triggers_cfg=self.axis_triggers_cfg)
            if self.axis_triggers_cfg
            else None
        )

        # Support multiple sticks (l_stick, r_stick, etc.)
        self.stick_cfgs = {}
        self.stick_surfaces = {}
        axes: Dict[str, Any] = profile.get("axes", {})
        for stick_name, cfg in axes.items():
            if stick_name.endswith("_stick") and isinstance(cfg, dict):
                self.stick_cfgs[stick_name] = cfg
                self.stick_surfaces[stick_name] = load_axis_stick_overlay(
                    assets_dir=assets_dir, stick_overlay_file=cfg.get("overlay", "")
                )

    def get_active_overlays(self, joy: JoystickType):
        """
        Use the "get" functions" to append our overlays
        """
        overlays = []
        overlays += get_button_overlays(joy=joy, button_surfaces=self.button_surfaces)
        if self.axis_dpad_cfg and self.axis_dpad_surfaces:
            overlays += get_axis_dpad_overlays(
                joy=joy, axis_dpad_cfg=self.axis_dpad_cfg, axis_dpad_surfaces=self.axis_dpad_surfaces
            )
        if self.cbutton_cfg and self.cbutton_surfaces:
            overlays += get_cbutton_overlays(joy=joy, profile=self.profile, cbutton_surfaces=self.cbutton_surfaces)
        if self.hat_surfaces:
            overlays += get_hat_overlays(joy=joy, hat_surfaces=self.hat_surfaces)
        if self.axis_triggers_cfg and self.axis_triggers_surfaces:
            overlays += get_axis_trigger_overlays(
                joy=joy, axis_triggers_cfg=self.axis_triggers_cfg, axis_triggers_surfaces=self.axis_triggers_surfaces
            )
        return overlays

    def get_stick_rect(self, joy: JoystickType, stick_name: str) -> tuple[Surface, Rect]:
        """
        Work with the stick surface
        """
        cfg: dict = self.stick_cfgs.get(stick_name)
        surface: Surface = self.stick_surfaces.get(stick_name)
        if not (cfg and surface):
            return None, None
        x_axis = cfg.get("x_axis", 0)
        y_axis = cfg.get("y_axis", 1)
        x = joy.get_axis(x_axis)
        y = joy.get_axis(y_axis)
        deadzone = cfg.get("deadzone", 0)
        if abs(x) < deadzone:
            x = 0
        if abs(y) < deadzone:
            y = 0
        center = cfg.get("center")
        radius = cfg.get("radius")
        stick_px = int(center[0] + x * radius)
        stick_py = int(center[1] + y * radius)
        return surface, surface.get_rect(center=(stick_px, stick_py))
