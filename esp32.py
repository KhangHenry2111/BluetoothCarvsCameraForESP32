"""
In trạng thái tay cầm Xbox ra terminal (cập nhật tại chỗ).
Chạy:  python xbox_test.py
Thoát: Ctrl+C
"""
import time
import pygame

DEADZONE = 0.12
REFRESH = 0.05  # 20 lần/giây

# Tên nút theo mapping Xbox 360 trên Windows (SDL2)
BUTTONS = ["A", "B", "X", "Y", "LB", "RB", "Back", "Start", "L3", "R3"]


def dz(v):
    return 0.0 if abs(v) < DEADZONE else v


def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("Không thấy tay cầm. Cắm tay cầm rồi chạy lại.")
        return

    pad = pygame.joystick.Joystick(0)
    print(f"Tay cầm : {pad.get_name()}")
    print(f"Trục    : {pad.get_numaxes()} | Nút: {pad.get_numbuttons()} | Hat: {pad.get_numhats()}")
    print("Gạt cần / bấm nút để xem. Ctrl+C để thoát.\n")

    try:
        while True:
            pygame.event.pump()

            lx, ly = dz(pad.get_axis(0)), dz(pad.get_axis(1))
            rx, ry = dz(pad.get_axis(2)), dz(pad.get_axis(3))

            # Cò: trục 4/5 chạy từ -1 (thả) đến +1 (bóp hết) -> đổi sang 0..1
            lt = (pad.get_axis(4) + 1) / 2 if pad.get_numaxes() > 4 else 0.0
            rt = (pad.get_axis(5) + 1) / 2 if pad.get_numaxes() > 5 else 0.0

            hat = pad.get_hat(0) if pad.get_numhats() > 0 else (0, 0)

            pressed = [
                BUTTONS[i] if i < len(BUTTONS) else f"B{i}"
                for i in range(pad.get_numbuttons())
                if pad.get_button(i)
            ]

            line = (
                f"L({lx:+.2f},{-ly:+.2f}) "
                f"R({rx:+.2f},{-ry:+.2f}) "
                f"LT={lt:.2f} RT={rt:.2f} "
                f"DPad={hat} "
                f"Nút={','.join(pressed) or '-':<14}"
            )
            print(line, end="\r", flush=True)
            time.sleep(REFRESH)

    except KeyboardInterrupt:
        print("\nĐã thoát.")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()