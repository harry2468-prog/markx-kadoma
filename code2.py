import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def load_and_fit(image_path, target_size, rounded=False, radius=20):
    """Safely loads an image, converts it, and fits it within target_size."""
    if not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        if rounded:
            mask = Image.new("L", img.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
            output = Image.new("RGBA", img.size, (0, 0, 0, 0))
            output.paste(img, (0, 0), mask=mask)
            return output
        return img
    except Exception as e:
        print(f"Notice: Could not process {image_path}: {e}")
        return None

def create_master_flyer():
    # 300 DPI A5 Commercial Print Dimensions: 1748 x 2480 pixels
    W, H = 1748, 2480
    
    # 1. Base Luxury Canvas (Deep Metallic Onyx)
    canvas = Image.new("RGB", (W, H), color=(12, 12, 12))
    draw = ImageDraw.Draw(canvas)

    # 2. Color Palette
    GOLD = (212, 175, 55)
    LIGHT_GOLD = (245, 215, 127)
    DARK_GOLD = (130, 100, 30)
    WHITE = (250, 250, 250)
    GRAY = (160, 160, 160)
    PANEL_BG = (20, 20, 20)
    CARD_BORDER = (55, 45, 20)

    # 3. Typography (Windows Standard Fonts)
    try:
        f_hero = ImageFont.truetype("arialbd.ttf", 80)
        f_sub = ImageFont.truetype("arialbd.ttf", 46)
        f_h2 = ImageFont.truetype("arialbd.ttf", 36)
        f_body = ImageFont.truetype("arial.ttf", 30)
        f_bold = ImageFont.truetype("arialbd.ttf", 30)
        f_small = ImageFont.truetype("arial.ttf", 24)
        f_tiny = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        f_hero = f_sub = f_h2 = f_body = f_bold = f_small = f_tiny = ImageFont.load_default()

    # 4. Outer Borders & Corner Accents
    draw.rectangle([(25, 25), (W - 25, H - 25)], outline=GOLD, width=6)
    draw.rectangle([(38, 38), (W - 38, H - 38)], outline=DARK_GOLD, width=2)
    
    # Decorative Corner Notches
    for cx, cy in [(25, 25), (W - 25, 25), (25, H - 25), (W - 25, H - 25)]:
        dx = 80 if cx == 25 else -80
        dy = 80 if cy == 25 else -80
        draw.line([(cx, cy), (cx + dx, cy)], fill=LIGHT_GOLD, width=8)
        draw.line([(cx, cy), (cx, cy + dy)], fill=LIGHT_GOLD, width=8)

    # -------------------------------------------------------------
    # HEADER SECTION: LOGOS + TITLE
    # -------------------------------------------------------------
    # Left Emblem: bigbulllogo.png
    bull_logo = load_and_fit("bigbulllogo.png", (210, 210))
    if bull_logo:
        # Subtle glow ring
        draw.ellipse([(70, 60), (290, 280)], outline=GOLD, width=4)
        canvas.paste(bull_logo, (75 + (210 - bull_logo.width)//2, 65 + (210 - bull_logo.height)//2), mask=bull_logo)
        draw.text((180, 295), "BIG BULLS", fill=LIGHT_GOLD, font=f_small, anchor="mm")

    # Right Emblem: ladybulllogo.png
    lady_logo = load_and_fit("ladybulllogo.png", (210, 210))
    if lady_logo:
        draw.ellipse([(W - 290, 60), (W - 70, 280)], outline=GOLD, width=4)
        canvas.paste(lady_logo, (W - 285 + (210 - lady_logo.width)//2, 65 + (210 - lady_logo.height)//2), mask=lady_logo)
        draw.text((W - 180, 295), "LADY BULLS", fill=LIGHT_GOLD, font=f_small, anchor="mm")

    # Center: Zimbabwe Flag Badge
    zim_flag = load_and_fit("zimflag.jpeg", (130, 80), rounded=True, radius=12)
    if zim_flag:
        flag_x = (W - zim_flag.width) // 2
        canvas.paste(zim_flag, (flag_x, 65), mask=zim_flag)
        draw.rounded_rectangle([(flag_x - 3, 62), (flag_x + zim_flag.width + 3, 65 + zim_flag.height + 3)], radius=14, outline=GOLD, width=3)

    # Header Titles
    draw.text((W // 2, 175), "QRATEDX & SPEEDWAY KADOMA PRESENT", fill=GRAY, font=f_small, anchor="mm")
    draw.text((W // 2, 235), "TEAM MARK X KADOMA", fill=GOLD, font=f_hero, anchor="mm")
    draw.text((W // 2, 310), "CITY OF GOLD EDITION", fill=LIGHT_GOLD, font=f_sub, anchor="mm")
    draw.text((W // 2, 365), "★ BIG BULLS MEET IN THE MIDDLE ★", fill=WHITE, font=f_h2, anchor="mm")

    # Route Ribbon
    draw.rectangle([(80, 395), (W - 80, 455)], fill=PANEL_BG, outline=GOLD, width=2)
    draw.text((W // 2, 425), "NATIONWIDE CONVOY: HARARE • BULAWAYO • MUTARE • GWERU • KWEKWE ➔ KADOMA", fill=WHITE, font=f_bold, anchor="mm")

    # -------------------------------------------------------------
    # HERO SECTION: DUAL TOYOTA MARK X CAR SHOWCASE
    # -------------------------------------------------------------
    hero_card_top = 480
    hero_card_h = 580
    draw.rectangle([(80, hero_card_top), (W - 80, hero_card_top + hero_card_h)], fill=(16, 16, 16), outline=CARD_BORDER, width=3)

    # Showcase Title
    draw.text((W // 2, hero_card_top + 40), "OFFICIAL SHOWCASE: GRX120 & GRX130 FLEET", fill=LIGHT_GOLD, font=f_h2, anchor="mm")

    # Place Car 1 (toyotamarkx.webp) on left
    car1 = load_and_fit("toyotamarkx.webp", (720, 420), rounded=True, radius=18)
    if car1:
        canvas.paste(car1, (120, hero_card_top + 90), mask=car1)
        draw.rounded_rectangle([(120, hero_card_top + 90), (120 + car1.width, hero_card_top + 90 + car1.height)], radius=18, outline=DARK_GOLD, width=2)
        draw.text((120 + car1.width // 2, hero_card_top + 535), "POWER & STANCE", fill=GOLD, font=f_small, anchor="mm")

    # Place Car 2 (toyotamarkx2.webp) on right
    car2 = load_and_fit("toyotamarkx2.webp", (720, 420), rounded=True, radius=18)
    if car2:
        car2_x = W - 120 - car2.width
        canvas.paste(car2, (car2_x, hero_card_top + 90), mask=car2)
        draw.rounded_rectangle([(car2_x, hero_card_top + 90), (car2_x + car2.width, hero_card_top + 90 + car2.height)], radius=18, outline=DARK_GOLD, width=2)
        draw.text((car2_x + car2.width // 2, hero_card_top + 535), "GOLD EDITION PERFORMANCE", fill=GOLD, font=f_small, anchor="mm")

    # -------------------------------------------------------------
    # EVENT LOGISTICS CARD (MIDDLE)
    # -------------------------------------------------------------
    event_top = 1090
    draw.rectangle([(80, event_top), (W - 80, event_top + 340)], fill=PANEL_BG, outline=GOLD, width=3)
    draw.text((W // 2, event_top + 45), "EVENT DETAILS & SCHEDULE", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    draw.text((W // 2, event_top + 115), "DATE: SATURDAY, 10 OCTOBER 2026", fill=WHITE, font=f_sub, anchor="mm")
    draw.text((W // 2, event_top + 185), "VENUE: SPEEDWAY BAR, KADOMA", fill=GOLD, font=f_sub, anchor="mm")
    draw.text((W // 2, event_top + 250), "GATES OPEN: 09:00 AM  •  DRESS CODE: CLEAN FASHIONED", fill=WHITE, font=f_body, anchor="mm")
    draw.text((W // 2, event_top + 300), "Official Road Map to Kadoma Music Festival @ Odyssey", fill=GRAY, font=f_small, anchor="mm")

    # -------------------------------------------------------------
    # TROPHIES & HONOURS BADGE
    # -------------------------------------------------------------
    award_top = 1460
    draw.rectangle([(80, award_top), (W - 80, award_top + 350)], fill=(16, 16, 16), outline=DARK_GOLD, width=2)
    draw.text((W // 2, award_top + 40), "TROPHY CATEGORIES & COMPETITIONS", fill=LIGHT_GOLD, font=f_h2, anchor="mm")

    categories = [
        "🏆 Best Mark X Build (GRX120 to GRX130)   •   🔊 Loud Exhaust King",
        "💎 Lowest Stance Pimped  •  Cleanest Ride  •  Best Rims Display",
        "👑 Lady Bulls: Queen of the Track  •  Lady Bull Spirit (Most Stylish)",
        "✨ Golden Touch (Best Interior Showcase & Sound Demo)"
    ]
    for idx, cat in enumerate(categories):
        draw.text((W // 2, award_top + 105 + (idx * 55)), cat, fill=WHITE, font=f_body, anchor="mm")

    # -------------------------------------------------------------
    # BOTTOM ACTION GRID (STAMP + CONTACTS + QR CODE)
    # -------------------------------------------------------------
    bot_y = 1840

    # 1. LEFT: OFFICIAL GATE STAMP ZONE
    stamp_cx, stamp_cy = 300, bot_y + 190
    stamp_r = 150
    draw.ellipse([(stamp_cx - stamp_r, stamp_cy - stamp_r), (stamp_cx + stamp_r, stamp_cy + stamp_r)], outline=GOLD, width=5)
    draw.ellipse([(stamp_cx - stamp_r + 12, stamp_cy - stamp_r + 12), (stamp_cx + stamp_r - 12, stamp_cy + stamp_r - 12)], outline=DARK_GOLD, width=2)
    draw.text((stamp_cx, stamp_cy - 40), "OFFICIAL", fill=GOLD, font=f_h2, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 5), "GATE STAMP", fill=WHITE, font=f_bold, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 45), "HERE", fill=LIGHT_GOLD, font=f_h2, anchor="mm")
    draw.text((stamp_cx, stamp_cy + 85), "[ VALID ENTRY ]", fill=GRAY, font=f_tiny, anchor="mm")

    # 2. MIDDLE: ORGANISERS BLOCK
    contacts_x = 520
    draw.rectangle([(contacts_x, bot_y), (contacts_x + 680, bot_y + 380)], fill=PANEL_BG, outline=CARD_BORDER, width=2)
    draw.text((contacts_x + 340, bot_y + 40), "ORGANISERS & HOSTS", fill=LIGHT_GOLD, font=f_h2, anchor="mm")

    contacts = [
        ("Craig T (Director Craig Motors):", "0790 187 400"),
        ("DJ Sir Clemmie Dee (A1 Soundz):", "0773 730 063"),
        ("Mr Mapeta (Speedway Bar Host):", "0779 216 474"),
    ]
    for i, (name, phone) in enumerate(contacts):
        y_pos = bot_y + 95 + (i * 75)
        draw.text((contacts_x + 30, y_pos), name, fill=GOLD, font=f_small)
        draw.text((contacts_x + 30, y_pos + 32), f"Call / WhatsApp: {phone}", fill=WHITE, font=f_bold)

    # 3. RIGHT: HIGH-RES SCANNABLE QR CODE
    qr_box_x = W - 460
    qr_url = "https://wa.me/263790187400?text=Hello%20Team%20Mark%20X%20Kadoma%20Registration"
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=2)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    
    # QR Container
    draw.rectangle([(qr_box_x, bot_y), (W - 80, bot_y + 380)], fill=PANEL_BG, outline=GOLD, width=3)
    canvas.paste(qr_img, (qr_box_x + 28, bot_y + 25))
    draw.text((qr_box_x + 190, bot_y + 335), "SCAN TO REGISTER", fill=LIGHT_GOLD, font=f_bold, anchor="mm")
    draw.text((qr_box_x + 190, bot_y + 360), "Instant WhatsApp Pass", fill=GRAY, font=f_tiny, anchor="mm")

    # -------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------
    draw.line([(80, H - 120), (W - 80, H - 120)], fill=GOLD, width=2)
    draw.text((W // 2, H - 70), "#TeamMarkXKadoma  •  #CityOfGold  •  United  •  Powerful  •  Fearless Zimbabwe", fill=GRAY, font=f_body, anchor="mm")

    # Output file
    output_filename = "Team_Mark_X_Kadoma_Official_Flyer.png"
    canvas.save(output_filename, dpi=(300, 300))
    print(f"\n[SUCCESS] Master flyer generated and saved to: {output_filename}")

if __name__ == "__main__":
    create_master_flyer()