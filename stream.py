import os
import pygame.camera
import pygame.image
import sys
import thread

class Camera:

    def __init__(self, width, height):
        print "Loading Camera..."
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        count = 1
        while len(cameras) < 1:
            cameras = pygame.camera.list_cameras()
            count += 1
        
        if len(cameras) < 1:
           print "Unable to load camera... Exiting!"
           sys.exit()
        else:
            print "Camera {0} loaded in {1} attempts.".format(cameras[0], count)
            
        self.width = width
        self.height = height
        self.webcam = pygame.camera.Camera(cameras[0], (self.width, self.height), "RGB")
        self.webcam.start()
    
    def get_dimensions(self):
        # grab first frame
        img = self.webcam.get_image()
        width = img.get_width()
        height = img.get_height()
        
        return (width, height)
        
    def start_display(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Brook Camera View")
        
    def refresh_display(self):
        # grab next frame
        img = self.webcam.get_image()
        # draw frame
        self.screen.blit(img, (0,0))
        pygame.display.flip()
    
    def stop(self):
        print "Exiting..."
        pygame.display.quit()
        self.webcam.stop()

class CameraRunner:
    
    def __init__(self, id):
        #id: int
        width = 640
        height = 480
        self.cam = Camera(width, height)
        print "Runner{0}: Stream dimensions are {1}.".format(id, self.cam.get_dimensions())
    
    def start(self):
        self.cam.start_display()
        while True :
            for e in pygame.event.get() :
                if e.type == pygame.QUIT :
                    self.cam.stop()
                    sys.exit()
            
            self.cam.refresh_display()
        
if __name__ == "__main__":
    os.environ['PYGAME_CAMERA'] = 'opencv'
    print "Starting Watcher..."
    
    # create a runner
    runner1 = CameraRunner(1)
    
    # create a thread for the camera
    runner1.start()
    
    while True:
        pass