#!/usr/bin/env python3
"""
PhotoDay Picture Day Kit PDF Generator
Called by Claude after Canva assets are generated.
Usage: python3 generate_kit_pdf.py '<config_json>' '[{"url":"...","name":"..."},...]'
"""
import sys, json, re
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def hex2color(h):
    h = h.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return Color(r/255, g/255, b/255)

def luminance(hex_c):
    h = hex_c.lstrip('#')
    r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrasting(hex_c):
    return '#FFFFFF' if luminance(hex_c) < 0.5 else '#000000'

ASSETS = [
    { 'tag':'EMAIL',   'name':'Email / Flyer Banner',    'dims':'1200 × 545 px',   'ratio': 1200/545,  'use':'Email campaigns & digital flyers' },
    { 'tag':'WEB-V',   'name':'Vertical Web Banner',     'dims':'300 × 600 px',    'ratio': 300/600,   'use':'School website sidebar' },
    { 'tag':'WEB-H',   'name':'Horizontal Web Banner',   'dims':'728 × 90 px',     'ratio': 728/90,    'use':'Website header & digital signage' },
    { 'tag':'SOCIAL',  'name':'4:5 Social Graphic',      'dims':'1080 × 1350 px',  'ratio': 1080/1350, 'use':'Instagram & Facebook posts' },
    { 'tag':'CARD',    'name':'Reminder Cards',           'dims':'3.5" × 5"',       'ratio': 3.5/5,     'use':'Take-home reminder cards for students' },
    { 'tag':'POSTER',  'name':'Picture Day Poster',       'dims':'20" × 30"',       'ratio': 20/30,     'use':'Hallway & bulletin board print' },
]

POST_SUGGESTIONS = [
    ["📧 Email & Digital Flyer",
     "Send 3 weeks before picture day to all families",
     "Resend 1 week before as a reminder",
     "Send day-of with a direct gallery/registration link"],
    ["📱 School Website Sidebar",
     "Post 4 weeks out — keep live until 1 week after picture day",
     "Link directly to gallery or registration page"],
    ["🖥️ Website Header & Digital Signage",
     "Add to school website header 3 weeks before",
     "Display on lobby screens/marquee signs the week of picture day"],
    ["📲 Instagram & Facebook",
     "Post 3 weeks, 1 week, and 3 days before picture day",
     "Share in parent Facebook groups and school community pages",
     "Use Stories/Reels the day of for extra reach"],
    ["🖼️ Print & Distribute Reminder Cards",
     "Send home with students 1–2 weeks before",
     "Ideal for teacher distribution with take-home folders",
     "Print on cardstock for a professional feel"],
    ["📋 Hallway & Bulletin Board Posters",
     "Print and hang 3–4 weeks before picture day",
     "Place at main entrance, cafeteria, and hallways",
     "Replace with 'Picture Day is TODAY!' sign on the day"],
]

def draw_cover(c, cfg, W, H, asset_count):
    primary   = cfg['theme']['primary']
    secondary = cfg['theme']['secondary']
    job_name  = cfg['jobName']
    date      = cfg['date']
    job_type  = cfg['jobTypeLabel']

    # Background gradient simulation
    c.setFillColor(hex2color(primary))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Accent block
    c.setFillColor(hex2color(secondary))
    c.rect(0, H*0.18, W, H*0.06, fill=1, stroke=0)

    # Title
    tc = contrasting(primary)
    c.setFillColor(HexColor(tc))
    c.setFont('Helvetica-Bold', 36)
    title = f"{job_name}'s"
    c.drawCentredString(W/2, H*0.62, title)
    c.setFont('Helvetica-Bold', 48)
    c.drawCentredString(W/2, H*0.50, 'Picture Day Kit')

    # Subtitle
    c.setFont('Helvetica', 18)
    c.setFillColor(HexColor(contrasting(primary)))
    alpha_fill = HexColor(secondary)
    c.drawCentredString(W/2, H*0.39, date + '  ·  ' + job_type)

    # AP badge if required
    if cfg['advancePay']['required']:
        c.setFillColor(HexColor('#7F1D1D'))
        c.roundRect(W/2-120, H*0.28, 240, 32, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W/2, H*0.28+10, '⚠  AdvancePay Required — Registration CTA')

    # Asset count badge
    asset_label = f'{asset_count} Ready-to-Use Marketing Asset{"s" if asset_count != 1 else ""}'
    badge_w = max(160, len(asset_label) * 7 + 24)
    c.setFillColor(hex2color(secondary))
    c.roundRect(W/2 - badge_w/2, H*0.19, badge_w, 28, 5, fill=1, stroke=0)
    c.setFillColor(HexColor(contrasting(secondary)))
    c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(W/2, H*0.19+8, asset_label)

    # Footer
    c.setFillColor(HexColor('#00000033'))
    c.rect(0, 0, W, H*0.12, fill=1, stroke=0)
    c.setFillColor(HexColor(tc))
    c.setFont('Helvetica', 11)
    c.drawCentredString(W/2, H*0.05, 'Generated by PhotoDay  ·  Powered by Canva')

