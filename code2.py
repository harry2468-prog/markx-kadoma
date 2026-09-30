import os
import urllib.parse
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# =============================================================================
# 1. IMAGE ASSETS CONFIGURATION
# =============================================================================
IMAGES = {
    # Logos & National Crest
    "left_logo": "bigbulllogo.png",
    "right_logo": "ladybulllogo.png",
    "flag": "flagzim.webp",

    # The 3 Cars in a Row (Left, Center, Right)
    "car_left": "markx1.jpg",               # Car 1: Left Wing
    "car_center": "markx2.webp",            # Car 2: Center Car
    "car_right": "markx3.jpg",              # Car 3: Right Wing

    # Blazing Fire Textures
    "fire_floor": "blazingfire.webp",       # Fiery runway under the cars
    "fire_car": "blazingfire2.webp",        # Fire burst reflecting on bumpers & tires
}

# =============================================================================
# 2. CONTROL PANEL: SIZES, MESSAGE & YOUR EXACT COORDINATES
# =============================================================================
# --- UNIFORM CAR SIZING ---
CAR_WIDTH = 510       # Width for all 3 cars in pixels
CAR_HEIGHT = 290      # Height for all 3 cars in pixels

# --- REFLECTION CONTROLS ---
REFLECTION_INTENSITY = 0.85
REFLECTION_LENGTH = 0.45

# --- CAR 1 (LEFT WING) ---
CAR1_X = 110          # Horizontal position
CAR1_Y = 600          # Vertical position
REF1_X = 110          # Independent Reflection X
REF1_Y = 888          # Independent Reflection Y

# --- CAR 2 (CENTER CAR) ---
CAR2_X = (1748 - CAR_WIDTH) // 2   # Automatically centered: 619
CAR2_Y = 600          # Vertical position (Aligned with Left and Right)
REF2_X = CAR2_X       # Independent Reflection X
REF2_Y = 888          # Independent Reflection Y

# --- CAR 3 (RIGHT WING) ---
CAR3_X = 1748 - 110 - CAR_WIDTH    # Symmetrical Right position: 1128
CAR3_Y = 600          # Vertical position
REF3_X = CAR3_X       # Independent Reflection X
REF3_Y = 888          # Independent Reflection Y

# --- QR CODE EXACT POSITION (PLACED DIRECTLY AS IT IS, NO GOLD BOX) ---
QR_X = 1170           # Exact Horizontal position of the QR Code
QR_Y = 1780           # Exact Vertical position of the QR Code

# TARGET WHATSAPP REGISTRATION NUMBER & PRE-FILLED MESSAGE
WHATSAPP_NUMBER = "263779216474"   # +263 77 921 6474
WHATSAPP_MESSAGE = "Hi, I would like to register for Mark X edition"


