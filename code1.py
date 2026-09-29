import os
from PIL import Image, ImageDraw, ImageFont

def create_event_flyer(output_filename="mark_x_kadoma_flyer.png"):
    # A5 size at 300 DPI for sharp print quality: 1748 x 2480 pixels
    width = 1748
    height = 2480
    
    # 1. Create Base Image with Luxury Dark Background
    img = Image.new("RGB", (width, height), color=(15, 15, 15))
    draw = ImageDraw.Draw(img)
    
    # 2. Colors
    GOLD_PRIMARY = (212, 175, 55)
    GOLD_LIGHT = (255, 223, 128)
    WHITE = (245, 245, 245)
    MUTED_GRAY = (140, 140, 140)
    DARK_CARD = (25, 25, 25)
    
    # 3. Fonts Setup (Falls back to default if TTF not found)
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 95)
        font_subtitle = ImageFont.truetype("arialbd.ttf", 55)
        font_section = ImageFont.truetype("arialbd.ttf", 45)
        font_body = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except IOError:
        font_title = font_subtitle = font_section = font_body = font_small = ImageFont.load_default()

    # 4. Outer Gold Border
    border_margin = 40
    draw.rectangle(
        [(border_margin, border_margin), (width - border_margin, height - border_margin)],
        outline=GOLD_PRIMARY,
        width=8
    )
    draw.rectangle(
        [(border_margin + 12, border_margin + 12), (width - border_margin - 12, height - border_margin - 12)],
        outline=GOLD_PRIMARY,
        width=2
    )

    # 5. Header / Title Section
    draw.text((width // 2, 140), "QRATEDX PRESENTS", fill=MUTED_GRAY, font=font_small, anchor="mm")
    draw.text((width // 2, 230), "TEAM MARK X KADOMA", fill=GOLD_PRIMARY, font=font_title, anchor="mm")
    draw.text((width // 2, 320), "CITY OF GOLD EDITION", fill=GOLD_LIGHT, font=font_subtitle, anchor="mm")
    draw.text((width // 2, 390), "BIG BULLS MEET IN THE MIDDLE", fill=WHITE, font=font_section, anchor="mm")
    
    # Divider Line
    draw.line([(150, 440), (width - 150, 440)], fill=GOLD_PRIMARY, width=4)

    # 6. Nationwide Route Badge
    route_text = "HARARE • BULAWAYO • GWERU • KWEKWE • MUTARE"
    draw.rectangle([(140, 470), (width - 140, 540)], fill=DARK_CARD, outline=GOLD_PRIMARY, width=2)
    draw.text((width // 2, 505), route_text, fill=WHITE, font=font_body, anchor="mm")

    # 7. Event Core Details Card
    card_top = 580
    card_bottom = 980
    draw.rectangle([(140, card_top), (width - 140, card_bottom)], fill=DARK_CARD, outline=GOLD_PRIMARY, width=3)
    
    draw.text((width // 2, card_top + 60), "EVENT DETAILS", fill=GOLD_LIGHT, font=font_section, anchor="mm")
    draw.text((width // 2, card_top + 140), "DATE: 10 OCTOBER 2026", fill=WHITE, font=font_subtitle, anchor="mm")
    draw.text((width // 2, card_top + 220), "VENUE: SPEEDWAY BAR, KADOMA", fill=GOLD_PRIMARY, font=font_subtitle, anchor="mm")
    draw.text((width // 2, card_top + 300), "GATES OPEN: 09:00 AM • DRESS CODE: CLEAN FASHIONED", fill=WHITE, font=font_body, anchor="mm")

    # 8. Awards & Showcases Box
    showcase_top = 1030
    draw.rectangle([(140, showcase_top), (width - 140, showcase_top + 480)], fill=(20, 20, 20), outline=MUTED_GRAY, width=2)
    draw.text((width // 2, showcase_top + 50), "OFFICIAL SHOWCASE & AWARDS", fill=GOLD_LIGHT, font=font_section, anchor="mm")
    
    categories = [
        "• Best Mark X Build (GRX120 / GRX130)   • Loud Exhaust King",
        "• Cleanest Ride & Lowest Stance         • Best Rims Pimped",
        "• Lady Bulls: Queen of the Track        • Golden Touch (Best Interior)",
        "• Road Map to Kadoma Music Festival @ Odyssey"
    ]
    for idx, text in enumerate(categories):
        draw.text((width // 2, showcase_top + 130 + (idx * 70)), text, fill=WHITE, font=font_body, anchor="mm")

    # 9. Official Physical Stamp / Verification Box (For Entry Pass / Stamping)
    stamp_center_x = 350
    stamp_center_y = 1800
    stamp_radius = 160
    
    # Outer circle for stamp
    draw.ellipse(
        [(stamp_center_x - stamp_radius, stamp_center_y - stamp_radius),
         (stamp_center_x + stamp_radius, stamp_center_y + stamp_radius)],
        outline=GOLD_PRIMARY,
        width=5
    )
    # Dashed/Inner ring guide
    inner_r = stamp_radius - 15
    draw.ellipse(
        [(stamp_center_x - inner_r, stamp_center_y - inner_r),
         (stamp_center_x + inner_r, stamp_center_y + inner_r)],
        outline=MUTED_GRAY,
        width=2
    )
    draw.text((stamp_center_x, stamp_center_y - 25), "OFFICIAL", fill=GOLD_LIGHT, font=font_section, anchor="mm")
    draw.text((stamp_center_x, stamp_center_y + 25), "STAMP HERE", fill=WHITE, font=font_body, anchor="mm")

    # 10. Organisers & Contacts (Right side of stamp)
    info_x = 600
    info_y = 1660
    draw.text((info_x, info_y), "ORGANISERS & CONTACTS:", fill=GOLD_PRIMARY, font=font_section)
    draw.text((info_x, info_y + 70), "Craig T (Craig Motors): 0790 187 400", fill=WHITE, font=font_body)
    draw.text((info_x, info_y + 140), "DJ Sir Clemmie Dee (A1 Soundz): 0773 730 063", fill=WHITE, font=font_body)
    draw.text((info_x, info_y + 210), "Mr Mapeta (Speedway Bar): 0779 216 474", fill=WHITE, font=font_body)
    draw.text((info_x, info_y + 280), "Scan & Register Online / WhatsApp", fill=GOLD_LIGHT, font=font_body)

    # 11. Footer
    draw.line([(150, 2260), (width - 150, 2260)], fill=GOLD_PRIMARY, width=3)
    draw.text(
        (width // 2, 2330),
        "#TeamMarkXKadoma  •  #CityOfGold  •  Fearless & United Zimbabwe",
        fill=MUTED_GRAY,
        font=font_body,
        anchor="mm"
    )

    # Save output
    img.save(output_filename, dpi=(300, 300))
    print(f"Print-ready flyer generated successfully at: {output_filename}")

if __name__ == "__main__":
    create_event_flyer()