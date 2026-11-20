import os
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFilter

SCREENSHOT_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots'
RENDER_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs('/tmp/ff_master_profile', exist_ok=True)

print("Step 1: Generating realistic visual background assets...")

# Asset A: Rice Plant Macro Texture for Panen Tanam
rice_w, rice_h = 412, 540
rice_im = Image.new('RGB', (rice_w, rice_h), (18, 48, 26))
rice_draw = ImageDraw.Draw(rice_im)

for y in range(rice_h):
    r = int(14 + (y / rice_h) * 16)
    g = int(58 - (y / rice_h) * 24)
    b = int(28 - (y / rice_h) * 16)
    rice_draw.line([(0, y), (rice_w, y)], fill=(r, g, b))

random.seed(101)
for i in range(12):
    lx = random.randint(40, 360)
    curve = random.randint(-40, 40)
    leaf_pts = [
        (lx, 0),
        (lx + curve, 180),
        (lx + curve * 2, 380),
        (lx + curve * 3, rice_h)
    ]
    leaf_w = random.randint(22, 45)
    leaf_col = random.choice([(45, 115, 60), (38, 98, 52), (52, 130, 70), (32, 85, 42)])
    for j in range(len(leaf_pts)-1):
        rice_draw.line([leaf_pts[j], leaf_pts[j+1]], fill=leaf_col, width=leaf_w)
    for j in range(len(leaf_pts)-1):
        rice_draw.line([leaf_pts[j], leaf_pts[j+1]], fill=(80, 165, 95), width=2)

cx, cy = 206, 240
for r in range(45, 5, -5):
    rice_draw.ellipse([cx - r, cy - int(r*1.6), cx + r, cy + int(r*1.6)], fill=(155 - r, 110 - int(r*0.8), 40))

rice_im = rice_im.filter(ImageFilter.SMOOTH)
rice_asset_path = f'{RENDER_DIR}/rice_leaf_macro.jpg'
rice_im.save(rice_asset_path, quality=92)
print("   ✅ Generated rice_leaf_macro.jpg")

# Asset B: Cartography Texture for SIG Desa
map_w, map_h = 1440, 860
map_im = Image.new('RGB', (map_w, map_h), (236, 244, 232))
map_draw = ImageDraw.Draw(map_im)

random.seed(777)
for x in range(0, map_w, 55):
    for y in range(0, map_h, 55):
        tone = random.choice([
            (222, 238, 216), (228, 242, 222), (214, 232, 208),
            (206, 226, 200), (232, 244, 226), (198, 220, 192)
        ])
        map_draw.rectangle([x, y, x+53, y+53], fill=tone, outline=(184, 208, 178), width=1)

river_pts = []
for x in range(0, map_w+60, 30):
    y = int(280 + 75 * math.sin(x / 160.0) + 25 * math.cos(x / 80.0))
    river_pts.append((x, y))

for i in range(len(river_pts)-1):
    map_draw.line([river_pts[i], river_pts[i+1]], fill=(130, 185, 238), width=34)
for i in range(len(river_pts)-1):
    map_draw.line([river_pts[i], river_pts[i+1]], fill=(168, 214, 255), width=22)

roads = [
    [(0, 720), (320, 500), (560, 340), (880, 200), (1180, 140), (1440, 100)],
    [(560, 340), (580, 680), (620, 860)],
    [(320, 500), (760, 600), (1120, 500), (1440, 460)],
    [(1180, 140), (1220, 500), (1280, 860)]
]
for r in roads:
    for i in range(len(r)-1):
        map_draw.line([r[i], r[i+1]], fill=(255, 255, 255), width=16)
        map_draw.line([r[i], r[i+1]], fill=(255, 215, 0), width=2)

for _ in range(120):
    bx = random.randint(280, 1260)
    by = random.randint(180, 800)
    bw, bh = random.randint(18, 38), random.randint(14, 28)
    map_draw.rectangle([bx, by, bx+bw, by+bh], fill=random.choice([(215, 145, 125), (200, 130, 110), (185, 155, 135)]), outline=(145, 95, 85))

map_im = map_im.filter(ImageFilter.SMOOTH_MORE)
map_asset_path = f'{RENDER_DIR}/sig_carto_base.jpg'
map_im.save(map_asset_path, quality=94)
print("   ✅ Generated sig_carto_base.jpg")

