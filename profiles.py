"""
profiles.py

Controller profiles.
"""

PROFILES = {
    "NES": {
        "base": "nes/base.png",
        "button_overlays": {2: "nes/b.png", 3: "nes/a.png", 8: "nes/select.png", 9: "nes/start.png"},
        "console": "NES",
        "controller_name": "JC-W01U",
        "hat_overlays": {
            (0, 1): "nes/up.png",
            (0, -1): "nes/down.png",
            (-1, 0): "nes/left.png",
            (1, 0): "nes/right.png",
        },
    },
    "NES_SNES_Classic": {
        "base": "nes/base.png",
        "button_overlays": {
            0: "nes/b.png",
            1: "nes/turbo_b.png",
            2: "nes/a.png",
            3: "nes/turbo_a.png",
            8: "nes/select.png",
            9: "nes/start.png",
        },
        "console": "NES",
        "controller_name": "JC-W01U",
        "hat_overlays": {
            (0, 1): "nes/up.png",
            (0, -1): "nes/down.png",
            (-1, 0): "nes/left.png",
            (1, 0): "nes/right.png",
        },
    },
    "SNES_Classic": {
        "base": "snes/base.png",
        "button_overlays": {
            0: "snes/y.png",
            1: "snes/x.png",
            2: "snes/b.png",
            3: "snes/a.png",
            4: "snes/l.png",
            5: "snes/r.png",
            8: "snes/select.png",
            9: "snes/start.png",
        },
        "console": "SNES",
        "controller_name": "JC-W01U",
        "hat_overlays": {
            (0, 1): "snes/up.png",
            (0, -1): "snes/down.png",
            (-1, 0): "snes/left.png",
            (1, 0): "snes/right.png",
        },
    },
    "SNES_OEM": {
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
        "console": "SNES",
        "controller_name": "SNES PC Game Pad",
        "axes": {
            "dpad": {
                "x_axis": 0,
                "y_axis": 1,
                "threshold": 0.5,
                "overlays": {
                    "left": "snes/left.png",
                    "right": "snes/right.png",
                    "up": "snes/up.png",
                    "down": "snes/down.png",
                },
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
        },
        "console": "N64",
        "controller_name": "8BitDo 64 Bluetooth Controller",
        "axes": {
            "l_stick": {
                "x_axis": 0,
                "y_axis": 1,
                "overlay": "n64/stick.png",
                "center": (203, 92),
                "radius": 20,
                "deadzone": 0.2,
            },
            "c_buttons": {
                "up": {"axis": 4, "direction": -1, "overlay": "n64/c_up.png"},
                "down": {"axis": 4, "direction": 1, "overlay": "n64/c_down.png"},
                "left": {"axis": 3, "direction": -1, "overlay": "n64/c_left.png"},
                "right": {"axis": 3, "direction": 1, "overlay": "n64/c_right.png"},
                "threshold": 0.5,
            },
        },
        "hat_overlays": {
            (0, 1): "n64/up.png",
            (0, -1): "n64/down.png",
            (-1, 0): "n64/left.png",
            (1, 0): "n64/right.png",
        },
    },
    "PSX": {
        "base": "psx/base.png",
        "button_overlays": {
            2: "psx/square.png",
            0: "psx/cross.png",
            1: "psx/circle.png",
            3: "psx/triangle.png",
            9: "psx/l1.png",
            10: "psx/r1.png",
            4: "psx/select.png",
            6: "psx/start.png",
            11: "psx/up.png",
            12: "psx/down.png",
            13: "psx/left.png",
            14: "psx/right.png",
            7: "psx/l_thumb.png",
            8: "psx/r_thumb.png",
        },
        "console": "PSX",
        "controller_name": "PS4 Controller",
        "axes": {
            "l_stick": {
                "x_axis": 0,
                "y_axis": 1,
                "overlay": "psx/stick.png",
                "center": (199, 121),
                "radius": 15,
                "deadzone": 0.2,
            },
            "r_stick": {
                "x_axis": 2,
                "y_axis": 3,
                "overlay": "psx/stick.png",
                "center": (315, 121),
                "radius": 15,
                "deadzone": 0.2,
            },
            "triggers": {
                "x_axis": 4,
                "y_axis": 5,
                "threshold": 0.85,
                "overlays": {
                    "r2": "psx/r2.png",
                    "l2": "psx/l2.png",
                },
            },
        },
    },
}
