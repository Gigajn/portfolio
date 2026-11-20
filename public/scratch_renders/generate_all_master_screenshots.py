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

# -----------------------------------------------------------------------------
# Asset A: Rice Plant Macro Texture for Panen Tanam
# -----------------------------------------------------------------------------
rice_w, rice_h = 412, 540
rice_im = Image.new('RGB', (rice_w, rice_h), (18, 48, 26))
rice_draw = ImageDraw.Draw(rice_im)

# Sunlight gradient
for y in range(rice_h):
    r = int(14 + (y / rice_h) * 16)
    g = int(58 - (y / rice_h) * 24)
    b = int(28 - (y / rice_h) * 16)
    rice_draw.line([(0, y), (rice_w, y)], fill=(r, g, b))

# Render lush rice leaves with realistic veins and curvature
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
    # Leaf midrib vein
    for j in range(len(leaf_pts)-1):
        rice_draw.line([leaf_pts[j], leaf_pts[j+1]], fill=(80, 165, 95), width=2)

# Add diseased leaf lesion (Hawar Daun / Bacterial Leaf Blight lesion)
cx, cy = 206, 240
for r in range(45, 5, -5):
    rice_draw.ellipse([cx - r, cy - int(r*1.6), cx + r, cy + int(r*1.6)], fill=(155 - r, 110 - int(r*0.8), 40))

rice_im = rice_im.filter(ImageFilter.SMOOTH)
rice_asset_path = f'{RENDER_DIR}/rice_leaf_macro.jpg'
rice_im.save(rice_asset_path, quality=92)
print("   ✅ Generated rice_leaf_macro.jpg")

# -----------------------------------------------------------------------------
# Asset B: Cartography Texture for SIG Desa
# -----------------------------------------------------------------------------
map_w, map_h = 1440, 860
map_im = Image.new('RGB', (map_w, map_h), (236, 244, 232))
map_draw = ImageDraw.Draw(map_im)

# Agricultural & terrain blocks
random.seed(777)
for x in range(0, map_w, 55):
    for y in range(0, map_h, 55):
        tone = random.choice([
            (222, 238, 216), (228, 242, 222), (214, 232, 208),
            (206, 226, 200), (232, 244, 226), (198, 220, 192)
        ])
        map_draw.rectangle([x, y, x+53, y+53], fill=tone, outline=(184, 208, 178), width=1)

# River curve (Sungai Pelus)
river_pts = []
for x in range(0, map_w+60, 30):
    y = int(280 + 75 * math.sin(x / 160.0) + 25 * math.cos(x / 80.0))
    river_pts.append((x, y))

for i in range(len(river_pts)-1):
    map_draw.line([river_pts[i], river_pts[i+1]], fill=(130, 185, 238), width=34)
for i in range(len(river_pts)-1):
    map_draw.line([river_pts[i], river_pts[i+1]], fill=(168, 214, 255), width=22)

# Arterial roads
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

# Village settlement rooftops
for _ in range(120):
    bx = random.randint(280, 1260)
    by = random.randint(180, 800)
    bw, bh = random.randint(18, 38), random.randint(14, 28)
    map_draw.rectangle([bx, by, bx+bw, by+bh], fill=random.choice([(215, 145, 125), (200, 130, 110), (185, 155, 135)]), outline=(145, 95, 85))

map_im = map_im.filter(ImageFilter.SMOOTH_MORE)
map_asset_path = f'{RENDER_DIR}/sig_carto_base.jpg'
map_im.save(map_asset_path, quality=94)
print("   ✅ Generated sig_carto_base.jpg")

# -----------------------------------------------------------------------------
# Asset C: Fashion Apparel Thumbnails for Stock Management BGE
# -----------------------------------------------------------------------------
apparel_items = [
    ('bge_tee.jpg', (35, 35, 40), 'Oversized Tee (Black)'),
    ('bge_denim.jpg', (38, 55, 85), 'Selvedge Denim (Indigo)'),
    ('bge_hoodie.jpg', (120, 125, 130), 'Pullover Hoodie (Grey)'),
    ('bge_sneaker.jpg', (220, 215, 205), 'Retro Runner (White)')
]

for fname, col, lbl in apparel_items:
    aim = Image.new('RGB', (160, 160), col)
    adraw = ImageDraw.Draw(aim)
    adraw.rectangle([20, 20, 140, 140], outline=(255, 255, 255), width=2)
    aim.save(f'{RENDER_DIR}/{fname}')

print("   ✅ Generated apparel assets for BGE Supply")

# -----------------------------------------------------------------------------
# Step 2: Generating HTML Templates for Headless Browser Rendering
# -----------------------------------------------------------------------------

