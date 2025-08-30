import argparse
from pathlib import Path

import pygame

# ------------------- Profiles -------------------
PROFILES = {
    "NES": {
        "base": "nes/base.png",
        "button_overlays": {
            2: "nes/b.png",
            3: "nes/a.png",
            8: "nes/select.png",
            9: "nes/start.png",
        },
        "controller_name": "JC-W01U",
        "hat_overlays": {
            (0, 1): "nes/up.png",
            (0, -1): "nes/down.png",
            (-1, 0): "nes/left.png",
            (1, 0): "nes/right.png",
        },
    },
    "SNES": {
        "base": "snes/base.png",
        "button_overlays": {
            0: "snes/b.png",
            1: "snes/a.png",
            2: "snes/y.png",
            3: "snes/x.png",
            4: "snes/l.png",
            5: "snes/r.png",
            6: "snes/select.png",
            7: "snes/start.png",
        },
        "controller_name": "SNES PC Game Pad",
        # Axis-based D-pad config
        "axis_dpad": {
            "x/axis": 0,            # typically 0: left/right  (-1..+1)
            "y/axis": 1,            # typically 1: up/down     (-1..+1)
            "threshold": 0.5,       # >=0.5 counted as pressed
            "invert/y": False,      # set True if your adapter reports up as +1
            "overlays": {
                "left":  "snes/left.png",
                "right": "snes/right.png",
                "up":    "snes/up.png",
                "down":  "snes/down.png",
                "up/left": "snes/up_left.png",
                "up/right": "snes/up_right.png",
                "down/left": "snes/down_left.png",
                "down/right":"snes/down_right.png",
            },
        },
    },
    "N64": {
        "base": "n64/base.png",
        "button_overlays": {
            0: "n64/a.png",
            1: "n64/b.png",
            8: "n64/z.png",
            9: "n64/z.png",
            11: "n64/start.png",
            6: "n64/l.png",
            7: "n64/r.png",
            # expand as needed depending on how your controller maps
        },
        "controller_name": "8BitDo 64 Bluetooth Controller",
        "x_axis": 0, "y_axis": 1,
        "stick_overlay": "n64/stick.png",
        "stick_center": (203, 92),  # where the stick base sits on your base image
        "stick_radius": 20,          # how far it can move
        "deadzone": 0.2,
        "c_buttons": {  # mapped via Z Axis and Z Rotation
            "up":    {"axis": 4, "direction": -1, "image": "n64/c_up.png"},
            "down":  {"axis": 4, "direction":  1, "image": "n64/c_down.png"},
            "left":  {"axis": 3, "direction": -1, "image": "n64/c_left.png"},
            "right": {"axis": 3, "direction":  1, "image": "n64/c_right.png"},
            "threshold": 0.5,
        },
        "hat_overlays": {  # d-pad via POV hat
            (0, 1):  "n64/up.png",
            (0, -1): "n64/down.png",
            (-1, 0): "n64/left.png",
            (1, 0):  "n64/right.png",
        },
    }

}
# ------------------------------------------------

def load_image(path: Path):
    return pygame.image.load(path).convert_alpha()

