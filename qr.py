#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import zbar
import config
import pygame
from pygame import camera
from PIL import Image
from qrtools import QR


def get_qr_content(with_gui=False, manual_detect=False):

    screen = None
    detected = False
    camera.init()
    if not camera.list_cameras():
        print("No camera detected!")
        sys.exit(-1)
    cam = camera.Camera(camera.list_cameras()[config.camera_number-1])
    size = cam.get_size()
    width, height = size

    if not manual_detect:
        sys.stdout.write("QR detection started, wait several seconds...")
        sys.stdout.flush()
        cam.start()

        if with_gui:
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("Check QR recognize")
    else:
        with_gui = True
        print("QR detection through GUI, press any key when green line flash")

    data = 0
    while not detected:
        try:

            if manual_detect:
                qr = QR()
                qr.decode_webcam()
                data = qr.data

            else:
                img = cam.get_image()

                # we can use file buffer for recognition
                # pygame.image.save(img, "file.jpg")
                # pil_string_image = Image.open("file.jpg").convert('L').tostring()

                pygame_img = pygame.image.tostring(img, 'RGB', False)
                pil_string_image = Image.fromstring(
                    'RGB', size, pygame_img).convert('L').tostring()

                if with_gui:
                    screen.blit(img, (0, 0))
                    pygame.display.flip()  # display update

                zbar_image = zbar.Image(
                    width, height, 'Y800', pil_string_image)

                scanner = zbar.ImageScanner()
                scanner.parse_config('enable')
                data = scanner.scan(zbar_image)

                sys.stdout.write('.')
                sys.stdout.flush()

                for qr in zbar_image:
                    if data:
                        print("Additional QR recognized!")
                    data = qr.data

            if data:
                print("\nRecognized: `{}`".format(data))
                detected = True

        except Exception as e:
            print("Error! " + str(e))
        finally:
            time.sleep(config.qr_scan_waiting)

    if not manual_detect:
        pygame.display.quit()
        cam.stop()

    return 0 if data == "NULL" else data


# through Zbar recognizer
def get_content_with_gui_manual():
    return get_qr_content(True, True)


# show in Pygame window
def get_content_with_gui():
    return get_qr_content(True, False)


# do not show GUI
def get_content_no_gui():
    return get_qr_content(False, False)