def draw_asset_page(c, cfg, asset_idx, asset_info, canva_links, W, H):
    a       = ASSETS[asset_idx]
    primary = cfg['theme']['primary']
    sec     = cfg['theme']['secondary']
    sugg    = POST_SUGGESTIONS[asset_idx]
    MARGIN  = 36
    COL_GAP = 18

    # ── HEADER ──────────────────────────────────────
    HDR_H = 72
    c.setFillColor(hex2color(primary))
    c.rect(0, H - HDR_H, W, HDR_H, fill=1, stroke=0)

    # Number badge
    badge_r = 22
    bx, by = W - MARGIN - badge_r, H - HDR_H/2
    c.setFillColor(hex2color(sec))
    c.circle(bx, by, badge_r, fill=1, stroke=0)
    c.setFillColor(HexColor(contrasting(sec)))
    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(bx, by - 6, str(asset_idx + 1))

    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 19)
    c.drawString(MARGIN, H - 36, a['name'])
    c.setFont('Helvetica', 11)
    c.drawString(MARGIN, H - 54, a['dims'] + '   ·   ' + a['use'])

    # ── TWO-COLUMN LAYOUT ───────────────────────────
    CONTENT_TOP = H - HDR_H - 18
    FOOTER_H    = 30
    CONTENT_BOT = FOOTER_H + 10
    CONTENT_H   = CONTENT_TOP - CONTENT_BOT

    # LEFT column: thumbnail preview
    L_W = (W - MARGIN*2 - COL_GAP) * 0.52
    L_X = MARGIN

    # RIGHT column: details
    R_X = L_X + L_W + COL_GAP
    R_W = W - MARGIN - R_X

    # ── THUMBNAIL ───────────────────────────────────
    max_thumb_w = L_W - 8
    max_thumb_h = CONTENT_H * 0.52
    ratio = a['ratio']
    if ratio >= 1:                                 # landscape / square
        tw = min(max_thumb_w, max_thumb_h * ratio)
        th = tw / ratio
    else:                                          # portrait
        th = min(max_thumb_h, max_thumb_w / ratio)
        tw = th * ratio
    tx = L_X + (L_W - tw) / 2
    ty = CONTENT_TOP - 12 - th

    thumb_url = None
    if canva_links and asset_idx < len(canva_links):
        thumb_url = canva_links[asset_idx].get('thumbnail')

    if thumb_url and thumb_url.startswith('http'):
        try:
            import urllib.request
            data = urllib.request.urlopen(thumb_url, timeout=8).read()
            img  = ImageReader(BytesIO(data))
            c.drawImage(img, tx, ty, width=tw, height=th, preserveAspectRatio=True, anchor='c')
            # border
            c.setStrokeColor(HexColor('#E5E7EB'))
            c.setLineWidth(1)
            c.roundRect(tx, ty, tw, th, 4, fill=0, stroke=1)
        except Exception:
            _draw_placeholder(c, primary, sec, a['tag'], tx, ty, tw, th)
    else:
        _draw_placeholder(c, primary, sec, a['tag'], tx, ty, tw, th)

    # ── CTA PILL ────────────────────────────────────
    cta    = cfg['cta']['button']
    pill_y = ty - 14
    pill_h = 26
    pill_w = L_W - 8
    c.setFillColor(hex2color(sec))
    c.roundRect(L_X + 4, pill_y - pill_h, pill_w, pill_h, 6, fill=1, stroke=0)
    c.setFillColor(HexColor(contrasting(sec)))
    c.setFont('Helvetica-Bold', 10)
    cta_display = f'CTA: "{cta}"'
    # truncate if too long
    while c.stringWidth(cta_display, 'Helvetica-Bold', 10) > pill_w - 16 and len(cta_display) > 10:
        cta_display = cta_display[:-2] + '…"'
    c.drawCentredString(L_X + 4 + pill_w/2, pill_y - pill_h + 8, cta_display)

    # ── POSTING SUGGESTIONS (auto-height) ───────────
    def wrap_text(text, font, size, max_w, canvas_obj):
        words = text.split(); line, lines = '', []
        for w in words:
            test = (line + ' ' + w).strip()
            if canvas_obj.stringWidth(test, font, size) < max_w:
                line = test
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)
        return lines

    LINE_H = 13
    DOT_R  = 3
    tip_lines_all = []
    for tip in sugg[1:]:
        tip_lines_all.append(wrap_text(tip, 'Helvetica', 9, L_W - 34, c))

    sug_inner_h = 14 + 14 + sum(len(ll)*LINE_H + 4 for ll in tip_lines_all) + 6
    sug_h   = max(sug_inner_h, 60)
    sug_top = pill_y - pill_h - 18

    c.setFillColor(HexColor('#FFFBEB'))
    c.roundRect(L_X, sug_top - sug_h, L_W, sug_h, 8, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#FDE68A'))
    c.setLineWidth(1)
    c.roundRect(L_X, sug_top - sug_h, L_W, sug_h, 8, fill=0, stroke=1)

    c.setFillColor(HexColor('#78350F'))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(L_X + 10, sug_top - 14, 'WHEN & WHERE TO POST')
    c.setFillColor(HexColor('#92400E'))
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(L_X + 10, sug_top - 26, sugg[0])

    c.setFont('Helvetica', 9)
    tip_y = sug_top - 40
    for tip_lines in tip_lines_all:
        c.setFillColor(hex2color(sec))
        c.circle(L_X + 16, tip_y + 3, DOT_R, fill=1, stroke=0)
        c.setFillColor(HexColor('#92400E'))
        for ln in tip_lines:
            c.drawString(L_X + 24, tip_y, ln)
            tip_y -= LINE_H
        tip_y -= 4

    # ── LEFT COLUMN FILL (for wide/short previews) ──
    left_used_bottom = sug_top - sug_h          # bottom of suggestions box
    left_available   = left_used_bottom - CONTENT_BOT - 12

    PHOTO_TIPS = [
        ["Remind parents about picture day retakes by scheduling a follow-up email with your gallery link.",
         "Photographers with 3+ touchpoints see 40% higher photo order rates."],
        ["Keep your web banner live for at least 1 week after picture day — late orders often come in the first 7 days.",
         "Linking the banner directly to the gallery increases conversion significantly."],
        ["Boost reach by sharing the horizontal banner to school digital signage and the school's email newsletter.",
         "Consistent messaging across channels drives more orders."],
        ["Tag the school in your social post and ask them to share it — their followers are your customers.",
         "Schools with co-posted content see 2–3x more gallery visits from social."],
        ["Send reminder cards home the Friday before picture day for maximum impact.",
         "Pre-printed cards with access codes reduce parent confusion at order time."],
        ["Hang posters near parent drop-off/pick-up zones for maximum visibility.",
         "Adding QR codes to printed posters lets parents register or order on-the-spot."],
    ]
    ptip = PHOTO_TIPS[asset_idx]
    tip_box_h = min(left_available - 8, 80)
    if tip_box_h >= 44:
        tip_y_top = left_used_bottom - 8
        c.setFillColor(HexColor('#EFF6FF'))
        c.roundRect(L_X, tip_y_top - tip_box_h, L_W, tip_box_h, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#BFDBFE'))
        c.setLineWidth(1)
        c.roundRect(L_X, tip_y_top - tip_box_h, L_W, tip_box_h, 8, fill=0, stroke=1)
        c.setFillColor(hex2color(primary))
        c.setFont('Helvetica-Bold', 9)
        c.drawString(L_X + 10, tip_y_top - 13, 'PHOTODAY TIP')
        c.setFillColor(HexColor('#1E40AF'))
        c.setFont('Helvetica', 8.5)
        tr_y = tip_y_top - 25
        for para in ptip:
            if tr_y < tip_y_top - tip_box_h + 8: break
            wrapped = wrap_text(para, 'Helvetica', 8.5, L_W - 22, c)
            for wl in wrapped:
                if tr_y < tip_y_top - tip_box_h + 8: break
                c.drawString(L_X + 10, tr_y, wl)
                tr_y -= 11
            tr_y -= 4

    # ── RIGHT COLUMN ────────────────────────────────
    ry = CONTENT_TOP - 12

    # Specs box
    specs_h = 110
    c.setFillColor(HexColor('#F8FAFC'))
    c.roundRect(R_X, ry - specs_h, R_W, specs_h, 8, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#E5E7EB'))
    c.roundRect(R_X, ry - specs_h, R_W, specs_h, 8, fill=0, stroke=1)

    c.setFillColor(hex2color(primary))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(R_X + 12, ry - 16, 'ASSET SPECS')
    c.setFillColor(HexColor('#374151'))
    c.setFont('Helvetica', 9.5)
    spec_rows = [
        ('Dimensions',  a['dims']),
        ('Format',      'PNG (digital), PDF (print)'),
        ('Gallery type', cfg['gallery']['type'].title()),
    ]
    if cfg['gallery'].get('accessCode'):
        spec_rows.append(('Access code', cfg['gallery']['accessCode']))
    if cfg['gallery'].get('qrUrl'):
        spec_rows.append(('QR target',   cfg['gallery']['qrUrl']))
    for i, (lbl, val) in enumerate(spec_rows):
        sy2 = ry - 32 - i * 16
        if sy2 < ry - specs_h + 8: break
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(HexColor('#6B7280'))
        c.drawString(R_X + 12, sy2, lbl + ':')
        c.setFont('Helvetica', 9)
        c.setFillColor(HexColor('#1E293B'))
        c.drawString(R_X + 90, sy2, str(val))

    ry -= specs_h + 14

    # Gallery lookup box
    lookup_h = 56
    gl = cfg['gallery'].get('lookupText', '')
    if gl:
        c.setFillColor(HexColor('#F0FDF4'))
        c.roundRect(R_X, ry - lookup_h, R_W, lookup_h, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#86EFAC'))
        c.roundRect(R_X, ry - lookup_h, R_W, lookup_h, 8, fill=0, stroke=1)
        c.setFillColor(HexColor('#065F46'))
        c.setFont('Helvetica-Bold', 9)
        c.drawString(R_X + 12, ry - 14, 'GALLERY LOOKUP TEXT')
        c.setFont('Helvetica', 8.5)
        # wrap
        words = gl.split(); line, lines2 = '', []
        for w in words:
            test = (line + ' ' + w).strip()
            if c.stringWidth(test, 'Helvetica', 8.5) < R_W - 24:
                line = test
            else:
                lines2.append(line); line = w
        if line: lines2.append(line)
        for i2, ln in enumerate(lines2[:2]):
            c.drawString(R_X + 12, ry - 27 - i2*12, ln)
        ry -= lookup_h + 14

    # Canva links
    if canva_links and asset_idx < len(canva_links):
        lnk = canva_links[asset_idx]
        for lbl, url_key, bg, fg in [
            ('Edit in Canva', 'editUrl',  primary, '#FFFFFF'),
            ('View in Canva', 'viewUrl',  sec,     contrasting(sec))
        ]:
            url = lnk.get(url_key)
            if not url: continue
            btn_h = 28
            c.setFillColor(hex2color(bg))
            c.roundRect(R_X, ry - btn_h, R_W, btn_h, 6, fill=1, stroke=0)
            c.setFillColor(HexColor(fg))
            c.setFont('Helvetica-Bold', 10)
            c.drawCentredString(R_X + R_W/2, ry - btn_h + 9, lbl + '  →')
            c.linkURL(url, (R_X, ry - btn_h, R_X + R_W, ry), relative=0)
            ry -= btn_h + 8

    # ── AP / Offer note ─────────────────────────────
    ap = cfg['advancePay']
    if ap['required'] or ap.get('hasOffer'):
        note_rows = []
        if ap['required']:
            note_rows = [
                ('AP REQUIRED', True, '#9F1239'),
                ('CTA: "REGISTER FOR PICTURE DAY"', False, '#9F1239'),
                ('No buy/order language on any assets', False, '#BE123C'),
            ]
            box_bg, box_border = '#FFF1F2', '#FECDD3'
        else:
            amt = ap.get('offerAmount','')
            exp = ap.get('offerExpiry','')
            note_rows = [
                ('ADVANCEPAY OFFER ATTACHED', True, '#065F46'),
                (f'Amount: {amt}', False, '#065F46'),
                (f'Expires: {exp}' if exp else 'Expiry: not set', False, '#047857'),
                ('CTA: "Buy Now, Save Later!"', False, '#065F46'),
            ]
            box_bg, box_border = '#F0FDF4', '#86EFAC'
        note_h = len(note_rows) * 14 + 22
        if ry - note_h > CONTENT_BOT:
            ry -= 8
            c.setFillColor(HexColor(box_bg))
            c.roundRect(R_X, ry - note_h, R_W, note_h, 8, fill=1, stroke=0)
            c.setStrokeColor(HexColor(box_border))
            c.roundRect(R_X, ry - note_h, R_W, note_h, 8, fill=0, stroke=1)
            nr_y = ry - 14
            for txt, bold, col in note_rows:
                c.setFillColor(HexColor(col))
                c.setFont('Helvetica-Bold' if bold else 'Helvetica', 9)
                c.drawString(R_X + 12, nr_y, txt)
                nr_y -= 14
            ry -= note_h + 8

    # ── Timing checklist ────────────────────────────
    timing_map = [
        ['4 weeks out',  '3 weeks out', '1 week out', 'Day of'],
        ['4 weeks out',  '2 weeks out', 'Day of',     ''],
        ['3 weeks out',  '1 week out',  'Day of',     ''],
        ['3 weeks out',  '1 week out',  '3 days out', 'Day of'],
        ['2 weeks out',  '1 week out',  '',           ''],
        ['4 weeks out',  '1 week out',  '',           ''],
    ]
    timing = [t for t in timing_map[asset_idx] if t]
    timing_h = len(timing) * 16 + 28
    if ry - timing_h > CONTENT_BOT:
        ry -= 8
        c.setFillColor(HexColor('#F8FAFC'))
        c.roundRect(R_X, ry - timing_h, R_W, timing_h, 8, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#E5E7EB'))
        c.roundRect(R_X, ry - timing_h, R_W, timing_h, 8, fill=0, stroke=1)
        c.setFillColor(hex2color(primary))
        c.setFont('Helvetica-Bold', 9)
        c.drawString(R_X + 12, ry - 14, 'SUGGESTED SEND SCHEDULE')
        for ti, t in enumerate(timing):
            ty2 = ry - 28 - ti * 16
            # checkbox
            c.setStrokeColor(hex2color(sec))
            c.setLineWidth(1.2)
            c.roundRect(R_X + 12, ty2 - 1, 11, 11, 2, fill=0, stroke=1)
            c.setFillColor(HexColor('#374151'))
            c.setFont('Helvetica', 9)
            c.drawString(R_X + 28, ty2 + 1, t)

    # ── FOOTER ──────────────────────────────────────
    c.setFillColor(HexColor('#F1F5F9'))
    c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    c.setFillColor(HexColor('#64748B'))
    c.setFont('Helvetica', 8.5)
    c.drawString(MARGIN, 10, f'{cfg["jobName"]}   ·   {cfg["date"]}   ·   PhotoDay Picture Day Kit')
    total = cfg.get('_total_assets', 6)
    page_num = cfg.get('_asset_page_num', asset_idx + 1)
    c.drawRightString(W - MARGIN, 10, f'Asset {page_num} of {total}')

def _draw_placeholder(c, primary, sec, tag, x, y, w, h):
    # Background
    c.setFillColor(hex2color(primary))
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    # Inner accent
    pad = max(4, min(w, h) * 0.04)
    c.setFillColor(hex2color(sec))
    c.roundRect(x + pad, y + pad, w - pad*2, h - pad*2, 5, fill=1, stroke=0)
    # Tag label (no emoji — uses plain ASCII)
    c.setFillColor(HexColor(contrasting(sec)))
    tag_fs = min(h * 0.14, 20)
    c.setFont('Helvetica-Bold', tag_fs)
    c.drawCentredString(x + w/2, y + h/2 + tag_fs*0.2, tag)
    c.setFont('Helvetica', min(h * 0.07, 10))
    c.drawCentredString(x + w/2, y + h/2 - tag_fs*0.8, 'Canva design')

def generate_kit_pdf(cfg, canva_links, out_path):
    W, H = letter
    c = canvas.Canvas(out_path, pagesize=(W, H))

    # Determine which asset indices to render
    selected_indices = cfg.get('selectedAssetIndices', list(range(len(ASSETS))))
    # Validate indices
    selected_indices = [i for i in selected_indices if 0 <= i < len(ASSETS)]
    if not selected_indices:
        selected_indices = list(range(len(ASSETS)))

    asset_count = len(selected_indices)

    # Cover page
    draw_cover(c, cfg, W, H, asset_count)
    c.showPage()

    # One page per selected asset
    for page_num, asset_idx in enumerate(selected_indices, start=1):
        asset_info = ASSETS[asset_idx]
        # Inject pagination metadata into cfg for footer
        cfg['_total_assets'] = asset_count
        cfg['_asset_page_num'] = page_num
        draw_asset_page(c, cfg, asset_idx, asset_info, canva_links, W, H)
        c.showPage()

    c.save()
    print(f"PDF saved: {out_path}")

if __name__ == '__main__':
    # Args: config_json canva_links_json out_path
    cfg         = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    canva_links = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
    out_path    = sys.argv[3] if len(sys.argv) > 3 else '/sessions/optimistic-busy-feynman/mnt/outputs/picture-day-kit.pdf'
    generate_kit_pdf(cfg, canva_links, out_path)
