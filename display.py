#!/usr/bin/env python3

class display(object):
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.window = sdl2.ext.Window("Slam", size=(W,H), position=(-500,-500))
        self.window.show()

    def draw(self, img):
        # junk
        events = sdl2.ext.get_events()
        for event in envents:
            if event.type == sdl2.SDL_QUIT:
                exit(0)
        
        # draw
        surf = sdl2.ext.pixels2d(window.get_surface())
        surf[:, :, 0:3] = img.swapaxes(0,1)[:, :, 0]

        # blit
        self.window.refresh()



