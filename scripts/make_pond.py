from PIL import Image, ImageSequence

BG_PATH, KOI_PATH, OUT_PATH = "assets/pond_square.png", "koi/koi.gif", "koi/koi_pond.gif"

koi = Image.open(KOI_PATH)
size = koi.size
bg = Image.open(BG_PATH).convert("RGBA").resize(size, Image.NEAREST)

comp = [Image.alpha_composite(bg, f.convert("RGBA")).convert("RGB")
        for f in ImageSequence.Iterator(koi)]

# one shared palette so colours don't flicker between frames
samples = comp[::10]
sheet = Image.new("RGB", (size[0], size[1] * len(samples)))
for i, s in enumerate(samples):
    sheet.paste(s, (0, size[1] * i))
pal = sheet.quantize(colors=200, method=Image.MEDIANCUT, dither=Image.NONE)

frames = [c.quantize(palette=pal, dither=Image.NONE) for c in comp]
frames[0].save(OUT_PATH, save_all=True, append_images=frames[1:],
               duration=koi.info.get("duration", 70), loop=0, disposal=1, optimize=True)
print("Saved", OUT_PATH, len(frames), "frames")
