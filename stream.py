from multiprocessing import Process
import os
import pygame.camera
import pygame.image
import sys
import thread

class Camera:

    def __init__(self, camera, width, height, id):
        self.width = width
        self.height = height
        self.id = id
        self.webcam = pygame.camera.Camera(camera, (self.width, self.height), "RGB")
        self.webcam.start()

    def get_dimensions(self):
        # grab first frame
        img = self.webcam.get_image()
        width = img.get_width()
        height = img.get_height()

        return (width, height)

    def start_display(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Camera{0}: Brook Camera View".format(self.id))

    def refresh_display(self):
        # grab next frame
        img = self.webcam.get_image()
        # draw frame
        self.screen.blit(img, (0,0))
        pygame.display.flip()

    def stop(self):
        print "Camera{0}: Exiting...".format(self.id)
        pygame.display.quit()
        self.webcam.stop()

class CameraRunner:

    def __init__(self, id, camera):
        print "Runner{0}: Loading camera {1}".format(id, camera)
        width = 640
        height = 480
        self.cam = Camera(camera, width, height, id)
        print "Runner{0}: Stream dimensions are {1}.".format(id, self.cam.get_dimensions())
        self.process = Process(target=self.refresh, args=())

    def start(self):
        self.process.start()

    def refresh(self):
        self.cam.start_display()
        while True :
            for e in pygame.event.get() :
                if e.type == pygame.QUIT :
                    self.cam.stop()
                    sys.exit()

            self.cam.refresh_display()

def LoadCameras(count):
    print "Main: Loading Camera..."
    pygame.camera.init()
    cameras = pygame.camera.list_cameras()
    counter = 1
    while len(cameras) < count:
        cameras = pygame.camera.list_cameras()
        counter += 1
    if len(cameras) < count:
        print "Main: Unable to load {0} cameras... Exiting!".format(count)
        sys.exit()
    else:
        print "Main: Loaded {0} cameras {0} in {1} attempts.".format(count, cameras, counter)

    return cameras

if __name__ == "__main__":
    os.environ['PYGAME_CAMERA'] = 'opencv'
    print "Main: Starting Watcher..."

    cameras = LoadCameras(2)

    # create a runner
    runner1 = CameraRunner(1, cameras[0])
    runner2 = CameraRunner(2, cameras[1])

    # create a thread for the camera
    runner1.start()
    runner2.start()
    runner1.process.join()
    runner2.process.join()