# 1. SIG DESA MASTER TEMPLATE (1440x860)
html_sig_desa_master = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa Karangrau — WebGIS PostGIS Engine</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1440px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  header {{
    height: 64px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; z-index: 40; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }}
  .brand-area {{ display: flex; align-items: center; gap: 12px; }}
  .emblem {{
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 10px; display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }}
  .brand-titles h1 {{
    font-size: 1.05rem; font-weight: 800; color: #0f172a;
    display: flex; align-items: center; gap: 8px;
  }}
  .tenant-pill {{
    background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0;
    font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;
  }}
  .brand-sub {{ font-size: 0.74rem; color: #64748b; }}
  .top-actions {{ display: flex; align-items: center; gap: 12px; }}
  .basemap-toggle {{
    display: flex; background: #f1f5f9; padding: 4px;
    border-radius: 10px; gap: 3px; border: 1px solid #e2e8f0;
  }}
  .opt-btn {{
    border: none; background: transparent; font-family: inherit;
    font-size: 0.78rem; font-weight: 600; padding: 6px 12px;
    border-radius: 7px; color: #64748b;
  }}
  .opt-btn.active {{
    background: #ffffff; color: #0f172a; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }}
  .btn-primary-action {{
    background: #0f172a; color: white; font-size: 0.8rem; font-weight: 700;
    padding: 8px 16px; border-radius: 9px; display: flex; align-items: center; gap: 6px;
  }}
  .workspace {{ flex: 1; display: flex; position: relative; overflow: hidden; }}
  .gis-sidebar {{
    width: 360px; background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(16px); border-right: 1px solid #e2e8f0;
    display: flex; flex-direction: column; z-index: 30;
    box-shadow: 4px 0 20px rgba(0,0,0,0.06);
  }}
  .sidebar-section {{ padding: 16px 20px; border-bottom: 1px solid #f1f5f9; }}
  .section-title {{
    font-size: 0.7rem; font-weight: 800; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px;
  }}
  .kpi-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .kpi-box {{
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 10px 12px;
  }}
  .kpi-num {{ font-size: 1.25rem; font-weight: 800; color: #0f172a; }}
  .kpi-label {{ font-size: 0.7rem; color: #64748b; font-weight: 600; margin-top: 2px; }}
  .layer-item {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 9px 0; border-bottom: 1px dashed #f1f5f9;
  }}
  .layer-item:last-child {{ border-bottom: none; }}
  .layer-meta {{ display: flex; align-items: center; gap: 10px; }}
  .color-swatch {{ width: 14px; height: 14px; border-radius: 4px; }}
  .layer-name {{ font-size: 0.82rem; font-weight: 600; color: #334155; }}
  .layer-badge {{
    font-size: 0.68rem; font-weight: 700; color: #64748b;
    background: #f1f5f9; padding: 2px 7px; border-radius: 6px;
  }}
  .search-wrapper {{ position: relative; margin-top: 6px; }}
  .search-box {{
    width: 100%; padding: 9px 12px 9px 34px;
    border: 1px solid #cbd5e1; border-radius: 9px;
    font-size: 0.8rem; outline: none; background: #f8fafc;
  }}
  .search-ico {{
    position: absolute; left: 10px; top: 50%;
    transform: translateY(-50%); color: #94a3b8; font-size: 0.85rem;
  }}
  .map-canvas {{
    flex: 1; position: relative;
    background-image: url('file://{map_asset_path}');
    background-size: cover; background-position: center;
    overflow: hidden;
  }}
  .map-overlay-polygons {{
    width: 100%; height: 100%; position: absolute; top: 0; left: 0;
  }}
  .map-zoom-controls {{
    position: absolute; top: 20px; right: 20px; z-index: 25;
    display: flex; flex-direction: column; gap: 6px;
  }}
  .zoom-btn {{
    width: 36px; height: 36px; background: white;
    border: 1px solid #cbd5e1; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 700; color: #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }}
  .feature-inspector-popup {{
    position: absolute; bottom: 24px; left: 384px; z-index: 25;
    background: #ffffff; border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18);
    border: 1px solid #cbd5e1; max-width: 440px;
    display: flex; flex-direction: column; gap: 8px;
  }}
  .inspector-header {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
  .inspector-tag {{
    font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
    color: #059669; letter-spacing: 0.5px;
  }}
  .inspector-title {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; }}
  .inspector-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;
    margin-top: 4px; background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 8px 10px;
  }}
  .attr-val {{ font-size: 0.85rem; font-weight: 700; color: #1e293b; font-family: 'JetBrains Mono', monospace; }}
  .attr-lbl {{ font-size: 0.65rem; color: #64748b; font-weight: 600; }}
  .coords-chip {{
    position: absolute; bottom: 24px; right: 24px; z-index: 25;
    background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(8px);
    color: #e2e8f0; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }}
</style>
</head>
<body>
  <header>
    <div class="brand-area">
      <div class="emblem">🗺️</div>
      <div class="brand-titles">
        <h1>
          <span>SIG Desa Karangrau</span>
          <span class="tenant-pill">Kec. Banyumas</span>
        </h1>
        <div class="brand-sub">Sistem Informasi Geografis Profil & Batas Administrasi Desa</div>
      </div>
    </div>
    <div class="top-actions">
      <div class="basemap-toggle">
        <button class="opt-btn active">Peta Vektor</button>
        <button class="opt-btn">Citra Satelit</button>
        <button class="opt-btn">Topografi</button>
      </div>
      <div class="btn-primary-action">
        <span>Panel Administrasi Spasial ↗</span>
      </div>
    </div>
  </header>
  <div class="workspace">
    <aside class="gis-sidebar">
      <div class="sidebar-section">
        <div class="section-title">Ringkasan Wilayah Desa</div>
        <div class="kpi-row">
          <div class="kpi-box">
            <div class="kpi-num">4,856</div>
            <div class="kpi-label">Total Penduduk</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-num">284.5 Ha</div>
            <div class="kpi-label">Luas Terpetakan</div>
          </div>
        </div>
      </div>
      <div class="sidebar-section">
        <div class="section-title">Pencarian Lokasi & Obyek</div>
        <div class="search-wrapper">
          <span class="search-ico">🔍</span>
          <input type="text" class="search-box" value="Dusun II Karangrau" placeholder="Cari batas RW, dusun, fasilitas...">
        </div>
      </div>
      <div class="sidebar-section" style="flex: 1; overflow-y: auto;">
        <div class="section-title">Lapisan Spasial Aktif (PostGIS)</div>
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #10b981;"></div>
            <span class="layer-name">Batas Dusun & RW</span>
          </div>
          <span class="layer-badge">3 Dusun • 16 RW</span>
        </div>
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #3b82f6;"></div>
            <span class="layer-name">Sungai & Jaringan Irigasi</span>
          </div>
          <span class="layer-badge">12.4 km</span>
        </div>
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #eab308;"></div>
            <span class="layer-name">Tutupan Lahan Pertanian</span>
          </div>
          <span class="layer-badge">186.2 Ha</span>
        </div>
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #ef4444;"></div>
            <span class="layer-name">Fasilitas Publik & Balai Desa</span>
          </div>
          <span class="layer-badge">24 Titik</span>
        </div>
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #8b5cf6;"></div>
            <span class="layer-name">Zona Pemukiman Warga</span>
          </div>
          <span class="layer-badge">98.3 Ha</span>
        </div>
      </div>
    </aside>
    <div class="map-canvas">
      <!-- SVG Overlays for glowing polygon boundaries and POI markers -->
      <svg class="map-overlay-polygons" viewBox="0 0 1080 796">
        <!-- Active Dusun Polygons with Glowing PostGIS Borders -->
        <polygon points="260,190 680,180 740,540 310,560" fill="rgba(16, 185, 129, 0.22)" stroke="#059669" stroke-width="3.5" stroke-dasharray="6,4"/>
        <polygon points="680,180 1040,160 1000,520 740,540" fill="rgba(59, 130, 246, 0.14)" stroke="#2563eb" stroke-width="2.5"/>
        <polygon points="310,560 740,540 700,760 280,750" fill="rgba(234, 179, 8, 0.14)" stroke="#d97706" stroke-width="2.5"/>

        <!-- Road labels -->
        <text x="320" y="360" transform="rotate(-32, 320, 360)" fill="#1e293b" font-size="12" font-weight="800" stroke="#ffffff" stroke-width="3" paint-order="stroke fill">Jl. Raya Karangrau</text>
        <text x="680" y="490" fill="#1e293b" font-size="11" font-weight="700" stroke="#ffffff" stroke-width="3" paint-order="stroke fill">Jl. Dusun Krajan</text>
        <text x="760" y="380" transform="rotate(7, 760, 380)" fill="#1d4ed8" font-size="11" font-weight="800">Sungai Pelus</text>

        <!-- Facility Markers (Rich POI with Badges) -->
        <g transform="translate(560, 340)">
          <circle r="18" fill="#ef4444" opacity="0.25"/>
          <circle r="10" fill="#ef4444"/>
          <text x="0" y="4" fill="white" font-size="10" text-anchor="middle" font-weight="800">🏛</text>
          <rect x="18" y="-12" width="130" height="24" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="26" y="4" fill="#0f172a" font-size="10" font-weight="800">Balai Desa Karangrau</text>
        </g>

        <g transform="translate(760, 300)">
          <circle r="14" fill="#10b981" opacity="0.25"/>
          <circle r="8" fill="#10b981"/>
          <rect x="16" y="-10" width="124" height="22" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="24" y="4" fill="#0f172a" font-size="9.5" font-weight="700">Puskesmas Pembantu</text>
        </g>

        <g transform="translate(380, 520)">
          <circle r="14" fill="#3b82f6" opacity="0.25"/>
          <circle r="8" fill="#3b82f6"/>
          <rect x="16" y="-10" width="118" height="22" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
          <text x="24" y="4" fill="#0f172a" font-size="9.5" font-weight="700">SD Negeri Karangrau</text>
        </g>
      </svg>
      <div class="map-zoom-controls">
        <button class="zoom-btn">+</button>
        <button class="zoom-btn">−</button>
        <button class="zoom-btn" title="Pusatkan Peta">⌖</button>
      </div>
      <div class="feature-inspector-popup">
        <div class="inspector-header">
          <span class="inspector-tag">PostGIS Poligon Aktif</span>
          <span style="font-size: 0.75rem; color: #64748b; font-family: 'JetBrains Mono';">ID: GEO-DSN-02</span>
        </div>
        <div class="inspector-title">Dusun II Karangrau (RW 03 & RW 04)</div>
        <p style="font-size: 0.78rem; color: #475569; line-height: 1.45;">
          Kawasan sentra pertanian padi irigasi teknis dan pemukiman warga. Terhubung ke jaringan irigasi sekunder Sungai Pelus.
        </p>
        <div class="inspector-grid">
          <div>
            <div class="attr-val">1,620</div>
            <div class="attr-lbl">Jumlah Warga</div>
          </div>
          <div>
            <div class="attr-val">412 KK</div>
            <div class="attr-lbl">Kepala Keluarga</div>
          </div>
          <div>
            <div class="attr-val">42.8 Ha</div>
            <div class="attr-lbl">Luas Wilayah</div>
          </div>
        </div>
      </div>
      <div class="coords-chip">
        EPSG:4326 | Lat: -7.4294, Lng: 109.2435 | Skala: 1:5,000 | Spatial Index GIST
      </div>
    </div>
  </div>
</body>
</html>
'''

# 2. PANEN TANAM CAMERA AI SCANNER (412x860)
html_panen_tanam_master = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam — AI Crop Monitor</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px;
    background: #09130c; color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  .status-bar {{
    height: 38px; padding: 0 20px;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 0.8rem; font-weight: 600; z-index: 30;
  }}
  .camera-viewport {{
    flex: 1; position: relative;
    background-image: url('file://{rice_asset_path}');
    background-size: cover; background-position: center;
    overflow: hidden; display: flex; align-items: center; justify-content: center;
  }}
  .camera-top-hud {{
    position: absolute; top: 14px; left: 0; right: 0;
    padding: 0 18px; display: flex; justify-content: space-between; align-items: center;
    z-index: 20;
  }}
  .hud-badge {{
    background: rgba(9, 19, 12, 0.75); backdrop-filter: blur(10px);
    border: 1px solid rgba(74, 222, 128, 0.3); color: #86efac;
    font-size: 0.72rem; font-weight: 700; padding: 5px 12px; border-radius: 9999px;
  }}
  .hud-icon-btn {{
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(9, 19, 12, 0.75); backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
  }}
  .ai-target-box {{
    width: 220px; height: 260px;
    position: absolute; top: 110px;
    border: 2px solid #22c55e; border-radius: 18px;
    box-shadow: 0 0 30px rgba(34, 197, 94, 0.5), inset 0 0 15px rgba(34, 197, 94, 0.25);
  }}
  .ai-target-box::before {{
    content: ''; position: absolute; top: -5px; left: -5px;
    width: 18px; height: 18px; border-top: 3.5px solid #4ade80; border-left: 3.5px solid #4ade80;
  }}
  .ai-target-box::after {{
    content: ''; position: absolute; bottom: -5px; right: -5px;
    width: 18px; height: 18px; border-bottom: 3.5px solid #4ade80; border-right: 3.5px solid #4ade80;
  }}
  .ai-label-pill {{
    position: absolute; top: -14px; left: 16px;
    background: #22c55e; color: #052e16;
    font-size: 0.7rem; font-weight: 800; padding: 4px 12px;
    border-radius: 9999px; box-shadow: 0 4px 14px rgba(34, 197, 94, 0.5);
    display: flex; align-items: center; gap: 4px;
  }}
  .diagnostic-sheet {{
    background: rgba(14, 28, 19, 0.96);
    backdrop-filter: blur(24px);
    border-top: 1px solid rgba(74, 222, 128, 0.35);
    border-radius: 26px 26px 0 0;
    padding: 20px 22px 28px;
    display: flex; flex-direction: column; gap: 12px;
    z-index: 30; box-shadow: 0 -12px 36px rgba(0,0,0,0.4);
  }}
  .handle-bar {{
    width: 42px; height: 4px; background: rgba(255, 255, 255, 0.25);
    border-radius: 2px; margin: 0 auto 2px;
  }}
  .diag-title-row {{
    display: flex; justify-content: space-between; align-items: flex-start;
  }}
  .disease-name {{ font-size: 1.15rem; font-weight: 800; color: #ffffff; }}
  .pathogen-name {{ font-size: 0.72rem; color: #86efac; font-style: italic; }}
  .score-badge {{
    background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e;
    color: #4ade80; font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 9999px;
  }}
  .treatment-card {{
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px; padding: 12px 14px;
  }}
  .treatment-tag {{
    font-size: 0.68rem; font-weight: 700; color: #4ade80;
    text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px;
  }}
  .treatment-text {{ font-size: 0.78rem; color: #e2e8f0; line-height: 1.45; }}
  .btn-submit-action {{
    background: #22c55e; color: #052e16; font-size: 0.85rem; font-weight: 800;
    padding: 13px; border-radius: 9999px; border: none; width: 100%;
    box-shadow: 0 4px 16px rgba(34, 197, 94, 0.35); text-align: center;
  }}
</style>
</head>
<body>
  <div class="status-bar">
    <span>09:41</span>
    <span>● 4G &bull; 94%</span>
  </div>
  <div class="camera-viewport">
    <div class="camera-top-hud">
      <div class="hud-icon-btn">⚡</div>
      <div class="hud-badge">Edge NPU 38ms &bull; MobileNetV4</div>
      <div class="hud-icon-btn">⚙</div>
    </div>
    <div class="ai-target-box">
      <div class="ai-label-pill">✓ Hawar Daun Bakteri (98.4%)</div>
    </div>
  </div>
  <div class="diagnostic-sheet">
    <div class="handle-bar"></div>
    <div class="diag-title-row">
      <div>
        <div class="disease-name">Hawar Daun Bakteri (BLB)</div>
        <div class="pathogen-name">Xanthomonas oryzae pv. oryzae</div>
      </div>
      <span class="score-badge">Akurasi 98.4%</span>
    </div>
    <p style="font-size: 0.78rem; color: #94a3b8; line-height: 1.4;">
      Terdeteksi garis basah kekuningan di tepi helai daun padi Ciherang (Fase Awal • Keparahan 22%).
    </p>
    <div class="treatment-card">
      <div class="treatment-tag">Rekomendasi Penanganan Petani:</div>
      <div class="treatment-text">
        Semprotkan bakterisida hayati (Bacillus subtilis) dosis 2.0 ml/L pada pagi hari. Keringkan sawah secara berkala (intermittent irrigation) untuk memutus kelembaban spora.
      </div>
    </div>
    <div class="btn-submit-action">Catat ke Riwayat Perawatan Petak Sawah</div>
  </div>
</body>
</html>
'''

# 3. GEODIPA SPK MASTER TEMPLATE (1366x768)
html_geodipa_master = '''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Geodipa SPK — Evaluasi Kinerja Pegawai (SAW)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }
  header {
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .brand { display: flex; align-items: center; gap: 12px; }
  .logo-box {
    width: 36px; height: 36px; background: #0369a1; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.05rem;
  }
  .app-name { font-size: 0.98rem; font-weight: 800; color: #0f172a; }
  .app-sub { font-size: 0.72rem; color: #64748b; }
  .layout { flex: 1; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .kpi-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 12px 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
  }
  .kpi-val { font-size: 1.35rem; font-weight: 800; color: #0f172a; }
  .kpi-lbl { font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 2px; }
  .table-card {
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  }
  .table-top {
    padding: 12px 20px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  th {
    background: #f8fafc; padding: 11px 16px; font-weight: 700; color: #475569;
    font-size: 0.72rem; text-transform: uppercase; border-bottom: 1px solid #e2e8f0;
    text-align: left;
  }
  td { padding: 11px 16px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .rank-badge {
    width: 26px; height: 26px; border-radius: 50%; display: inline-flex;
    align-items: center; justify-content: center; font-weight: 800; font-size: 0.75rem;
  }
  .rank-1 { background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; }
  .rank-2 { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
  .rank-3 { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
  .dept-pill {
    background: #f1f5f9; color: #475569; font-size: 0.7rem; font-weight: 600;
    padding: 3px 9px; border-radius: 9999px;
  }
  .score-val { font-family: 'JetBrains Mono'; font-weight: 700; color: #0284c7; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="logo-box">GD</div>
      <div>
        <div class="app-name">Sistem Pendukung Keputusan Karyawan Terbaik (SPK SAW)</div>
        <div class="app-sub">PT Geo Dipa Energi (Persero) &bull; Evaluasi Kinerja Semester I</div>
      </div>
    </div>
    <div style="font-size: 0.78rem; font-weight: 700; background: #e0f2fe; color: #0369a1; padding: 6px 14px; border-radius: 8px;">
      Metode: Simple Additive Weighting (SAW)
    </div>
  </header>
  <div class="layout">
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-val">148</div>
        <div class="kpi-lbl">Total Pegawai Terdaftar</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">5 Kriteria</div>
        <div class="kpi-lbl">Bobot SAW Terstandar</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val" style="color: #0369a1;">0.942</div>
        <div class="kpi-lbl">Skor Preferensi Tertinggi</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">100%</div>
        <div class="kpi-lbl">Kelengkapan Peer-Review</div>
      </div>
    </div>
    <div class="table-card">
      <div class="table-top">
        <b style="font-size: 0.88rem; color: #0f172a;">Hasil Peringkat Evaluasi Karyawan Terbaik</b>
        <span style="font-size: 0.72rem; color: #64748b;">Kriteria: Disiplin (25%), Kinerja (30%), Kepemimpinan (20%), Kerjasama (15%), Inisiatif (10%)</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Peringkat</th>
            <th>Nama Pegawai</th>
            <th>NIP</th>
            <th>Divisi</th>
            <th>C1 (25%)</th>
            <th>C2 (30%)</th>
            <th>C3 (20%)</th>
            <th>C4 (15%)</th>
            <th>C5 (10%)</th>
            <th>Skor SAW (Vi)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="rank-badge rank-1">1</span></td>
            <td><b>Rizky Pratama, S.T.</b></td>
            <td>198804122019</td>
            <td><span class="dept-pill">Operasi Pembangkit</span></td>
            <td>95</td><td>94</td><td>90</td><td>92</td><td>96</td>
            <td class="score-val">0.942</td>
          </tr>
          <tr>
            <td><span class="rank-badge rank-2">2</span></td>
            <td><b>Anisa Wulandari, S.E.</b></td>
            <td>199208152020</td>
            <td><span class="dept-pill">Keuangan &amp; SDM</span></td>
            <td>92</td><td>95</td><td>88</td><td>94</td><td>90</td>
            <td class="score-val">0.926</td>
          </tr>
          <tr>
            <td><span class="rank-badge rank-3">3</span></td>
            <td><b>Budi Santoso, A.Md.</b></td>
            <td>198501202018</td>
            <td><span class="dept-pill">Pemeliharaan Turbin</span></td>
            <td>90</td><td>92</td><td>92</td><td>88</td><td>88</td>
            <td class="score-val">0.908</td>
          </tr>
          <tr>
            <td><span class="rank-badge" style="background:#f1f5f9; color:#64748b; border:1px solid #cbd5e1;">4</span></td>
            <td><b>Dwi Handoko, S.T.</b></td>
            <td>199011032019</td>
            <td><span class="dept-pill">Health, Safety &amp; Env</span></td>
            <td>88</td><td>90</td><td>86</td><td>90</td><td>85</td>
            <td class="score-val">0.884</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
'''

# 4. STOCK MANAGEMENT (BGE) MASTER TEMPLATE (1366x768)
html_bge_master = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>BGE Supply — Stock & Shopify Inventory Sync</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  header {{
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px;
  }}
  .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.05rem; }}
  .sync-pill {{
    background: #ecfdf5; border: 1px solid #a7f3d0; color: #059669;
    font-size: 0.72rem; font-weight: 700; padding: 4px 12px; border-radius: 9999px;
  }}
  .layout {{ flex: 1; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }}
  .kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
  .kpi {{
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 12px 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
  }}
  .kpi-val {{ font-size: 1.35rem; font-weight: 800; color: #0f172a; }}
  .kpi-lbl {{ font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 2px; }}
  .table-box {{
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  .table-nav {{
    padding: 12px 20px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left; }}
  th {{
    background: #f8fafc; padding: 11px 16px; font-weight: 700; color: #475569;
    font-size: 0.72rem; border-bottom: 1px solid #e2e8f0;
  }}
  td {{ padding: 11px 16px; border-bottom: 1px solid #f1f5f9; color: #334155; }}
  .sku-badge {{ font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #64748b; }}
  .thumb-img {{ width: 34px; height: 34px; border-radius: 6px; object-fit: cover; vertical-align: middle; margin-right: 8px; }}
  .sync-ok {{ display: inline-flex; align-items: center; gap: 4px; font-size: 0.72rem; font-weight: 700; color: #059669; }}
</style>
</head>
<body>
  <header>
    <div class="brand">
      <span>📦</span>
      <span>BGE Supply — Warehouse Stock &amp; Shopify Multi-Store Sync</span>
    </div>
    <div class="sync-pill">
      ● Shopify Webhook Connected (Two-Way Auto Sync)
    </div>
  </header>
  <div class="layout">
    <div class="kpi-row">
      <div class="kpi">
        <div class="kpi-val">1,248</div>
        <div class="kpi-lbl">Total SKU Produk</div>
      </div>
      <div class="kpi">
        <div class="kpi-val" style="color: #d97706;">14 SKU</div>
        <div class="kpi-lbl">Peringatan Stok Menipis</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">284 pcs</div>
        <div class="kpi-lbl">Barang dalam Pengiriman</div>
      </div>
      <div class="kpi">
        <div class="kpi-val" style="color: #059669;">99.8%</div>
        <div class="kpi-lbl">Akurasi Stok Toko &amp; Online</div>
      </div>
    </div>
    <div class="table-box">
      <div class="table-nav">
        <b style="font-size: 0.88rem; color: #0f172a;">Katalog Inventaris &amp; Alokasi Saluran Penjualan</b>
        <span style="font-size: 0.72rem; color: #64748b;">Sinkronisasi otomatis dengan API Toko Online</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Nama Produk &amp; Varian</th>
            <th>Kategori</th>
            <th>Gudang Pusat</th>
            <th>Toko Offline</th>
            <th>Alokasi Shopify</th>
            <th>Total Kuantitas</th>
            <th>Status Sinkronisasi</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="sku-badge">BGE-TEE-BLK-L</span></td>
            <td><img class="thumb-img" src="file://{RENDER_DIR}/bge_tee.jpg"><b>Heavyweight Oversized Tee - Black (L)</b></td>
            <td>Apparel</td>
            <td>42 pcs</td><td>18 pcs</td><td>34 pcs</td>
            <td><b>94 pcs</b></td>
            <td><span class="sync-ok">✓ Tersinkron</span></td>
          </tr>
          <tr>
            <td><span class="sku-badge">BGE-DNM-IND-32</span></td>
            <td><img class="thumb-img" src="file://{RENDER_DIR}/bge_denim.jpg"><b>Raw Selvedge Denim 14oz - Indigo (32)</b></td>
            <td>Pants</td>
            <td>16 pcs</td><td>6 pcs</td><td>12 pcs</td>
            <td><b>34 pcs</b></td>
            <td><span class="sync-ok">✓ Tersinkron</span></td>
          </tr>
          <tr>
            <td><span class="sku-badge">BGE-HOD-GRY-XL</span></td>
            <td><img class="thumb-img" src="file://{RENDER_DIR}/bge_hoodie.jpg"><b>French Terry Pullover Hoodie - Grey (XL)</b></td>
            <td>Outerwear</td>
            <td>5 pcs</td><td>2 pcs</td><td>4 pcs</td>
            <td><b style="color:#d97706;">11 pcs (Stok Menipis)</b></td>
            <td><span class="sync-ok">✓ Tersinkron</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
'''

# 5. KLASIFIKASI STUNTING (CHILDER) MASTER TEMPLATE (1366x768)
html_stunting_master = '''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Childer Growth Guardian — Skrining & Klasifikasi Stunting</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }
  header {
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px;
  }
  .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.05rem; }
  .layout { flex: 1; padding: 20px 24px; display: grid; grid-template-columns: 380px 1fr; gap: 20px; overflow: hidden; }
  .card {
    background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 20px; display: flex; flex-direction: column; gap: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  }
  .card-title { font-size: 0.95rem; font-weight: 800; color: #0f172a; }
  .form-group { display: flex; flex-direction: column; gap: 5px; }
  .form-lbl { font-size: 0.74rem; font-weight: 700; color: #475569; }
  .form-input {
    padding: 9px 12px; border: 1px solid #cbd5e1; border-radius: 8px;
    font-size: 0.85rem; font-family: inherit; outline: none; background: #f8fafc;
  }
  .result-banner {
    background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px;
    padding: 14px 16px; margin-top: auto;
  }
  .result-tag { font-size: 0.68rem; font-weight: 800; color: #059669; text-transform: uppercase; }
  .result-val { font-size: 1.15rem; font-weight: 800; color: #064e3b; margin: 2px 0; }
  .chart-canvas {
    flex: 1; position: relative; background: #ffffff;
    border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;
    display: flex; flex-direction: column;
  }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <span>👶</span>
      <span>Childer — Portal Deteksi Dini &amp; Skrining Pertumbuhan Balita</span>
    </div>
    <div style="font-size: 0.75rem; color: #0369a1; background: #e0f2fe; padding: 5px 12px; border-radius: 9999px; font-weight: 700;">
      Model: Artificial Neural Network (Standard Deviasi WHO)
    </div>
  </header>
  <div class="layout">
    <div class="card">
      <div class="card-title">Parameter Antropometri Balita</div>
      <div class="form-group">
        <label class="form-lbl">Nama Balita</label>
        <input class="form-input" value="Muhammad Al-Fatih">
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="form-group">
          <label class="form-lbl">Usia (Bulan)</label>
          <input class="form-input" value="24 Bulan">
        </div>
        <div class="form-group">
          <label class="form-lbl">Jenis Kelamin</label>
          <input class="form-input" value="Laki-laki">
        </div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="form-group">
          <label class="form-lbl">Tinggi Badan (cm)</label>
          <input class="form-input" value="86.5 cm">
        </div>
        <div class="form-group">
          <label class="form-lbl">Berat Badan (kg)</label>
          <input class="form-input" value="12.1 kg">
        </div>
      </div>
      <div class="result-banner">
        <div class="result-tag">Hasil Klasifikasi Model ANN (Akurasi 96.2%)</div>
        <div class="result-val">Gizi Baik • Tinggi Badan Normal</div>
        <p style="font-size: 0.75rem; color: #047857;">Z-Score Height-for-Age: -0.42 SD (Dalam batas median standar WHO).</p>
      </div>
    </div>
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div class="card-title">Kurva Pertumbuhan Standar WHO (Tinggi Badan menurut Umur)</div>
        <span style="font-size: 0.72rem; color: #64748b;">Plot Pasien: Usia 24 Bulan &bull; 86.5 cm</span>
      </div>
      <div class="chart-canvas">
        <svg width="100%" height="100%" viewBox="0 0 800 500">
          <!-- WHO percentile bands -->
          <polygon points="60,420 740,160 740,240 60,440" fill="#fef3c7" opacity="0.6"/>
          <polygon points="60,440 740,240 740,320 60,460" fill="#dcfce7" opacity="0.8"/>
          <!-- +2 SD, Median, -2 SD curves -->
          <path d="M 60,410 Q 400,280 740,160" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
          <path d="M 60,435 Q 400,315 740,215" fill="none" stroke="#10b981" stroke-width="3"/>
          <path d="M 60,460 Q 400,350 740,270" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="4,4"/>
          <!-- Patient Point -->
          <circle cx="400" cy="318" r="8" fill="#0284c7" stroke="#ffffff" stroke-width="3"/>
          <text x="415" y="322" font-size="12" font-weight="800" fill="#0369a1">Pasien (86.5 cm, Normal)</text>
          <!-- Axis labels -->
          <text x="60" y="485" font-size="11" fill="#64748b">0 Bulan</text>
          <text x="390" y="485" font-size="11" fill="#64748b">24 Bulan</text>
          <text x="710" y="485" font-size="11" fill="#64748b">48 Bulan</text>
        </svg>
      </div>
    </div>
  </div>
</body>
</html>
'''

# Write templates
templates = [
    ('sig_desa_master.html', html_sig_desa_master, f'{SCREENSHOT_DIR}/sig_desa.png', '1440,860'),
    ('panen_tanam_master.html', html_panen_tanam_master, f'{SCREENSHOT_DIR}/panen_tanam_scan.png', '412,860'),
    ('geodipa_master.html', html_geodipa_master, f'{SCREENSHOT_DIR}/geodipa_spk.png', '1366,768'),
    ('bge_master.html', html_bge_master, f'{SCREENSHOT_DIR}/stock_management_bge.png', '1366,768'),
    ('stunting_master.html', html_stunting_master, f'{SCREENSHOT_DIR}/klasifikasi_stunting.png', '1366,768')
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

print("All Master Screenshots Rendered Successfully!")
'''

with open(f'{RENDER_DIR}/generate_all_master_screenshots.py', 'w', encoding='utf-8') as f:
    f.write(html_sig_desa_master)