# =============================================================================
# 3. ADVANCED FIRE-REFLECTION & BLENDING ENGINE
# =============================================================================
def load_img(path, size=None, rounded=False, radius=12):
    """Safely loads images, converts to RGBA, and resizes to exact target size."""
    if not path or not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGBA")
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        if rounded:
            mask = Image.new("L", img.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
            out = Image.new("RGBA", img.size, (0, 0, 0, 0))
            out.paste(img, (0, 0), mask=mask)
            return out
        return img
    except Exception as e:
        print(f"Notice: Could not load {path}: {e}")
        return None


def apply_fire_glow_on_car(car_img, fire_img, intensity_factor=1.0):
    """Reflects blazing fire glow onto the lower body of the car scaled by intensity."""
    if not fire_img or intensity_factor <= 0.0:
        return car_img

    w, h = car_img.size
    glow_h = int(h * 0.45)
    fire_part = fire_img.resize((w, glow_h), Image.Resampling.LANCZOS).convert("RGBA")
    car_lower = car_img.crop((0, h - glow_h, w, h))

    blended_lower = ImageChops.screen(car_lower.convert("RGB"), fire_part.convert("RGB")).convert("RGBA")

    max_alpha = int(210 * max(0.0, min(1.0, intensity_factor)))
    mask_1d = Image.new("L", (1, glow_h))
    mask_data = [int(max_alpha * (y / glow_h)) for y in range(glow_h)]
    mask_1d.putdata(mask_data)
    fade_mask = mask_1d.resize((w, glow_h), Image.Resampling.BILINEAR)

    result = car_img.copy()
    result.paste(blended_lower, (0, h - glow_h), mask=fade_mask)
    return result


def create_fire_mirror_reflection(car_img, fire_floor_img, length_factor=0.45, intensity_factor=0.85):
    """Generates the burning ground reflection modulated by length and intensity factors."""
    if intensity_factor <= 0.0:
        return None

    flipped = car_img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    ref_h = max(10, int(flipped.height * length_factor))
    flipped = flipped.crop((0, 0, flipped.width, ref_h))

    if fire_floor_img:
        fire_res = fire_floor_img.resize((flipped.width, ref_h), Image.Resampling.LANCZOS)
        blended_ref = ImageChops.screen(flipped.convert("RGB"), fire_res.convert("RGB")).convert("RGBA")
    else:
        blended_ref = flipped

    max_opacity = int(255 * max(0.0, min(1.0, intensity_factor)))
    grad_1d = Image.new("L", (1, ref_h))
    grad_data = [int(max_opacity * (1.0 - (y / ref_h))) for y in range(ref_h)]
    grad_1d.putdata(grad_data)
    gradient_mask = grad_1d.resize((flipped.width, ref_h), Image.Resampling.BILINEAR)

    r, g, b, orig_a = blended_ref.split()
    final_alpha = ImageChops.multiply(orig_a, gradient_mask)
    blended_ref.putalpha(final_alpha)
    return blended_ref


def place_fire_reflected_car(canvas, car_img, fire_floor_img, fire_body_img, 
                             car_x, car_y, ref_x, ref_y, 
                             intensity=0.85, length=0.45, label=""):
    """Composites a car with its intensity-controlled fire reflection at decoupled coordinates."""
    if not car_img:
        return

    glowing_car = apply_fire_glow_on_car(car_img, fire_body_img, intensity_factor=intensity)
    car_w, car_h = glowing_car.size
    draw = ImageDraw.Draw(canvas)

    # 1. Contact shadow under tires
    shadow_w = int(car_w * 0.92)
    shadow_h = 24
    shadow_x = car_x + (car_w - shadow_w) // 2
    draw.ellipse([(shadow_x, car_y + car_h - 12), (shadow_x + shadow_w, car_y + car_h + 12)], fill=(0, 0, 0, 240))

    # 2. Fire reflection at independent (ref_x, ref_y)
    reflection = create_fire_mirror_reflection(glowing_car, fire_floor_img, length_factor=length, intensity_factor=intensity)
    if reflection:
        canvas.paste(reflection, (ref_x, ref_y), mask=reflection)

    # 3. Main car placed on top
    canvas.paste(glowing_car, (car_x, car_y), mask=glowing_car)

    # 4. Optional Label
    if label:
        try:
            font = ImageFont.truetype("arialbd.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        ref_bottom = (ref_y + reflection.height) if reflection else (car_y + car_h)
        draw.text((car_x + (car_w // 2), ref_bottom + 14), label, fill=(245, 215, 127), font=font, anchor="mm")


# =============================================================================
# 4. MASTER FLYER GENERATION
# =============================================================================
def generate_master_flyer(output_filename="Team_Mark_X_Fire_Reflective.png"):
    W, H = 1748, 2480  # 300 DPI A5 Commercial Print
    canvas = Image.new("RGB", (W, H), color=(8, 8, 8))
    draw = ImageDraw.Draw(canvas)

    # Palette
    GOLD = (212, 175, 55)
    LIGHT_GOLD = (245, 215, 127)
    DARK_GOLD = (130, 100, 30)
    WHITE = (250, 250, 250)
    GRAY = (160, 160, 160)
    PANEL_BG = (16, 16, 16)

    # Fonts
    try:
        f_hero = ImageFont.truetype("arialbd.ttf", 85)
        f_sub = ImageFont.truetype("arialbd.ttf", 44)
        f_h2 = ImageFont.truetype("arialbd.ttf", 36)
        f_bold = ImageFont.truetype("arialbd.ttf", 28)
        f_body = ImageFont.truetype("arial.ttf", 26)
        f_small = ImageFont.truetype("arial.ttf", 22)
        f_tiny = ImageFont.truetype("arial.ttf", 19)
    except IOError:
        f_hero = f_sub = f_h2 = f_bold = f_body = f_small = f_tiny = ImageFont.load_default()

    # Outer Borders
    draw.rectangle([(25, 25), (W - 25, H - 25)], outline=GOLD, width=6)
    draw.rectangle([(38, 38), (W - 38, H - 38)], outline=DARK_GOLD, width=2)

    # -------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------
    bull_logo = load_img(IMAGES["left_logo"], (210, 210))
    if bull_logo:
        draw.ellipse([(70, 60), (290, 280)], outline=GOLD, width=4)
        canvas.paste(bull_logo, (75 + (210 - bull_logo.width)//2, 65 + (210 - bull_logo.height)//2), mask=bull_logo)
        draw.text((180, 295), "BIG BULLS", fill=LIGHT_GOLD, font=f_small, anchor="mm")

    lady_logo = load_img(IMAGES["right_logo"], (210, 210))
    if lady_logo:
        draw.ellipse([(W - 290, 60), (W - 70, 280)], outline=GOLD, width=4)
        canvas.paste(lady_logo, (W - 285 + (210 - lady_logo.width)//2, 65 + (210 - lady_logo.height)//2), mask=lady_logo)
        draw.text((W - 180, 295), "LADY BULLS", fill=LIGHT_GOLD, font=f_small, anchor="mm")

    zim_flag = load_img(IMAGES["flag"], (140, 85), rounded=True, radius=12)
    if zim_flag:
        flag_x = (W - zim_flag.width) // 2
        canvas.paste(zim_flag, (flag_x, 65), mask=zim_flag)
        draw.rounded_rectangle([(flag_x - 3, 62), (flag_x + zim_flag.width + 3, 65 + zim_flag.height + 3)], radius=14, outline=GOLD, width=3)

    draw.text((W // 2, 175), "★ AUTOMOTIVE & LIFESTYLE EXPERIENCE ★", fill=GRAY, font=f_small, anchor="mm")
    draw.text((W // 2, 235), "TEAM MARK X KADOMA", fill=GOLD, font=f_hero, anchor="mm")
    draw.text((W // 2, 305), "KADOMA CITY OF GOLD EDITION", fill=LIGHT_GOLD, font=f_sub, anchor="mm")
    draw.text((W // 2, 355), "BIG BULLS MEET IN THE MIDDLE", fill=WHITE, font=f_h2, anchor="mm")

    # Convoy Route Banner
    draw.rectangle([(80, 390), (W - 80, 448)], fill=PANEL_BG, outline=GOLD, width=2)
    draw.text((W // 2, 419), "ONE CITY • ONE LOVE • ONE FAMILY  |  HARARE • BULAWAYO • MUTARE • GWERU • KWEKWE ➔ KADOMA", fill=WHITE, font=f_bold, anchor="mm")

    # -------------------------------------------------------------
    # 3-CAR STAGE (APPLYING YOUR EXACT CAR & REFLECTION COORDINATES)
    # -------------------------------------------------------------
    stage_top = 465
    stage_h = 590
    draw.rectangle([(80, stage_top), (W - 80, stage_top + stage_h)], fill=(12, 12, 12), outline=DARK_GOLD, width=3)
    draw.text((W // 2, stage_top + 32), "OFFICIAL SHOWCASE: CITY OF GOLD FLEET", fill=LIGHT_GOLD, font=f_h2, anchor="mm")

    fire_floor = load_img(IMAGES["fire_floor"])
    fire_car = load_img(IMAGES["fire_car"])

    if fire_floor and REFLECTION_INTENSITY > 0.0:
        fire_bed = fire_floor.resize((W - 180, 100), Image.Resampling.LANCZOS)
        runway_opacity = int(160 * REFLECTION_INTENSITY)
        fire_mask = Image.new("L", fire_bed.size, runway_opacity)
        canvas.paste(fire_bed, (90, 840), mask=fire_mask)

    # 1. Car 1 (Left Wing)
    c1 = load_img(IMAGES["car_left"], size=(CAR_WIDTH, CAR_HEIGHT), rounded=True, radius=10)
    place_fire_reflected_car(
        canvas, c1, fire_floor, fire_car, 
        car_x=CAR1_X, car_y=CAR1_Y, 
        ref_x=REF1_X, ref_y=REF1_Y, 
        intensity=REFLECTION_INTENSITY, length=REFLECTION_LENGTH,
        label="STANCE PIMPED"
    )

    # 2. Car 3 (Right Wing)
    c3 = load_img(IMAGES["car_right"], size=(CAR_WIDTH, CAR_HEIGHT), rounded=True, radius=10)
    place_fire_reflected_car(
        canvas, c3, fire_floor, fire_car, 
        car_x=CAR3_X, car_y=CAR3_Y, 
        ref_x=REF3_X, ref_y=REF3_Y, 
        intensity=REFLECTION_INTENSITY, length=REFLECTION_LENGTH,
        label="GR SPORT TUNED"
    )

    # 3. Car 2 (Center Car)
    c2 = load_img(IMAGES["car_center"], size=(CAR_WIDTH, CAR_HEIGHT), rounded=True, radius=10)
    place_fire_reflected_car(
        canvas, c2, fire_floor, fire_car, 
        car_x=CAR2_X, car_y=CAR2_Y, 
        ref_x=REF2_X, ref_y=REF2_Y, 
        intensity=REFLECTION_INTENSITY, length=REFLECTION_LENGTH,
        label="GOLD EDITION HERO"
    )

    # -------------------------------------------------------------
    # EVENT DATE & VENUE BADGE
    # -------------------------------------------------------------
    event_top = 1075
    draw.rectangle([(80, event_top), (W - 80, event_top + 90)], fill=PANEL_BG, outline=GOLD, width=3)
    draw.text((W // 2, event_top + 45), "🗓️ 10 OCTOBER 2026 • SPEEDWAY KADOMA MIDDLE CITY 🏆🏁", fill=LIGHT_GOLD, font=f_h2, anchor="mm")

    # -------------------------------------------------------------
    # SCHEDULE & AWARDS (2-COLUMN CARDS)
    # -------------------------------------------------------------
    cards_top = 1185
    card_h = 390
    card_w = (W - 180) // 2

    # Left Card: SCHEDULE
    draw.rectangle([(80, cards_top), (80 + card_w, cards_top + card_h)], fill=(14, 14, 14), outline=DARK_GOLD, width=2)
    draw.text((80 + card_w // 2, cards_top + 40), "SCHEDULE", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    
    schedule_items = [
        "• SHOWCASE PARADE",
        "• CONTROLLED DEMOS",
        "• BRAAI CHILL",
        "• AWARDS CEREMONY",
        "• KADOMA MUSIC FESTIVAL",
        "• 14:00 - 15:00 Queens Hour (Ladies Only)"
    ]
    for idx, item in enumerate(schedule_items):
        draw.text((115, cards_top + 95 + (idx * 45)), item, fill=WHITE, font=f_body)

    # Right Card: AWARDS
    right_card_x = W - 80 - card_w
    draw.rectangle([(right_card_x, cards_top), (W - 80, cards_top + card_h)], fill=(14, 14, 14), outline=DARK_GOLD, width=2)
    draw.text((right_card_x + card_w // 2, cards_top + 40), "AWARDS", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    
    awards_items = [
        "• BEST MARK X BUILD",
        "• LOUD EXHAUST KING",
        "• CLEANEST RIDE & BEST CLUB DISPLAY",
        "• QUEEN OF THE TRACK (Best Female Owned)",
        "• LADY BULL SPIRIT — Most Stylish",
        "• GOLDEN TOUCH — Best Interior"
    ]
    for idx, item in enumerate(awards_items):
        draw.text((right_card_x + 35, cards_top + 95 + (idx * 45)), item, fill=WHITE, font=f_body)

    # -------------------------------------------------------------
    # ORGANISERS & TICKET FEES BADGE
    # -------------------------------------------------------------
    org_top = 1595
    draw.rectangle([(80, org_top), (W - 80, org_top + 180)], fill=PANEL_BG, outline=GOLD, width=2)
    draw.text((W // 2, org_top + 28), "ORGANISED BY", fill=LIGHT_GOLD, font=f_bold, anchor="mm")

    # Craig T
    draw.text((120, org_top + 70), "🏎️ CRAIG T —", fill=GOLD, font=f_bold)
    draw.text((325, org_top + 70), "Director, Craig Motors (Fast & Furious)", fill=WHITE, font=f_body)
    draw.text((120, org_top + 105), "🎟️ REGISTRATION FEE: TBA", fill=LIGHT_GOLD, font=f_small)

    # DJ Sir Clemmie Dee
    draw.text((W // 2 + 30, org_top + 70), "🎧 DJ SIR CLEMMIE DEE —", fill=GOLD, font=f_bold)
    draw.text((W // 2 + 395, org_top + 70), "Director, A 1 Soundz Ent", fill=WHITE, font=f_body)
    draw.text((W // 2 + 30, org_top + 105), "🎫 ADM FEE: TBA", fill=LIGHT_GOLD, font=f_small)

    # Hotline to +263 77 921 6474
    draw.text((W // 2, org_top + 148), "📞 OFFICIAL HOTLINE / WHATSAPP: +263 77 921 6474  |  0790 187 400", fill=WHITE, font=f_bold, anchor="mm")

    # -------------------------------------------------------------
    # BOTTOM ACTION GRID (STAMP + ROADMAP + DIRECT RAW QR CODE)
    # -------------------------------------------------------------
    bot_y = 1800

    # 1. Gate Stamp Area
    stamp_cx = 280
    stamp_cy = bot_y + 190
    stamp_r = 150
    draw.ellipse([(stamp_cx - stamp_r, stamp_cy - stamp_r), (stamp_cx + stamp_r, stamp_cy + stamp_r)], outline=GOLD, width=5)
    draw.ellipse([(stamp_cx - stamp_r + 12, stamp_cy - stamp_r + 12), (stamp_cx + stamp_r - 12, stamp_cy + stamp_r - 12)], outline=DARK_GOLD, width=2)
    draw.text((stamp_cx, stamp_cy - 40), "OFFICIAL", fill=GOLD, font=f_h2, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 5), "GATE STAMP", fill=WHITE, font=f_bold, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 45), "HERE", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 85), "[ VALID ENTRY ]", fill=GRAY, font=f_tiny, anchor="mm")

    # 2. Road Map Banner Card (Stops before the QR Code)
    map_x = 480
    map_w = QR_X - map_x - 40
    draw.rectangle([(map_x, bot_y), (map_x + map_w, bot_y + 380)], fill=PANEL_BG, outline=DARK_GOLD, width=2)
    draw.text((map_x + map_w // 2, bot_y + 50), "ROAD MAP CONNECTION", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    draw.text((map_x + map_w // 2, bot_y + 110), "🎵 KADOMA MUSIC FESTIVAL @ ODYSSEY", fill=GOLD, font=f_bold, anchor="mm")
    draw.text((map_x + map_w // 2, bot_y + 170), "Family & Friends Welcome", fill=WHITE, font=f_body, anchor="mm")
    draw.text((map_x + map_w // 2, bot_y + 215), "Mark X Family & Clubs Invited", fill=GRAY, font=f_small, anchor="mm")
    draw.text((map_x + map_w // 2, bot_y + 260), "Lady Bulls Queens Welcome", fill=LIGHT_GOLD, font=f_small, anchor="mm")
    draw.text((map_x + map_w // 2, bot_y + 320), "SPEEDWAY BAR KADOMA", fill=WHITE, font=f_bold, anchor="mm")

    # 3. DIRECT WHATSAPP QR CODE (RAW PLACEMENT - NO GOLDEN CONTAINER BOX)
    encoded_message = urllib.parse.quote(WHATSAPP_MESSAGE)
    qr_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=9, border=2)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Paste QR Code directly onto the canvas with NO golden box
    canvas.paste(qr_img, (QR_X, QR_Y))

    # Text placed directly below the raw QR code
    qr_cx = QR_X + (qr_img.width // 2)
    draw.text((qr_cx, QR_Y + qr_img.height + 25), "SCAN FOR WHATSAPP", fill=LIGHT_GOLD, font=f_bold, anchor="mm")
    draw.text((qr_cx, QR_Y + qr_img.height + 52), "Direct Line: 077 921 6474", fill=GRAY, font=f_tiny, anchor="mm")

    # -------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------
    draw.line([(80, H - 110), (W - 80, H - 110)], fill=GOLD, width=2)
    draw.text(
        (W // 2, H - 65),
        "#TEAMMARKX  •  #KADOMA  •  #CITYOFGOLD  •  10.10.2026  •  HOTLINE: +263 77 921 6474  •  ROAD TO KADOMA MUSIC FESTIVAL @ ODYSSEY",
        fill=GRAY,
        font=f_tiny,
        anchor="mm"
    )

    canvas.save(output_filename, dpi=(300, 300))
    print(f"\n[DONE] Flyer generated with raw QR code (no gold box): {output_filename}")


if __name__ == "__main__":
    generate_master_flyer()