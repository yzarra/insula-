import pygame
import os

class Customizer:
    # base dimensions for scaling
    BASE_WIDTH = 1300
    BASE_HEIGHT = 1900
    SCALE_MULTIPLIER = 1.3

    # resource arrays
    SKIN_NAMES       = ["Black.png", "Brown.png", "Tan.png", "White.png"]
    SKIN_PATH        = os.path.join("assets", "characters", "mc", "skins")
    SWIMWEAR_OUTFITS = ["Baywatch.png", "Leopard.png", "Blue.png", "Glitter.png", "Gold.png", "Bandeau.png"]
    EVERYDAY_OUTFITS = ["Milf.png", "Jorts.png", "Underboob.png"]
    OUTFIT_PATHS     = [
        os.path.join("assets", "characters", "mc", "outfits", "swimsuits"),
        os.path.join("assets", "characters", "mc", "outfits", "everyday")
    ]
    HAIR_COLORS      = ["Black", "Brown", "Red", "Honey", "Platinum"]
    HAIR_STYLES      = ["Straight.png", "Blowout.png", "HalfUp.png", "Braids.png", "Bob.png", "Buns.png"]
    HAIR_PATH        = os.path.join("assets", "characters", "mc", "hairs")
    NOSE_SHAPES      = ["Small.png", "Wide.png", "Angular.png"]
    NOSE_PATH        = os.path.join("assets", "characters", "mc", "face", "Nose")
    LIP_SHAPES       = ["Big", "Med", "Thin"]
    LIP_COLORS       = ["RumRaisin.png", "PillowTalk.png", "Bubblegum.png", "Berry.png"]
    LIP_PATH         = os.path.join("assets", "characters", "mc", "face", "Mouth")
    EYE_SHAPES       = ["Sultry", "Doe", "Cat"]
    EYE_COLORS       = ["Brown.png", "Green.png", "Blue.png"]
    EYE_PATH         = os.path.join("assets", "characters", "mc", "face", "Eyes")
    BROW_STYLES      = ["Thin.png", "Thick.png", "Cunt.png", "None"]
    BROW_PATH        = os.path.join("assets", "characters", "mc", "face", "Brows")

    def __init__(self):
        pygame.init()

        # instance variables
        self.running = True
        self.screen_info = pygame.display.Info()
        self.screenW, self.screenH = self.screen_info.current_w, self.screen_info.current_h
        self.screen = pygame.display.set_mode((self.screenW, self.screenH), pygame.RESIZABLE)
        pygame.display.set_caption("Customizer")
        self.clock = pygame.time.Clock()

        # load background
        bg_path = os.path.join("assets", "backgrounds", "DressingRoom.png")
        self.background = pygame.image.load(bg_path).convert()

        # font & colours
        self.font = pygame.font.Font(None, 24)
        self.white, self.orange = (255,255,255), (240,182,144)

        # exit button
        self.exit_btn = pygame.Rect(self.screenW - 90, 10, 80, 30)

        # current indices
        self.skin_idx    = 0
        self.cat_idx     = 0  # 0 = swim, 1 = everyday
        self.outfit_idx  = 0
        self.hair_color  = 0
        self.hair_style  = 0
        self.nose_idx    = 0
        self.lip_shape   = 0
        self.lip_color   = 0
        self.eye_shape   = 0
        self.eye_color   = 0
        self.brow_style  = 0

        # load layer images
        self.labels = {}  # name → pygame.Surface
        for name in ("skin","outfit","hair","nose","lip","eye","brow"):
            self.labels[name] = None

        # create UI buttons
        self.buttons = []
        self._init_buttons()

    def _init_buttons(self):
        # left panel: styles
        y = 80
        for text, cb in [
            ("Hair Style", lambda: self._cycle("hair_style",   self.HAIR_STYLES)),
            ("Nose Shape", lambda: self._cycle("nose_idx",     self.NOSE_SHAPES)),
            ("Lip Shape",  lambda: self._cycle("lip_shape",    self.LIP_SHAPES)),
            ("Eye Shape",  lambda: self._cycle("eye_shape",    self.EYE_SHAPES)),
            ("Brows",      lambda: self._cycle("brow_style",   self.BROW_STYLES))
        ]:
            rect = pygame.Rect(10, y, 180, 30);  y += 40
            self.buttons.append((rect, text, cb))

        # right panel: outfits & categories
        y = 80
        for text, cb in [
            ("Category",   lambda: self._cycle("cat_idx",    [0,1])),
            ("Next Outfit",lambda: self._cycle("outfit_idx",
                                 self.SWIMWEAR_OUTFITS if self.cat_idx==0 else self.EVERYDAY_OUTFITS))
        ]:
            rect = pygame.Rect(self.screenW - 190, y, 180, 30);  y += 40
            self.buttons.append((rect, text, cb))

        # color buttons
        y = 80 + 5*40
        for text, cb in [
            ("Skin Tone",    lambda: self._cycle("skin_idx",   self.SKIN_NAMES)),
            ("Hair Color",   lambda: self._cycle("hair_color", self.HAIR_COLORS)),
            ("Lipstick",     lambda: self._cycle("lip_color",  self.LIP_COLORS)),
            ("Eye Color",    lambda: self._cycle("eye_color",  self.EYE_COLORS))
        ]:
            rect = pygame.Rect(10, y, 180, 30);  y += 40
            self.buttons.append((rect, text, cb))

    def _cycle(self, attr, options):
        # increment index and reload layers
        val = getattr(self, attr)
        val = (val + 1) % len(options)
        setattr(self, attr, val)
        self._reload_layers()

    def _reload_layers(self):
        # build full paths and load images
        # skin
        p = os.path.join(self.SKIN_PATH, self.SKIN_NAMES[self.skin_idx])
        self.labels["skin"]   = pygame.image.load(p).convert_alpha()
        # outfit
        path = self.OUTFIT_PATHS[self.cat_idx]
        fname = (self.SWIMWEAR_OUTFITS if self.cat_idx==0 else self.EVERYDAY_OUTFITS)[self.outfit_idx]
        self.labels["outfit"] = pygame.image.load(os.path.join(path, fname)).convert_alpha()
        # hair
        hairdir = self.HAIR_COLORS[self.hair_color]
        hairfile = self.HAIR_STYLES[self.hair_style]
        self.labels["hair"]   = pygame.image.load(os.path.join(self.HAIR_PATH, hairdir, hairfile)).convert_alpha()
        # nose
        skinfolder = self.SKIN_NAMES[self.skin_idx].replace(".png","")
        self.labels["nose"]   = pygame.image.load(os.path.join(self.NOSE_PATH, skinfolder, self.NOSE_SHAPES[self.nose_idx])).convert_alpha()
        # lip
        ldir = self.LIP_SHAPES[self.lip_shape]
        lfile = self.LIP_COLORS[self.lip_color]
        self.labels["lip"]    = pygame.image.load(os.path.join(self.LIP_PATH, ldir, lfile)).convert_alpha()
        # eye
        edir = self.EYE_SHAPES[self.eye_shape]
        efile = self.EYE_COLORS[self.eye_color]
        self.labels["eye"]    = pygame.image.load(os.path.join(self.EYE_PATH, edir, efile)).convert_alpha()
        # brow
        bfile = self.BROW_STYLES[self.brow_style]
        if bfile == "None":
            self.labels["brow"] = None
        else:
            self.labels["brow"] = pygame.image.load(os.path.join(self.BROW_PATH, bfile)).convert_alpha()

    def _draw_background(self):
        # scale & blit dressing room bg
        bg = pygame.transform.scale(self.background, (self.screenW, self.screenH))
        self.screen.blit(bg, (0,0))

    def _draw_ui(self):
        # exit button
        pygame.draw.rect(self.screen, self.orange, self.exit_btn)
        ex = self.font.render("Exit", True, self.white)
        self.screen.blit(ex, ex.get_rect(center=self.exit_btn.center))

        # draw all other buttons
        for rect, text, _ in self.buttons:
            pygame.draw.rect(self.screen, self.orange, rect)
            surf = self.font.render(text, True, self.white)
            self.screen.blit(surf, surf.get_rect(center=rect.center))

    def _draw_character(self):
        # compute scale factor & target size
        scale = min(self.screenW/self.BASE_WIDTH, self.screenH/self.BASE_HEIGHT) * self.SCALE_MULTIPLIER
        w, h = int(self.BASE_WIDTH*scale), int(self.BASE_HEIGHT*scale)
        x = (self.screenW - w)//2
        y = (self.screenH - h)//15
        
        for layer in ["skin","outfit","hair","nose","lip","eye","brow"]:
            img = self.labels[layer]
            if img:
                img_scaled = pygame.transform.smoothscale(img, (w,h))
                self.screen.blit(img_scaled, (x,y))

    def _handle_event(self, evt):
        if evt.type == pygame.QUIT:
            self.running = False
        elif evt.type == pygame.VIDEORESIZE:
            self.screenW, self.screenH = evt.w, evt.h
            self.screen = pygame.display.set_mode((self.screenW, self.screenH), pygame.RESIZABLE)
            self.exit_btn.topleft = (self.screenW-90,10)
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            # exit?
            if self.exit_btn.collidepoint(evt.pos):
                self.running = False
            # other buttons?
            for rect, _, cb in self.buttons:
                if rect.collidepoint(evt.pos):
                    cb()

    def overall(self):
        # prime layers once
        self._reload_layers()

        # main loop
        while self.running:
            for evt in pygame.event.get():
                self._handle_event(evt)

            self._draw_background()
            self._draw_character()
            self._draw_ui()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def get_character(self):
        # return a simple dict of choices
        return {
            "skin":    self.SKIN_NAMES[self.skin_idx],
            "category": self.cat_idx,
            "outfit":  self.outfit_idx,
            "hair":    (self.HAIR_COLORS[self.hair_color], self.HAIR_STYLES[self.hair_style]),
            "nose":    self.NOSE_SHAPES[self.nose_idx],
            "lip":     (self.LIP_SHAPES[self.lip_shape], self.LIP_COLORS[self.lip_color]),
            "eye":     (self.EYE_SHAPES[self.eye_shape], self.EYE_COLORS[self.eye_color]),
            "brow":    self.BROW_STYLES[self.brow_style]
        }
