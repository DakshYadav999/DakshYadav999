
from PIL import Image, ImageSequence

BG_PATH  = "assets/pond.png"
KOI_PATH = "koi/koi.gif"
OUT_PATH = "koi/koi_pond.gif"

# Set to True ONLY if the koi.gif has a solid background colour (not transparent).
# It makes the colour of the top-left pixel transparent so the pond shows through.
KEY_OUT_BACKGROUND = False
TOLERANCE = 12

def key_out(frame):
    px = frame.load()
    key = px[0, 0][:3]
    w, h = frame.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if abs(r-key[0]) <= TOLERANCE and abs(g-key[1]) <= TOLERANCE and abs(b-key[2]) <= TOLERANCE:
                px[x, y] = (r, g, b, 0)
    return frame

bg = Image.open(BG_PATH).convert("RGBA")
koi = Image.open(KOI_PATH)
duration = koi.info.get("duration", 100)

frames = []
for f in ImageSequence.Iterator(koi):
    f = f.convert("RGBA")
    if KEY_OUT_BACKGROUND:
        f = key_out(f)
    pond = bg.resize(f.size, Image.NEAREST)        # NEAREST keeps pixel art crisp
    merged = Image.alpha_composite(pond, f)
    frames.append(merged.convert("P", palette=Image.ADAPTIVE))

frames[0].save(OUT_PATH, save_all=True, append_images=frames[1:],
               duration=duration, loop=0, disposal=2, optimize=False)
print("Saved", OUT_PATH)
