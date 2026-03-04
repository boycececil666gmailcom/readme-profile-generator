from PIL import Image, ImageDraw
import os

os.makedirs('assets', exist_ok=True)

sizes = [16, 32, 48, 64, 128, 256]
imgs = []

BG     = (13,  17,  23,  255)
DOC    = (240, 246, 252, 255)
FOLD   = (240, 136,  62, 255)
LINE   = (139, 148, 158, 200)
SHADOW = (0,   0,   0,   80)

for sz in sizes:
    img = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    r = max(3, sz // 7)
    d.rounded_rectangle([0, 0, sz-1, sz-1], radius=r, fill=BG)

    dm   = max(2, sz * 3 // 16)
    fold = max(4, sz // 4)

    if sz >= 32:
        d.polygon([(dm+2, dm+2), (sz-dm-fold+2, dm+2),
                   (sz-dm+2, dm+fold+2), (sz-dm+2, sz-dm+2), (dm+2, sz-dm+2)],
                  fill=SHADOW)

    d.polygon([(dm, dm), (sz-dm-fold, dm),
               (sz-dm, dm+fold), (sz-dm, sz-dm), (dm, sz-dm)],
              fill=DOC)

    d.polygon([(sz-dm-fold, dm), (sz-dm-fold, dm+fold), (sz-dm, dm+fold)],
              fill=FOLD)

    d.line([(sz-dm-fold, dm), (sz-dm, dm+fold)],
           fill=(200, 100, 30, 180), width=max(1, sz//64))

    if sz >= 32:
        lx  = dm + max(2, sz // 12)
        ly  = dm + fold + max(2, sz // 12)
        lh  = max(1, sz // 20)
        gap = max(2, sz // 14)
        mw  = sz - dm - lx - max(2, sz // 12)
        for i, frac in enumerate([1.0, 0.75, 0.5]):
            y0 = ly + i * (lh + gap)
            y1 = y0 + lh
            if y1 < sz - dm - 2:
                d.rectangle([lx, y0, lx + int(mw * frac), y1], fill=LINE)

    imgs.append(img)

imgs[0].save('assets/icon.ico', format='ICO',
             sizes=[(s, s) for s in sizes],
             append_images=imgs[1:])
print('Icon saved: assets/icon.ico')
