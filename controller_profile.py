"""
controller_profile.py

Encapsulates all logic and assets for a controller profile, enabling data-driven overlays and input handling.
"""

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


class ControllerProfile:
    """
    Encapsulates all logic and assets for a controller profile.
    Loads overlays and provides methods to retrieve active overlays and stick positions
    based on the current joystick state. Enables data-driven, extensible controller support.
    Supports multiple analog sticks (e.g., l_stick, r_stick, etc.).
    """

    def __init__(self, profile, assets_dir):
        self.profile = profile
        self.assets_dir = assets_dir

        # Preload all overlays
        self.button_surfaces = load_button_overlays(assets_dir, profile.get("button_overlays", {}))
        self.hat_surfaces = load_hat_overlays(assets_dir, profile.get("hat_overlays", {}))
        self.axis_dpad_cfg = profile.get("axes", {}).get("dpad")
        self.axis_dpad_surfaces = (
            load_axis_dpad_overlays(assets_dir, self.axis_dpad_cfg) if self.axis_dpad_cfg else None
        )
        self.cbutton_cfg = profile.get("axes", {}).get("c_buttons")
        self.cbutton_surfaces = load_axis_cbutton_overlays(assets_dir, self.cbutton_cfg) if self.cbutton_cfg else None

        # Support multiple sticks (l_stick, r_stick, etc.)
        self.stick_cfgs = {}
        self.stick_surfaces = {}
        axes = profile.get("axes", {})
        for stick_name, cfg in axes.items():
            if stick_name.endswith("_stick") and isinstance(cfg, dict):
                self.stick_cfgs[stick_name] = cfg
                self.stick_surfaces[stick_name] = load_axis_stick_overlay(assets_dir, cfg.get("overlay", ""))

    def get_active_overlays(self, joy):
        overlays = []
        overlays += get_button_overlays(joy, self.button_surfaces)
        if self.axis_dpad_cfg and self.axis_dpad_surfaces:
            overlays += get_axis_dpad_overlays(joy, self.axis_dpad_cfg, self.axis_dpad_surfaces)
        if self.cbutton_cfg and self.cbutton_surfaces:
            overlays += get_cbutton_overlays(joy, self.profile, self.cbutton_surfaces)
        if self.hat_surfaces:
            overlays += get_hat_overlays(joy, self.hat_surfaces)
        return overlays

    def get_stick_rect(self, joy, stick_name):
        cfg = self.stick_cfgs.get(stick_name)
        surface = self.stick_surfaces.get(stick_name)
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
