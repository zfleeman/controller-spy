


def handle_debug_events(event):
    # Joystick event type values: 1536=JOYAXISMOTION, 1539=JOYBUTTONDOWN, 1540=JOYBUTTONUP, 1541=JOYHATMOTION
    if event.type == 1539:
        print(f"JOYBUTTONDOWN index={event.button}")
    elif event.type == 1540:
        print(f"JOYBUTTONUP index={event.button}")
    elif event.type == 1541:
        print(f"JOYHATMOTION hat={event.hat} value={event.value}")
    elif event.type == 1536:
        print(f"JOYAXISMOTION axis={event.axis} value={event.value:.3f}")

def get_button_overlays(joy, button_surfaces):
    overlays = []
    for i in range(joy.get_numbuttons()):
        if joy.get_button(i) and i in button_surfaces:
            overlays.append(button_surfaces[i])
    return overlays

def get_hat_overlays(joy, hat_surfaces):
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

def get_axis_dpad_overlays(joy, axis_dpad_cfg, axis_dpad_surfaces):
    overlays = []
    if axis_dpad_cfg and axis_dpad_surfaces:
        xi = axis_dpad_cfg.get("x_axis", 0)
        yi = axis_dpad_cfg.get("y_axis", 1)
        th = axis_dpad_cfg.get("threshold", 0.5)
        inv_y = axis_dpad_cfg.get("invert_y", False)
        x = joy.get_axis(xi)
        y = joy.get_axis(yi)
        if inv_y:
            y = -y
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

def get_cbutton_overlays(joy, profile, cbutton_surfaces):
    overlays = []
    if "c_buttons" in profile:
        for direction, mapping in profile["c_buttons"].items():
            if direction not in ["up", "down", "left", "right"]:
                continue
            axis_val = joy.get_axis(mapping["axis"])
            if mapping["direction"] == -1 and axis_val < -profile["c_buttons"]["threshold"]:
                overlays.append(cbutton_surfaces[direction])
            elif mapping["direction"] == 1 and axis_val > profile["c_buttons"]["threshold"]:
                overlays.append(cbutton_surfaces[direction])
    return overlays
