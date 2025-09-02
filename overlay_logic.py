"""
overlay_logic.py

Logic for determining which overlays to display based on joystick state and profile configuration.
Includes overlay selection for buttons, hats, axis D-pads, and C buttons.
"""

from pygame.joystick import JoystickType


def get_button_overlays(joy: JoystickType, button_surfaces: dict[int, object]) -> list[object]:
    """
    Returns a list of button overlay surfaces for pressed buttons.
    Args:
        joy: The pygame joystick object.
        button_surfaces (dict): Mapping of button indices to surfaces.
    Returns:
        list: List of surfaces for pressed buttons.
    """
    overlays = []
    for i in range(joy.get_numbuttons()):
        if joy.get_button(i) and i in button_surfaces:
            overlays.append(button_surfaces[i])
    return overlays


def get_hat_overlays(joy: JoystickType, hat_surfaces: dict[tuple[int, int], object]) -> list[object]:
    """
    Returns a list of hat overlay surfaces for active hats.
    Args:
        joy: The pygame joystick object.
        hat_surfaces (dict): Mapping of hat positions to surfaces.
    Returns:
        list: List of surfaces for active hats.
    """
    overlays = []
    for h in range(joy.get_numhats()):
        hat = joy.get_hat(h)
        if hat != (0, 0):
            if hat in hat_surfaces:
                overlays.append(hat_surfaces[hat])
            else:
                if hat[1] != 0 and (0, hat[1]) in hat_surfaces:
                    overlays.append(hat_surfaces[(0, hat[1])])
                if hat[0] != 0 and (hat[0], 0) in hat_surfaces:
                    overlays.append(hat_surfaces[(hat[0], 0)])
    return overlays


def get_axis_dpad_overlays(
    joy: JoystickType, axis_dpad_cfg: dict[str, object], axis_dpad_surfaces: dict[str, object]
) -> list[object]:
    """
    Returns a list of axis D-pad overlay surfaces based on joystick axis values.
    Args:
        joy: The pygame joystick object.
        axis_dpad_cfg (dict): Configuration for axis D-pad overlays.
        axis_dpad_surfaces (dict): Mapping of overlay keys to surfaces.
    Returns:
        list: List of surfaces for active axis D-pad directions.
    """
    overlays = []
    if axis_dpad_cfg and axis_dpad_surfaces:
        xi = axis_dpad_cfg.get("x_axis", 0)
        yi = axis_dpad_cfg.get("y_axis", 1)
        th = axis_dpad_cfg.get("threshold", 0.5)
        x = joy.get_axis(xi)
        y = joy.get_axis(yi)
        left = x <= -th
        right = x >= th
        up = y <= -th
        down = y >= th
        if up and left and "up_left" in axis_dpad_surfaces:
            overlays.append(axis_dpad_surfaces["up_left"])
        elif up and right and "up_right" in axis_dpad_surfaces:
            overlays.append(axis_dpad_surfaces["up_right"])
        elif down and left and "down_left" in axis_dpad_surfaces:
            overlays.append(axis_dpad_surfaces["down_left"])
        elif down and right and "down_right" in axis_dpad_surfaces:
            overlays.append(axis_dpad_surfaces["down_right"])
        else:
            if up and "up" in axis_dpad_surfaces:
                overlays.append(axis_dpad_surfaces["up"])
            if down and "down" in axis_dpad_surfaces:
                overlays.append(axis_dpad_surfaces["down"])
            if left and "left" in axis_dpad_surfaces:
                overlays.append(axis_dpad_surfaces["left"])
            if right and "right" in axis_dpad_surfaces:
                overlays.append(axis_dpad_surfaces["right"])
    return overlays


def get_cbutton_overlays(
    joy: JoystickType, profile: dict[str, object], cbutton_surfaces: dict[str, object]
) -> list[object]:
    """
    Returns a list of C button overlay surfaces based on joystick axis values and profile config.
    Args:
        joy: The pygame joystick object.
        profile (dict): Controller profile containing C button config.
        cbutton_surfaces (dict): Mapping of directions to surfaces.
    Returns:
        list: List of surfaces for active C button directions.
    """
    overlays = []
    c_buttons = None
    # Prefer axes["c_buttons"] if present (N64), else fallback to profile["c_buttons"] for legacy
    if "axes" in profile and "c_buttons" in profile["axes"]:
        c_buttons = profile["axes"]["c_buttons"]
    elif "c_buttons" in profile:
        c_buttons = profile["c_buttons"]
    if c_buttons:
        threshold = c_buttons.get("threshold", 0.5)
        for direction in ["up", "down", "left", "right"]:
            mapping = c_buttons.get(direction)
            if not mapping:
                continue
            axis_val = joy.get_axis(mapping["axis"])
            if mapping["direction"] == -1 and axis_val < -threshold:
                overlays.append(cbutton_surfaces[direction])
            elif mapping["direction"] == 1 and axis_val > threshold:
                overlays.append(cbutton_surfaces[direction])
    return overlays
