from PIL import Image, ImageSequence

BG_PATH  = "assets/pond.png"
KOI_PATH = "koi/koi.gif"
OUT_PATH = "koi/koi_pond.gif"

# Set to True ONLY if the koi.gif has a solid background colour (not transparent).
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

def cover(bg, size):
    """Scale the pond to fill the GIF size and crop the overflow, so it never stretches."""
    tw, th = size
    scale = max(tw / bg.width, th / bg.height)
    nw, nh = round(bg.width * scale), round(bg.height * scale)
    bg = bg.resize((nw, nh), Image.NEAREST)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return bg.crop((left, top, left + tw, top + th))

bg = Image.open(BG_PATH).convert("RGBA")
koi = Image.open(KOI_PATH)
duration = koi.info.get("duration", 100)
print("koi.gif size:", koi.size, "frames:", getattr(koi, "n_frames", 1))

pond = cover(bg, koi.size)
frames = []
for f in ImageSequence.Iterator(koi):
    f = f.convert("RGBA")
    if KEY_OUT_BACKGROUND:
        f = key_out(f)
    merged = Image.alpha_composite(pond, f)
    frames.append(merged.convert("P", palette=Image.ADAPTIVE))

frames[0].save(OUT_PATH, save_all=True, append_images=frames[1:],
               duration=duration, loop=0, disposal=2, optimize=False)
print("Saved", OUT_PATH)
