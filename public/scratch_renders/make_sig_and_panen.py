import os
import subprocess

RENDER_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders'
SC_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots'
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(SC_DIR, exist_ok=True)
os.makedirs('/tmp/ff_master_profile', exist_ok=True)

def render(html_content, fname, out_png, dims):
    hpath = os.path.join(RENDER_DIR, fname)
    with open(hpath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    cmd = [
        'firefox', '--headless',
        '-profile', '/tmp/ff_master_profile',
        '--screenshot', out_png,
        f'--window-size={dims}',
        f'file://{hpath}'
    ]
    print(f"Rendering {fname} -> {os.path.basename(out_png)} ({dims})...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error {fname}: {res.stderr[:200]}")
    else:
        print(f"  ✅ Rendered {os.path.basename(out_png)}")

# -----------------------------------------------------------------------------
# 1. SIG Desa: Main GIS Map (1440x860)
# -----------------------------------------------------------------------------
sig_desa_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa Karangrau — Peta Geospasial & Leaflet</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1440px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a;
    color: #1e293b;
    display: flex; flex-direction: column;
    overflow: hidden;
  }}
  header {{
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; z-index: 30; box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }}
  .brand {{ display: flex; align-items: center; gap: 12px; }}
  .brand-logo {{
    width: 36px; height: 36px; background: #166534; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.1rem;
  }}
  .brand-title {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; }}
  .brand-sub {{ font-size: 0.72rem; color: #64748b; font-weight: 500; }}
  .header-badges {{ display: flex; align-items: center; gap: 10px; }}
  .pill {{ font-size: 0.72rem; font-weight: 600; padding: 4px 10px; border-radius: 9999px; }}
  .pill-tenant {{ background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }}
  .pill-db {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-family: 'JetBrains Mono', monospace; }}

  .map-viewport {{
    flex: 1; position: relative; overflow: hidden;
    background: url('file://{RENDER_DIR}/indonesian_village_gis_aerial.jpg') center/cover no-repeat;
  }}

  /* Dark Vignette Overlay for Crisp UI Legibility */
  .map-overlay-tint {{
    position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.05) 0%, rgba(15, 23, 42, 0.25) 100%);
    pointer-events: none;
  }}

  /* SVG Vector Polygons Overlay */
  .vector-layer {{
    position: absolute; inset: 0; width: 100%; height: 100%;
    pointer-events: none;
  }}

  /* Left Floating GIS Control Panel */
  .gis-panel {{
    position: absolute; top: 20px; left: 24px; width: 340px;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.22);
    padding: 18px; z-index: 20;
    display: flex; flex-direction: column; gap: 14px;
  }}
  .search-box {{
    display: flex; align-items: center; gap: 8px;
    background: #f1f5f9; border: 1px solid #cbd5e1;
    border-radius: 10px; padding: 8px 12px;
  }}
  .search-box input {{
    border: none; background: transparent; outline: none;
    font-size: 0.8rem; font-family: inherit; width: 100%;
  }}
  .layer-group {{ display: flex; flex-direction: column; gap: 8px; }}
  .layer-title {{ font-size: 0.72rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.5px; }}
  .layer-item {{
    display: flex; align-items: center; justify-content: space-between;
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 8px 12px; font-size: 0.78rem; font-weight: 600;
  }}
  .layer-check {{ width: 15px; height: 15px; accent-color: #166534; }}
  
  .feature-card {{
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 12px; font-size: 0.75rem;
  }}
  .feature-head {{ font-weight: 800; color: #0f172a; margin-bottom: 4px; font-size: 0.82rem; }}
  .feature-row {{ display: flex; justify-content: space-between; margin-top: 4px; color: #64748b; }}
  .feature-val {{ font-weight: 700; color: #0f172a; }}

  /* Custom Leaflet Pin Markers */
  .pin-marker {{
    position: absolute; transform: translate(-50%, -100%);
    display: flex; flex-direction: column; align-items: center;
    cursor: pointer; z-index: 15;
  }}
  .pin-icon {{
    width: 32px; height: 32px; border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    border: 2px solid #ffffff;
  }}
  .pin-icon span {{ transform: rotate(45deg); font-size: 14px; }}
  .pin-blue {{ background: #2563eb; color: white; }}
  .pin-red {{ background: #dc2626; color: white; }}
  .pin-green {{ background: #16a34a; color: white; }}
  .pin-amber {{ background: #d97706; color: white; }}

  /* Interactive Popup */
  .pin-popup {{
    position: absolute; bottom: 42px; left: 50%; transform: translateX(-50%);
    background: #ffffff; border-radius: 10px; padding: 10px 14px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.25);
    white-space: nowrap; font-size: 0.75rem; border: 1px solid #e2e8f0;
    z-index: 25;
  }}
  .popup-title {{ font-weight: 800; color: #0f172a; margin-bottom: 2px; }}
  .popup-sub {{ color: #64748b; font-size: 0.7rem; }}

  /* Leaflet Controls & Coordinates Bar */
  .leaflet-ctrl {{
    position: absolute; top: 20px; right: 24px;
    display: flex; flex-direction: column; gap: 8px; z-index: 20;
  }}
  .ctrl-btn {{
    width: 38px; height: 38px; background: white; border-radius: 10px;
    border: 1px solid #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 800; color: #334155;
  }}
  .bottom-bar {{
    position: absolute; bottom: 16px; right: 24px;
    background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
    color: #e2e8f0; font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; padding: 6px 14px; border-radius: 8px;
    display: flex; gap: 16px; border: 1px solid rgba(255,255,255,0.15);
  }}
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-logo">SIG</div>
      <div>
        <div class="brand-title">SIG Desa Karangrau — Sistem Geospasial & Pemetaan Wilayah</div>
        <div class="brand-sub">Kecamatan Banyumas • Kabupaten Banyumas • Jawa Tengah</div>
      </div>
    </div>
    <div class="header-badges">
      <span class="pill pill-tenant">📍 Tenant: Desa Karangrau</span>
      <span class="pill pill-db">PostGIS 16 &bull; Leaflet 1.9 &bull; EPSG:4326</span>
    </div>
  </header>

  <div class="map-viewport">
    <div class="map-overlay-tint"></div>

    <!-- Polygons -->
    <svg class="vector-layer" viewBox="0 0 1440 800">
      <!-- Dusun 1 Polygon -->
      <polygon points="420,120 720,90 890,260 680,480 390,380" 
               fill="rgba(16, 185, 129, 0.22)" stroke="#10b981" stroke-width="3" stroke-dasharray="6,4"/>
      <text x="560" y="270" fill="#ffffff" font-size="14" font-weight="800" text-shadow="0 2px 4px rgba(0,0,0,0.8)">Dusun I (Karangrau Wetan)</text>
      
      <!-- Dusun 2 Polygon -->
      <polygon points="680,480 890,260 1260,340 1340,640 880,720" 
               fill="rgba(245, 158, 11, 0.22)" stroke="#f59e0b" stroke-width="3" stroke-dasharray="6,4"/>
      <text x="960" y="490" fill="#ffffff" font-size="14" font-weight="800" text-shadow="0 2px 4px rgba(0,0,0,0.8)">Dusun II (Karangrau Kulon)</text>

      <!-- Irrigated Rice Zone -->
      <polygon points="390,380 680,480 880,720 480,760 280,560" 
               fill="rgba(59, 130, 246, 0.20)" stroke="#3b82f6" stroke-width="3"/>
      <text x="460" y="610" fill="#ffffff" font-size="13" font-weight="700" text-shadow="0 2px 4px rgba(0,0,0,0.8)">Zonasi Sawah Irigasi Pelus (84.5 Ha)</text>
    </svg>

    <!-- Pins -->
    <div class="pin-marker" style="top: 320px; left: 620px;">
      <div class="pin-icon pin-blue"><span>🏛️</span></div>
      <div class="pin-popup">
        <div class="popup-title">Balai Desa Karangrau</div>
        <div class="popup-sub">Pusat Layanan Administrasi Warga</div>
      </div>
    </div>

    <div class="pin-marker" style="top: 240px; left: 810px;">
      <div class="pin-icon pin-red"><span>🏥</span></div>
    </div>

    <div class="pin-marker" style="top: 520px; left: 1040px;">
      <div class="pin-icon pin-green"><span>🌾</span></div>
    </div>

    <div class="pin-marker" style="top: 410px; left: 470px;">
      <div class="pin-icon pin-amber"><span>🏫</span></div>
    </div>

    <!-- GIS Left Floating Panel -->
    <div class="gis-panel">
      <div class="search-box">
        <span>🔍</span>
        <input type="text" value="Dusun I (Karangrau Wetan)" placeholder="Cari batas wilayah...">
      </div>

      <div class="layer-group">
        <div class="layer-title">Layer Spasial Aktif</div>
        <div class="layer-item">
          <span>🌿 Batas Dusun & Wilayah</span>
          <input type="checkbox" class="layer-check" checked>
        </div>
        <div class="layer-item">
          <span>💧 Zonasi Irigasi & Pertanian</span>
          <input type="checkbox" class="layer-check" checked>
        </div>
        <div class="layer-item">
          <span>📍 Fasilitas & Objek Penting</span>
          <input type="checkbox" class="layer-check" checked>
        </div>
      </div>

      <div class="feature-card">
        <div class="feature-head">Detail Objek Terpilih</div>
        <div class="feature-row"><span>Nama Wilayah:</span><span class="feature-val">Dusun I Karangrau</span></div>
        <div class="feature-row"><span>Luas Spasial:</span><span class="feature-val">68.4 Hektar</span></div>
        <div class="feature-row"><span>Jumlah KK:</span><span class="feature-val">412 Kepala Keluarga</span></div>
        <div class="feature-row"><span>Status Irigasi:</span><span class="feature-val">Irigasi Teknis Padi</span></div>
      </div>
    </div>

    <!-- Controls -->
    <div class="leaflet-ctrl">
      <div class="ctrl-btn">+</div>
      <div class="ctrl-btn">&minus;</div>
      <div class="ctrl-btn">🧭</div>
      <div class="ctrl-btn">📐</div>
    </div>

    <!-- Coordinates -->
    <div class="bottom-bar">
      <span>LAT: -7.47214</span>
      <span>LONG: 109.28190</span>
      <span>ZOOM: 16</span>
      <span>SRID: EPSG:4326</span>
    </div>
  </div>
</body>
</html>
"""

render(sig_desa_html, 'sig_desa.html', f'{SC_DIR}/sig_desa.png', '1440,860')


# -----------------------------------------------------------------------------
# 2. SIG Desa: Spatial Editor (1440x860)
# -----------------------------------------------------------------------------
sig_editor_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa — PostGIS Spatial Polygon Editor</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1440px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0b1120; color: #f8fafc;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  header {{
    height: 56px; background: #0f172a; border-bottom: 1px solid #1e293b;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 20px;
  }}
  .tool-row {{ display: flex; align-items: center; gap: 8px; }}
  .btn-tool {{
    background: #1e293b; border: 1px solid #334155; color: #e2e8f0;
    padding: 6px 14px; border-radius: 8px; font-size: 0.78rem; font-weight: 600;
    display: flex; align-items: center; gap: 6px;
  }}
  .btn-active {{ background: #166534; border-color: #22c55e; color: #ffffff; }}
  .btn-save {{ background: #2563eb; border-color: #3b82f6; color: #ffffff; }}
  
  .layout-body {{ flex: 1; display: flex; overflow: hidden; }}
  .canvas-area {{
    flex: 1; position: relative;
    background: url('file://{RENDER_DIR}/indonesian_village_gis_aerial.jpg') center/cover no-repeat;
  }}
  .side-inspector {{
    width: 360px; background: #0f172a; border-left: 1px solid #1e293b;
    padding: 20px; display: flex; flex-direction: column; gap: 16px;
  }}
  .field-group {{ display: flex; flex-direction: column; gap: 6px; }}
  .field-lbl {{ font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; }}
  .field-input {{
    background: #1e293b; border: 1px solid #334155; border-radius: 8px;
    padding: 8px 12px; font-size: 0.8rem; color: #ffffff; font-family: inherit;
  }}
  .code-block {{
    background: #020617; border: 1px solid #1e293b; border-radius: 8px;
    padding: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
    color: #38bdf8; overflow: hidden;
  }}
</style>
</head>
<body>
  <header>
    <div class="tool-row">
      <span style="font-weight: 800; font-size: 0.95rem; color: #38bdf8;">PostGIS Geosegment Editor</span>
      <span style="font-size: 0.75rem; color: #64748b;">| Layer: Poligon Batas Dusun</span>
    </div>
    <div class="tool-row">
      <div class="btn-tool btn-active">✏ Edit Vertex Node (Snap)</div>
      <div class="btn-tool">➕ Tambah Poligon</div>
      <div class="btn-tool">✂ Split Geometry</div>
      <div class="btn-tool btn-save">💾 Simpan ke Database (PostGIS)</div>
    </div>
  </header>
  <div class="layout-body">
    <div class="canvas-area">
      <svg style="position: absolute; inset: 0; width: 100%; height: 100%;" viewBox="0 0 1080 804">
        <polygon points="260,140 620,110 780,280 580,520 220,410" 
                 fill="rgba(56, 189, 248, 0.28)" stroke="#38bdf8" stroke-width="3"/>
        <!-- Edit Vertex Handles -->
        <circle cx="260" cy="140" r="7" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
        <circle cx="620" cy="110" r="7" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
        <circle cx="780" cy="280" r="7" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
        <circle cx="580" cy="520" r="7" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
        <circle cx="220" cy="410" r="7" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
        
        <!-- Active drag indicator -->
        <circle cx="780" cy="280" r="14" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,3"/>
      </svg>
    </div>
    <div class="side-inspector">
      <div style="font-weight: 800; font-size: 0.9rem; color: #ffffff; border-bottom: 1px solid #1e293b; padding-bottom: 10px;">
        Inspektor Geometri PostGIS
      </div>
      <div class="field-group">
        <div class="field-lbl">Nama Wilayah Spasial</div>
        <input class="field-input" value="Dusun I (Karangrau Wetan)">
      </div>
      <div class="field-group">
        <div class="field-lbl">Kode Administrasi Kemendagri</div>
        <input class="field-input" value="33.02.12.2001.01">
      </div>
      <div class="field-group">
        <div class="field-lbl">Kalkulasi Luas Poligon (ST_Area)</div>
        <input class="field-input" value="684,210.4 m² (68.42 Ha)">
      </div>
      <div class="field-group">
        <div class="field-lbl">Topologi Check (ST_IsValid)</div>
        <div style="background: #052e16; border: 1px solid #166534; color: #4ade80; padding: 8px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700;">
          ✓ Poligon Valid (Zero Self-Intersection)
        </div>
      </div>
      <div class="field-group">
        <div class="field-lbl">WKT Export (Well-Known Text)</div>
        <div class="code-block">
POLYGON((109.2811 -7.4720, 109.2845 -7.4715, 109.2862 -7.4735, 109.2838 -7.4760, 109.2805 -7.4748, 109.2811 -7.4720))
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(sig_editor_html, 'sig_editor.html', f'{SC_DIR}/sig_desa_spatial_editor.png', '1440,860')


# -----------------------------------------------------------------------------
# 3. SIG Desa: Resident Portal (1440x860)
# -----------------------------------------------------------------------------
sig_portal_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Portal Kependudukan & Layanan Desa Karangrau</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1440px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  header {{
    height: 70px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px;
  }}
  .hero-banner {{
    background: linear-gradient(135deg, #166534 0%, #15803d 100%);
    color: white; padding: 40px; margin: 24px 40px 0; border-radius: 20px;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .stats-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
    margin: 24px 40px;
  }}
  .stat-card {{
    background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);
  }}
  .stat-num {{ font-size: 1.8rem; font-weight: 800; color: #0f172a; }}
  .stat-lbl {{ font-size: 0.8rem; color: #64748b; font-weight: 600; margin-top: 4px; }}
</style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 14px;">
      <div style="width: 42px; height: 42px; background: #166534; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.2rem;">K</div>
      <div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a;">Portal Informasi Desa Karangrau</div>
        <div style="font-size: 0.78rem; color: #64748b;">Kecamatan Banyumas, Kabupaten Banyumas</div>
      </div>
    </div>
    <div style="font-size: 0.82rem; font-weight: 700; background: #f0fdf4; color: #166534; padding: 8px 18px; border-radius: 9999px; border: 1px solid #bbf7d0;">
      🌐 Layanan Publik Terbuka
    </div>
  </header>

  <div class="hero-banner">
    <div>
      <h1 style="font-size: 1.8rem; font-weight: 800;">Transparansi Data & Profil Geospasial Desa</h1>
      <p style="margin-top: 8px; font-size: 0.95rem; opacity: 0.9; max-width: 650px;">
        Penyajian data profil kependudukan, statistik wilayah pertanian, dan akses peta batas administrasi terpadu berbasis Open Source GIS.
      </p>
    </div>
    <div style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); padding: 16px 24px; border-radius: 14px; text-align: center;">
      <div style="font-size: 2rem; font-weight: 800;">4 Dusun</div>
      <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9;">18 RT &bull; 4 RW</div>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-num">3,482 Jiwa</div>
      <div class="stat-lbl">Total Populasi Penduduk</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">1,024 KK</div>
      <div class="stat-lbl">Kepala Keluarga Terdaftar</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">248.5 Ha</div>
      <div class="stat-lbl">Luas Teritorial Geografis</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">142.8 Ha</div>
      <div class="stat-lbl">Lahan Sawah Produktif</div>
    </div>
  </div>
</body>
</html>
"""

render(sig_portal_html, 'sig_portal.html', f'{SC_DIR}/sig_desa_resident_portal.png', '1440,860')


# -----------------------------------------------------------------------------
# 4. Panen Tanam: AI Camera Scanner (412x860)
# -----------------------------------------------------------------------------
panen_scan_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam — AI Camera Vision</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #000000; color: #ffffff;
    display: flex; flex-direction: column; overflow: hidden;
    position: relative;
  }}
  /* Camera Feed */
  .camera-feed {{
    position: absolute; inset: 0;
    background: url('file://{RENDER_DIR}/rice_leaf_blight_macro.jpg') center/cover no-repeat;
  }}

  /* Top Status & Controls */
  .camera-header {{
    position: relative; z-index: 20; padding: 42px 18px 14px;
    display: flex; justify-content: space-between; align-items: center;
    background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, transparent 100%);
  }}
  .btn-icon {{
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(0,0,0,0.45); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1rem;
  }}
  .loc-pill {{
    background: rgba(0,0,0,0.5); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 6px 14px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
  }}

  /* AI Bounding Box & HUD */
  .scan-hud {{
    position: absolute; top: 180px; left: 46px; width: 320px; height: 360px;
    border: 2px dashed rgba(34, 197, 94, 0.85);
    border-radius: 18px; box-shadow: 0 0 25px rgba(34, 197, 94, 0.35);
    z-index: 10;
  }}
  .laser-line {{
    position: absolute; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #4ade80, transparent);
    box-shadow: 0 0 10px #22c55e;
    top: 55%;
  }}
  .detection-pill {{
    position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
    background: #166534; border: 1.5px solid #4ade80;
    color: #ffffff; padding: 5px 12px; border-radius: 9999px;
    font-size: 0.72rem; font-weight: 800; white-space: nowrap;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  }}

  /* Bottom Drawer Diagnostic */
  .bottom-drawer {{
    position: absolute; bottom: 0; left: 0; right: 0; z-index: 20;
    background: rgba(18, 28, 20, 0.94); backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255,255,255,0.2);
    border-radius: 24px 24px 0 0;
    padding: 20px 20px 32px;
    display: flex; flex-direction: column; gap: 14px;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
  }}
  .drawer-handle {{
    width: 36px; height: 4px; background: rgba(255,255,255,0.3);
    border-radius: 9999px; margin: 0 auto 4px;
  }}
  .result-title {{ font-size: 1.05rem; font-weight: 800; color: #4ade80; }}
  .result-meta {{ font-size: 0.72rem; color: #cbd5e1; font-weight: 500; line-height: 1.4; }}
  .btn-action {{
    background: #22c55e; color: #052e16; font-weight: 800;
    padding: 12px; border-radius: 12px; border: none; font-size: 0.85rem;
    text-align: center;
  }}
</style>
</head>
<body>
  <div class="camera-feed"></div>

  <div class="camera-header">
    <div class="btn-icon">✕</div>
    <div class="loc-pill">📍 Kemranjen, Banyumas</div>
    <div class="btn-icon">⚡</div>
  </div>

  <div class="scan-hud">
    <div class="detection-pill">🔍 Xanthomonas oryzae (BLB) &bull; 96.8%</div>
    <div class="laser-line"></div>
  </div>

  <div class="bottom-drawer">
    <div class="drawer-handle"></div>
    <div>
      <div class="result-title">Hawar Daun Bakteri (Bacterial Leaf Blight)</div>
      <div class="result-meta" style="margin-top: 4px;">
        Terdeteksi gejala garis kekuningan pada tepian daun padi. Tingkat risiko: Sedang.
      </div>
    </div>

    <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 10px 14px; font-size: 0.72rem; color: #e2e8f0;">
      <span style="color: #4ade80; font-weight: 700;">Tindakan Cepat:</span> Pengeringan sawah berkala & kurangi pupuk N. Semprot Bakterisida berbahan aktif Tembaga Oksiklorida.
    </div>

    <button class="btn-action">Lihat Dosis Rekomendasi Per Hektar ➔</button>
  </div>
</body>
</html>
"""

render(panen_scan_html, 'panen_scan.html', f'{SC_DIR}/panen_tanam_scan.png', '412,860')


# -----------------------------------------------------------------------------
# 5. Panen Tanam: Mobile Dashboard / Home (412x860)
# -----------------------------------------------------------------------------
panen_home_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam — Mobile Android App</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #0f172a;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  .app-bar {{
    padding: 38px 20px 16px; background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .app-name {{ font-size: 1.15rem; font-weight: 800; color: #166534; }}
  .content-scroll {{ flex: 1; padding: 18px 20px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }}
  
  .weather-card {{
    background: linear-gradient(135deg, #166534 0%, #15803d 100%);
    color: white; border-radius: 18px; padding: 18px;
    box-shadow: 0 10px 20px -5px rgba(22, 101, 52, 0.28);
  }}
  .weather-temp {{ font-size: 2rem; font-weight: 800; }}
  .weather-alert {{
    background: rgba(254, 240, 138, 0.2); border: 1px solid #fef08a;
    color: #fef08a; padding: 6px 10px; border-radius: 8px;
    font-size: 0.72rem; font-weight: 700; margin-top: 10px;
  }}

  .scan-cta-card {{
    background: #ffffff; border: 2px dashed #22c55e; border-radius: 16px;
    padding: 18px; text-align: center;
  }}
  .scan-btn {{
    background: #166534; color: white; border: none;
    padding: 12px 20px; border-radius: 12px; font-weight: 800;
    font-size: 0.85rem; width: 100%; margin-top: 10px;
  }}

  .plot-item {{
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 14px; display: flex; justify-content: space-between; align-items: center;
  }}
  
  .bottom-nav {{
    height: 64px; background: #ffffff; border-top: 1px solid #e2e8f0;
    display: grid; grid-template-columns: repeat(4, 1fr);
    align-items: center; text-align: center; font-size: 0.68rem; font-weight: 700; color: #64748b;
  }}
  .nav-active {{ color: #166534; }}
</style>
</head>
<body>
  <div class="app-bar">
    <div>
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">Wilayah Banyumas &bull; MT I</div>
      <div class="app-name">🌾 Panen Tanam AI</div>
    </div>
    <div style="width: 36px; height: 36px; background: #f0fdf4; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #166534; border: 1px solid #bbf7d0;">
      PT
    </div>
  </div>

  <div class="content-scroll">
    <div class="weather-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <div style="font-size: 0.75rem; font-weight: 600; opacity: 0.9;">Kemranjen, Banyumas</div>
          <div class="weather-temp">28°C</div>
        </div>
        <div style="font-size: 1.8rem;">⛅</div>
      </div>
      <div style="font-size: 0.75rem; opacity: 0.9;">Kelembaban: 88% &bull; Curah Hujan Tinggi</div>
      <div class="weather-alert">⚠️ Peringatan Dini: Risiko Hawar Daun Tinggi</div>
    </div>

    <div class="scan-cta-card">
      <div style="font-size: 1.8rem;">📸</div>
      <div style="font-weight: 800; font-size: 0.92rem; color: #0f172a; margin-top: 4px;">Pindai Daun Padi dengan Kamera AI</div>
      <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px;">Deteksi otomatis Hawar Daun, Blas, dan Tungro</div>
      <button class="scan-btn">Buka Kamera Pemindai</button>
    </div>

    <div style="font-weight: 800; font-size: 0.85rem; color: #0f172a;">Petak Lahan Aktif</div>
    
    <div class="plot-item">
      <div>
        <div style="font-weight: 800; font-size: 0.82rem; color: #0f172a;">Petak Sawah A (Ciherang)</div>
        <div style="font-size: 0.72rem; color: #64748b;">Luas: 1.2 Hektar &bull; Umur: 45 HST</div>
      </div>
      <span style="background: #f0fdf4; color: #166534; font-size: 0.7rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;">✓ Sehat</span>
    </div>

    <div class="plot-item">
      <div>
        <div style="font-weight: 800; font-size: 0.82rem; color: #0f172a;">Petak Sawah B (Inpari 32)</div>
        <div style="font-size: 0.72rem; color: #64748b;">Luas: 0.8 Hektar &bull; Umur: 38 HST</div>
      </div>
      <span style="background: #fef2f2; color: #b91c1c; font-size: 0.7rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;">Perlu Tindakan</span>
    </div>
  </div>

  <div class="bottom-nav">
    <div class="nav-active">Beranda</div>
    <div>Pindai AI</div>
    <div>Lahan Saya</div>
    <div>Akun</div>
  </div>
</body>
</html>
"""

render(panen_home_html, 'panen_home.html', f'{SC_DIR}/panen_tanam_mobile.png', '412,860')


# -----------------------------------------------------------------------------
# 6. Panen Tanam: Treatment Plan (412x860)
# -----------------------------------------------------------------------------
panen_treatment_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam — Treatment Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #0f172a;
    display: flex; flex-direction: column; overflow: hidden;
  }}
  .app-bar {{
    padding: 38px 20px 16px; background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; gap: 12px;
  }}
  .content {{ padding: 20px; display: flex; flex-direction: column; gap: 16px; flex: 1; }}
  .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; }}
</style>
</head>
<body>
  <div class="app-bar">
    <div style="font-weight: 800; font-size: 1.1rem; color: #0f172a;">Kalkulator Dosis & Perawatan</div>
  </div>
  <div class="content">
    <div class="card" style="border-left: 4px solid #166534;">
      <div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase;">Diagnosis Terkonfirmasi</div>
      <div style="font-weight: 800; font-size: 1.05rem; color: #166534; margin-top: 2px;">Hawar Daun Bakteri (BLB)</div>
      <div style="font-size: 0.78rem; color: #475569; margin-top: 6px;">Target Luas: 1.0 Hektar (Kemranjen)</div>
    </div>

    <div class="card">
      <div style="font-weight: 800; font-size: 0.85rem; color: #0f172a; margin-bottom: 12px;">Rekomendasi Dosis Bahan Aktif</div>
      
      <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.78rem;">
        <span style="color: #64748b;">Bakterisida:</span>
        <span style="font-weight: 700; color: #0f172a;">Tembaga Oksiklorida 77%</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.78rem;">
        <span style="color: #64748b;">Konsentrasi:</span>
        <span style="font-weight: 700; color: #0f172a;">2.0 - 2.5 gram / Liter</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.78rem;">
        <span style="color: #64748b;">Volume Semprot:</span>
        <span style="font-weight: 700; color: #0f172a;">400 - 500 Liter / Hektar</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.78rem;">
        <span style="color: #64748b;">Kebutuhan Tangki (16L):</span>
        <span style="font-weight: 800; color: #166534;">~28 Tangki Semprot</span>
      </div>
    </div>

    <div class="card" style="background: #f0fdf4; border-color: #bbf7d0;">
      <div style="font-weight: 800; font-size: 0.82rem; color: #166534;">Jadwal Penyemprotan Preventif</div>
      <div style="font-size: 0.72rem; color: #166534; margin-top: 4px; line-height: 1.4;">
        Aplikasi di pagi hari sebelum pukul 09.00 saat embun mengering untuk mencegah penyebaran bakteri ke bulir padi.
      </div>
    </div>
  </div>
</body>
</html>
"""

render(panen_treatment_html, 'panen_treatment.html', f'{SC_DIR}/panen_tanam_treatment.png', '412,860')

print("All SIG Desa & Panen Tanam screenshots rendered!")