def main():

    parser = argparse.ArgumentParser(description="Controller Overlay")
    parser.add_argument(
        "--profile", choices=PROFILES.keys(), default="N64", help="Controller profile to use (NES, SNES, N64, etc.)"
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info for mapping discovery")
    args = parser.parse_args()

    profile = PROFILES[args.profile]
    BASE_IMAGE = profile["base"]
    BUTTON_OVERLAYS = profile.get("button_overlays", {})
    HAT_OVERLAYS = profile.get("hat_overlays", {})
    STICK_CENTER = profile.get("stick_center")
    STICK_RADIUS = profile.get("stick_radius", 0)
    DEADZONE = profile.get("deadzone", 0.15)
    STICK_OVERLAY_FILE = profile.get("stick_overlay")

    ASSETS_DIR = Path("assets")

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joysticks detected.")
        return

    joystick_index = 0
    found = False
    for i in range(pygame.joystick.get_count()):
        name = pygame.joystick.Joystick(i).get_name()
        if name.lower() == profile["controller_name"].lower():
            joystick_index = i
            found = True
            break
    if not found:
        print(f"Joystick named '{profile['controller_name']}' not found. Available devices:")
        for i in range(pygame.joystick.get_count()):
            print(f"  {i}: {pygame.joystick.Joystick(i).get_name()}")
        return

    joy = pygame.joystick.Joystick(joystick_index)
    joy.init()
    print(f"Using joystick: {joy.get_name()}")

    # Load base image
    base_path = ASSETS_DIR / BASE_IMAGE
    if not base_path.is_file():
        print("Base image not found:", base_path)
        return
    base_raw = pygame.image.load(str(base_path))
    w, h = base_raw.get_size()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Controller Overlay")
    base_img = base_raw.convert_alpha()

    # Load button overlays
    button_surfaces = {}
    for idx, fname in BUTTON_OVERLAYS.items():
        path = ASSETS_DIR / fname
        if path.is_file():
            button_surfaces[idx] = pygame.image.load(str(path)).convert_alpha()
        else:
            print(f"Warning: button overlay missing {path}")

    # Load hat overlays
    hat_surfaces = {}
    for hat, fname in HAT_OVERLAYS.items():
        path = ASSETS_DIR / fname
        if path.is_file():
            hat_surfaces[hat] = pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: hat overlay missing {path}")

    # Load C button overlays (N64 profile)
    cbutton_surfaces = {}
    cbutton_cfg = profile.get("c_buttons")
    if cbutton_cfg:
        for direction in ["up", "down", "left", "right"]:
            mapping = cbutton_cfg.get(direction)
            if mapping:
                path = ASSETS_DIR / mapping["image"]
                if path.is_file():
                    cbutton_surfaces[direction] = pygame.image.load(path).convert_alpha()
                else:
                    print(f"Warning: missing C button overlay: {path}")

    # load cbutton overlays
    axis_dpad_cfg = profile.get("axis_dpad")
    axis_dpad_surfaces = {}
    if axis_dpad_cfg:
        for key, fname in axis_dpad_cfg.get("overlays", {}).items():
            path = ASSETS_DIR / fname
            if path.is_file():
                axis_dpad_surfaces[key] = load_image(path)
            else:
                print(f"Warning: missing axis-dpad overlay: {path}")

    # Load stick overlay if defined
    stick_surf = None
    if STICK_CENTER and STICK_OVERLAY_FILE:
        path = ASSETS_DIR / STICK_OVERLAY_FILE
        if path.is_file():
            stick_surf = pygame.image.load(path).convert_alpha()
        else:
            print(f"Warning: stick overlay missing {path}")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif args.debug:
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"JOYBUTTONDOWN index={event.button}")
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"JOYBUTTONUP index={event.button}")
                elif event.type == pygame.JOYHATMOTION:
                    print(f"JOYHATMOTION hat={event.hat} value={event.value}")
                elif event.type == pygame.JOYAXISMOTION:
                    print(f"JOYAXISMOTION axis={event.axis} value={event.value:.3f}")

        overlays = []

        # Buttons
        for i in range(joy.get_numbuttons()):
            if joy.get_button(i) and i in button_surfaces:
                overlays.append(button_surfaces[i])

        # Hats
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

        # Axis-based D-pad (SNES-style)
        if axis_dpad_cfg and axis_dpad_surfaces:
            xi = axis_dpad_cfg.get("x_axis", 0)
            yi = axis_dpad_cfg.get("y_axis", 1)
            th = axis_dpad_cfg.get("threshold", 0.5)
            inv_y = axis_dpad_cfg.get("invert_y", False)

            x = joy.get_axis(xi)
            y = joy.get_axis(yi)
            if inv_y:
                y = -y

            left  = x <= -th
            right = x >=  th
            up    = y <= -th
            down  = y >=  th

            # Prefer diagonals if provided
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

        # --- C-buttons (Z axis, Z rotation) ---
        if "c_buttons" in profile:
            for direction, mapping in profile["c_buttons"].items():
                if direction not in ["up", "down", "left", "right"]:
                    continue
                axis_val = joy.get_axis(mapping["axis"])
                if mapping["direction"] == -1 and axis_val < -profile["c_buttons"]["threshold"]:
                    overlays.append(cbutton_surfaces[direction])
                elif mapping["direction"] == 1 and axis_val > profile["c_buttons"]["threshold"]:
                    overlays.append(cbutton_surfaces[direction])

        # Draw everything
        screen.fill((0, 0, 0))
        screen.blit(base_img, (0, 0))
        for surf in overlays:
            screen.blit(surf, (0, 0))

        # Draw analog stick overlay if defined
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