# Asset C: Apparel Thumbnails
apparel_items = [
    ('bge_tee.jpg', (35, 35, 40)),
    ('bge_denim.jpg', (38, 55, 85)),
    ('bge_hoodie.jpg', (120, 125, 130))
]
for fname, col in apparel_items:
    aim = Image.new('RGB', (160, 160), col)
    adraw = ImageDraw.Draw(aim)
    adraw.rectangle([20, 20, 140, 140], outline=(255, 255, 255), width=2)
    aim.save(f'{RENDER_DIR}/{fname}')

# Templates
html_sig_desa = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1440px; height: 860px; font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #1e293b; display: flex; flex-direction: column; overflow: hidden;
  }}
  header {{
    height: 64px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between; padding: 0 24px;
    z-index: 40; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }}
  .brand-area {{ display: flex; align-items: center; gap: 12px; }}
  .emblem {{
    width: 38px; height: 38px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.2rem;
  }}
  .brand-titles h1 {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px; }}
  .tenant-pill {{ background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px; }}
  .workspace {{ flex: 1; display: flex; position: relative; overflow: hidden; }}
  .gis-sidebar {{
    width: 360px; background: rgba(255, 255, 255, 0.96); backdrop-filter: blur(16px);
    border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 30;
  }}
  .sidebar-section {{ padding: 16px 20px; border-bottom: 1px solid #f1f5f9; }}
  .section-title {{ font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 10px; }}
  .kpi-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .kpi-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; }}
  .kpi-num {{ font-size: 1.25rem; font-weight: 800; color: #0f172a; }}
  .kpi-label {{ font-size: 0.7rem; color: #64748b; font-weight: 600; }}
  .layer-item {{ display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px dashed #f1f5f9; }}
  .color-swatch {{ width: 14px; height: 14px; border-radius: 4px; }}
  .layer-name {{ font-size: 0.82rem; font-weight: 600; color: #334155; }}
  .layer-badge {{ font-size: 0.68rem; font-weight: 700; color: #64748b; background: #f1f5f9; padding: 2px 7px; border-radius: 6px; }}
  .map-canvas {{
    flex: 1; position: relative; background-image: url('file://{map_asset_path}');
    background-size: cover; background-position: center; overflow: hidden;
  }}
  .feature-inspector-popup {{
    position: absolute; bottom: 24px; left: 384px; z-index: 25;
    background: #ffffff; border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18); border: 1px solid #cbd5e1; max-width: 440px;
  }}
  .inspector-tag {{ font-size: 0.65rem; font-weight: 800; text-transform: uppercase; color: #059669; }}
  .inspector-title {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; margin: 2px 0 6px; }}
  .inspector-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; }}
  .attr-val {{ font-size: 0.85rem; font-weight: 700; color: #1e293b; font-family: 'JetBrains Mono'; }}
  .attr-lbl {{ font-size: 0.65rem; color: #64748b; font-weight: 600; }}
  .coords-chip {{
    position: absolute; bottom: 24px; right: 24px; z-index: 25;
    background: rgba(15, 23, 42, 0.88); color: #e2e8f0; font-size: 0.72rem;
    font-family: 'JetBrains Mono'; padding: 6px 14px; border-radius: 8px;
  }}
</style>
</head>
<body>
  <header>
    <div class="brand-area">
      <div class="emblem">🗺️</div>
      <div class="brand-titles">
        <h1><span>SIG Desa Karangrau</span><span class="tenant-pill">Kec. Banyumas</span></h1>
        <div style="font-size: 0.74rem; color: #64748b;">Sistem Informasi Geografis Profil &amp; Batas Administrasi Desa</div>
      </div>
    </div>
    <div style="font-size: 0.8rem; font-weight: 700; background: #0f172a; color: white; padding: 8px 16px; border-radius: 8px;">
      Panel Administrasi Spasial PostGIS ↗
    </div>
  </header>
  <div class="workspace">
    <aside class="gis-sidebar">
      <div class="sidebar-section">
        <div class="section-title">Ringkasan Wilayah Desa</div>
        <div class="kpi-row">
          <div class="kpi-box"><div class="kpi-num">4,856</div><div class="kpi-label">Total Penduduk</div></div>
          <div class="kpi-box"><div class="kpi-num">284.5 Ha</div><div class="kpi-label">Luas Terpetakan</div></div>
        </div>
      </div>
      <div class="sidebar-section" style="flex: 1;">
        <div class="section-title">Lapisan Spasial Aktif (PostGIS)</div>
        <div class="layer-item"><div style="display:flex;align-items:center;gap:8px;"><div class="color-swatch" style="background:#10b981;"></div><span class="layer-name">Batas Dusun &amp; RW</span></div><span class="layer-badge">3 Dusun • 16 RW</span></div>
        <div class="layer-item"><div style="display:flex;align-items:center;gap:8px;"><div class="color-swatch" style="background:#3b82f6;"></div><span class="layer-name">Sungai &amp; Saluran Irigasi</span></div><span class="layer-badge">12.4 km</span></div>
        <div class="layer-item"><div style="display:flex;align-items:center;gap:8px;"><div class="color-swatch" style="background:#eab308;"></div><span class="layer-name">Lahan Pertanian Basah</span></div><span class="layer-badge">186.2 Ha</span></div>
        <div class="layer-item"><div style="display:flex;align-items:center;gap:8px;"><div class="color-swatch" style="background:#ef4444;"></div><span class="layer-name">Fasilitas Publik &amp; Balai</span></div><span class="layer-badge">24 Titik</span></div>
      </div>
    </aside>
    <div class="map-canvas">
      <svg style="width:100%; height:100%; position:absolute; top:0; left:0;" viewBox="0 0 1080 796">
        <polygon points="260,190 680,180 740,540 310,560" fill="rgba(16, 185, 129, 0.24)" stroke="#059669" stroke-width="3.5" stroke-dasharray="6,4"/>
        <polygon points="680,180 1040,160 1000,520 740,540" fill="rgba(59, 130, 246, 0.16)" stroke="#2563eb" stroke-width="2.5"/>
        <text x="320" y="360" transform="rotate(-32, 320, 360)" fill="#0f172a" font-size="12" font-weight="800" stroke="#ffffff" stroke-width="3" paint-order="stroke fill">Jl. Raya Karangrau</text>
        <g transform="translate(560, 340)">
          <circle r="18" fill="#ef4444" opacity="0.25"/><circle r="10" fill="#ef4444"/>
          <text x="0" y="4" fill="white" font-size="10" text-anchor="middle" font-weight="800">🏛</text>
          <rect x="18" y="-12" width="130" height="24" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="26" y="4" fill="#0f172a" font-size="10" font-weight="800">Balai Desa Karangrau</text>
        </g>
      </svg>
      <div class="feature-inspector-popup">
        <div class="inspector-tag">PostGIS Poligon Aktif (ID: GEO-DSN-02)</div>
        <div class="inspector-title">Dusun II Karangrau (RW 03 &amp; RW 04)</div>
        <p style="font-size: 0.78rem; color: #475569; line-height: 1.45;">
          Kawasan sentra pertanian padi irigasi teknis dan pemukiman warga terhubung ke jaringan irigasi sekunder Sungai Pelus.
        </p>
        <div class="inspector-grid">
          <div><div class="attr-val">1,620</div><div class="attr-lbl">Warga</div></div>
          <div><div class="attr-val">412 KK</div><div class="attr-lbl">Keluarga</div></div>
          <div><div class="attr-val">42.8 Ha</div><div class="attr-lbl">Luas</div></div>
        </div>
      </div>
      <div class="coords-chip">
        EPSG:4326 | Lat: -7.4294, Lng: 109.2435 | PostGIS GIST Spatial Index
      </div>
    </div>
  </div>
</body>
</html>'''

html_panen_tanam = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px; background: #09130c; color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif; display: flex; flex-direction: column; overflow: hidden;
  }}
  .status-bar {{ height: 38px; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; font-weight: 600; z-index: 30; }}
  .camera-viewport {{
    flex: 1; position: relative; background-image: url('file://{rice_asset_path}');
    background-size: cover; background-position: center; overflow: hidden; display: flex; align-items: center; justify-content: center;
  }}
  .hud-badge {{
    position: absolute; top: 14px; background: rgba(9, 19, 12, 0.75); backdrop-filter: blur(10px);
    border: 1px solid rgba(74, 222, 128, 0.3); color: #86efac; font-size: 0.72rem; font-weight: 700;
    padding: 5px 12px; border-radius: 9999px;
  }}
  .ai-target-box {{
    width: 220px; height: 260px; position: absolute; top: 110px;
    border: 2px solid #22c55e; border-radius: 18px;
    box-shadow: 0 0 30px rgba(34, 197, 94, 0.5), inset 0 0 15px rgba(34, 197, 94, 0.25);
  }}
  .ai-label-pill {{
    position: absolute; top: -14px; left: 16px; background: #22c55e; color: #052e16;
    font-size: 0.7rem; font-weight: 800; padding: 4px 12px; border-radius: 9999px;
  }}
  .diagnostic-sheet {{
    background: rgba(14, 28, 19, 0.96); backdrop-filter: blur(24px);
    border-top: 1px solid rgba(74, 222, 128, 0.35); border-radius: 26px 26px 0 0;
    padding: 20px 22px 28px; display: flex; flex-direction: column; gap: 12px; z-index: 30;
  }}
  .disease-name {{ font-size: 1.15rem; font-weight: 800; color: #ffffff; }}
  .score-badge {{ background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; color: #4ade80; font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 9999px; }}
  .treatment-card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px 14px; }}
  .btn-submit-action {{ background: #22c55e; color: #052e16; font-size: 0.85rem; font-weight: 800; padding: 13px; border-radius: 9999px; border: none; width: 100%; text-align: center; }}
</style>
</head>
<body>
  <div class="status-bar"><span>09:41</span><span>● 4G &bull; 94%</span></div>
  <div class="camera-viewport">
    <div class="hud-badge">Edge AI NPU 38ms &bull; MobileNetV4</div>
    <div class="ai-target-box">
      <div class="ai-label-pill">✓ Hawar Daun Bakteri (98.4%)</div>
    </div>
  </div>
  <div class="diagnostic-sheet">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
      <div>
        <div class="disease-name">Hawar Daun Bakteri (BLB)</div>
        <div style="font-size:0.72rem; color:#86efac; font-style:italic;">Xanthomonas oryzae pv. oryzae</div>
      </div>
      <span class="score-badge">Akurasi 98.4%</span>
    </div>
    <p style="font-size: 0.78rem; color: #94a3b8; line-height: 1.4;">
      Terdeteksi garis basah kekuningan di tepi daun padi Ciherang (Fase Awal • Keparahan 22%).
    </p>
    <div class="treatment-card">
      <div style="font-size:0.68rem; font-weight:700; color:#4ade80; text-transform:uppercase;">Rekomendasi Penanganan Petani:</div>
      <div style="font-size:0.78rem; color:#e2e8f0; line-height:1.45;">
        Semprotkan bakterisida hayati (Bacillus subtilis) dosis 2.0 ml/L pada pagi hari. Keringkan sawah secara berkala (intermittent irrigation) untuk memutus kelembaban spora.
      </div>
    </div>
    <div class="btn-submit-action">Catat ke Riwayat Perawatan Petak Sawah</div>
  </div>
</body>
</html>'''

templates = [
    ('sig_master.html', html_sig_desa, f'{SCREENSHOT_DIR}/sig_desa.png', '1440,860'),
    ('panen_master.html', html_panen_tanam, f'{SCREENSHOT_DIR}/panen_tanam_scan.png', '412,860'),
    ('panen_master.html', html_panen_tanam, f'{SCREENSHOT_DIR}/panen_tanam_mobile.png', '412,860')
]

for fname, html, out_png, dims in templates:
    tpath = f'{RENDER_DIR}/{fname}'
    with open(tpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Rendering {fname} -> {out_png}...")
    cmd = [
        'firefox', '--headless',
        '-profile', '/tmp/ff_master_profile',
        '--screenshot', out_png,
        f'--window-size={dims}',
        f'file://{tpath}'
    ]
    subprocess.run(cmd, check=True)
    print(f"   ✅ Done: {out_png} ({os.path.getsize(out_png)} bytes)")

print("Master Rendering Completed!")
