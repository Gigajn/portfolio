import os
import subprocess
import time

RENDER_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders'
SCREENSHOT_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots'
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. SIG DESA — Interactive GIS Thematic Map (High-Fidelity Leaflet Cartography)
# -----------------------------------------------------------------------------
html_sig_desa = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa Karangrau — Peta Tematik & Data Spasial Desa</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1440px;
    height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a;
    color: #1e293b;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Top Tenant Navigation */
  header {
    height: 64px;
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 40;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  }
  .brand-area {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .emblem {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }
  .brand-titles h1 {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .tenant-pill {
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 9999px;
  }
  .brand-sub {
    font-size: 0.74rem;
    color: #64748b;
  }
  .top-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .basemap-toggle {
    display: flex;
    background: #f1f5f9;
    padding: 4px;
    border-radius: 10px;
    gap: 3px;
    border: 1px solid #e2e8f0;
  }
  .opt-btn {
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 7px;
    color: #64748b;
    cursor: pointer;
  }
  .opt-btn.active {
    background: #ffffff;
    color: #0f172a;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .btn-primary-action {
    background: #0f172a;
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
  }

  /* Main Map Viewport */
  .workspace {
    flex: 1;
    display: flex;
    position: relative;
    overflow: hidden;
  }

  /* Left GIS Control Panel */
  .gis-sidebar {
    width: 360px;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(16px);
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    z-index: 30;
    box-shadow: 4px 0 20px rgba(0,0,0,0.06);
  }
  .sidebar-section {
    padding: 16px 20px;
    border-bottom: 1px solid #f1f5f9;
  }
  .section-title {
    font-size: 0.7rem;
    font-weight: 800;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 10px;
  }
  .kpi-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .kpi-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
  }
  .kpi-num {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0f172a;
  }
  .kpi-label {
    font-size: 0.7rem;
    color: #64748b;
    font-weight: 600;
    margin-top: 2px;
  }
  .layer-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px dashed #f1f5f9;
  }
  .layer-item:last-child { border-bottom: none; }
  .layer-meta {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .color-swatch {
    width: 14px;
    height: 14px;
    border-radius: 4px;
  }
  .layer-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #334155;
  }
  .layer-badge {
    font-size: 0.68rem;
    font-weight: 700;
    color: #64748b;
    background: #f1f5f9;
    padding: 2px 7px;
    border-radius: 6px;
  }
  .search-wrapper {
    position: relative;
    margin-top: 6px;
  }
  .search-box {
    width: 100%;
    padding: 9px 12px 9px 34px;
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    font-size: 0.8rem;
    outline: none;
    background: #f8fafc;
  }
  .search-ico {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 0.85rem;
  }

  /* Cartographic Map Canvas */
  .map-canvas {
    flex: 1;
    position: relative;
    background: #eef3ec; /* Rich cartographic tone */
    overflow: hidden;
  }
  
  /* Satellite / Terrain Cartographic Vector Styling */
  .map-svg-layer {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }

  /* Map Controls */
  .map-zoom-controls {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 25;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .zoom-btn {
    width: 36px;
    height: 36px;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    cursor: pointer;
  }

  /* Thematic Inspection Popup (PostGIS Feature Drawer) */
  .feature-inspector-popup {
    position: absolute;
    bottom: 24px;
    left: 384px;
    z-index: 25;
    background: #ffffff;
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.16);
    border: 1px solid #cbd5e1;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .inspector-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .inspector-tag {
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    color: #059669;
    letter-spacing: 0.5px;
  }
  .inspector-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
  }
  .inspector-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 4px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 10px;
  }
  .attr-val {
    font-size: 0.85rem;
    font-weight: 700;
    color: #1e293b;
    font-family: 'JetBrains Mono', monospace;
  }
  .attr-lbl {
    font-size: 0.65rem;
    color: #64748b;
    font-weight: 600;
  }

  /* Bottom Legend & Coordinates Chip */
  .coords-chip {
    position: absolute;
    bottom: 24px;
    right: 24px;
    z-index: 25;
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(8px);
    color: #e2e8f0;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
</style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header>
    <div class="brand-area">
      <div class="emblem">🗺️</div>
      <div class="brand-titles">
        <h1>
          <span>SIG Desa Karangrau</span>
          <span class="tenant-pill">Kec. Banyumas</span>
        </h1>
        <div class="brand-sub">Platform Informasi Geografis & Batas Administrasi Desa</div>
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

  <!-- Workspace -->
  <div class="workspace">

    <!-- Left GIS Panel -->
    <aside class="gis-sidebar">
      <div class="sidebar-section">
        <div class="section-title">Ringkasan Wilayah</div>
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
        <div class="section-title">Pencarian Objek & Lokasi</div>
        <div class="search-wrapper">
          <span class="search-ico">🔍</span>
          <input type="text" class="search-box" value="Dusun II Karangrau" placeholder="Cari batas RW, dusun, fasilitas...">
        </div>
      </div>

      <div class="sidebar-section" style="flex: 1; overflow-y: auto;">
        <div class="section-title">Lapisan Spasial Aktif (PostGIS Layers)</div>
        
        <div class="layer-item">
          <div class="layer-meta">
            <div class="color-swatch" style="background: #10b981;"></div>
            <span class="layer-name">Batas Wilayah Dusun & RW</span>
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
            <span class="layer-name">Fasilitas Publik & Kantor Desa</span>
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

    <!-- Map Canvas Area -->
    <div class="map-canvas">
      
      <!-- Cartographic Vector Render -->
      <svg class="map-svg-layer" viewBox="0 0 1080 796" preserveAspectRatio="none">
        <defs>
          <!-- Subtle terrain pattern -->
          <pattern id="farmland-pattern" width="20" height="20" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="20" y2="20" stroke="#d5e4cd" stroke-width="1"/>
          </pattern>
        </defs>

        <!-- Background base terrain -->
        <rect width="100%" height="100%" fill="#edf3ea"/>

        <!-- Farmland Parcels (Lahan Pertanian Basah) -->
        <polygon points="120,60 520,40 560,340 220,380 90,240" fill="#d9e9d3" stroke="#b4cfa9" stroke-width="2"/>
        <polygon points="560,40 980,80 920,420 540,360" fill="#d3e4cc" stroke="#b0cda4" stroke-width="2"/>
        <polygon points="140,420 480,410 460,740 100,710" fill="#deeed8" stroke="#bcd8b0" stroke-width="2"/>
        <polygon points="520,420 960,450 940,760 500,740" fill="#d7e8cf" stroke="#b4cfa9" stroke-width="2"/>

        <!-- Active Highlight Polygon: Dusun II Karangrau -->
        <polygon points="260,210 640,190 710,510 320,540" fill="rgba(16, 185, 129, 0.22)" stroke="#059669" stroke-width="3" stroke-dasharray="6,4"/>

        <!-- River Stream (Sungai Pelus & Irigasi) -->
        <path d="M 0,260 Q 220,320 420,290 T 780,380 T 1080,350" fill="none" stroke="#60a5fa" stroke-width="12" stroke-linecap="round"/>
        <path d="M 420,290 Q 510,480 620,796" fill="none" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>

        <!-- Primary Road Arteries (Jalan Raya Desa Karangrau) -->
        <path d="M 60,796 L 280,440 L 480,240 L 820,120 L 1080,80" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round"/>
        <path d="M 60,796 L 280,440 L 480,240 L 820,120 L 1080,80" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
        
        <!-- Secondary Neighborhood Streets -->
        <path d="M 280,440 L 740,480 L 980,360" fill="none" stroke="#ffffff" stroke-width="6"/>
        <path d="M 280,440 L 740,480 L 980,360" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>
        <path d="M 480,240 L 520,680" fill="none" stroke="#ffffff" stroke-width="5"/>
        <path d="M 480,240 L 520,680" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>

        <!-- Road Labels -->
        <text x="320" y="320" transform="rotate(-34, 320, 320)" fill="#475569" font-size="11" font-weight="700">Jl. Raya Karangrau</text>
        <text x="560" y="470" fill="#64748b" font-size="10" font-weight="600">Jl. Dusun Krajan</text>
        <text x="760" y="365" transform="rotate(7, 760, 365)" fill="#2563eb" font-size="11" font-weight="700">Sungai Pelus</text>

        <!-- Point Facilities Markers -->
        <!-- Kantor Desa -->
        <g transform="translate(480, 240)">
          <circle r="16" fill="#ef4444" opacity="0.2"/>
          <circle r="9" fill="#ef4444"/>
          <text x="0" y="4" fill="white" font-size="9" text-anchor="middle" font-weight="800">🏛</text>
          <text x="16" y="4" fill="#0f172a" font-size="11" font-weight="800">Balai Desa Karangrau</text>
        </g>

        <!-- Pustu / Posyandu -->
        <g transform="translate(680, 310)">
          <circle r="12" fill="#10b981" opacity="0.25"/>
          <circle r="7" fill="#10b981"/>
          <text x="12" y="4" fill="#0f172a" font-size="10" font-weight="700">Puskesmas Pembantu</text>
        </g>

        <!-- SD Negeri 1 Karangrau -->
        <g transform="translate(340, 480)">
          <circle r="12" fill="#3b82f6" opacity="0.25"/>
          <circle r="7" fill="#3b82f6"/>
          <text x="12" y="4" fill="#0f172a" font-size="10" font-weight="700">SD Negeri Karangrau</text>
        </g>

        <!-- Masjid Al-Ikhlas -->
        <g transform="translate(560, 560)">
          <circle r="12" fill="#8b5cf6" opacity="0.25"/>
          <circle r="7" fill="#8b5cf6"/>
          <text x="12" y="4" fill="#0f172a" font-size="10" font-weight="700">Masjid Jami</text>
        </g>
      </svg>

      <!-- Zoom Controls -->
      <div class="map-zoom-controls">
        <button class="zoom-btn">+</button>
        <button class="zoom-btn">−</button>
        <button class="zoom-btn" title="Pusatkan Peta">⌖</button>
      </div>

      <!-- Active Feature Inspector Card -->
      <div class="feature-inspector-popup">
        <div class="inspector-header">
          <span class="inspector-tag">PostGIS Poligon Terpilih</span>
          <span style="font-size: 0.75rem; color: #64748b;">ID: GEO-DSN-02</span>
        </div>
        <div class="inspector-title">Dusun II Karangrau (RW 03 & RW 04)</div>
        <p style="font-size: 0.78rem; color: #475569; line-height: 1.4;">
          Kawasan pemukiman dan pertanian produktif. Dilengkapi 1 posyandu, 1 embung irigasi desa, dan sentra UMKM kerajinan.
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

      <!-- Bottom Coordinate Chip -->
      <div class="coords-chip">
        EPSG:4326 | Lat: -7.4294, Lng: 109.2435 | Skala: 1:5,000 | Render PostGIS GIST
      </div>

    </div>

  </div>

</body>
</html>
"""

with open(f'{RENDER_DIR}/sig_desa_preview.html', 'w') as f:
    f.write(html_sig_desa)

print("Saved sig_desa_preview.html")
"""

with open('/tmp/test_sig.py', 'w') as f:
    f.write(html_sig_desa)
