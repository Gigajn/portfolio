import os
import subprocess
import time

RENDER_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders'
SCREENSHOT_DIR = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots'
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs('/tmp/ff_profile', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. SIG DESA — Interactive GIS Thematic Map (Clean, Realistic Cartography)
# -----------------------------------------------------------------------------
html_sig_desa = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa Karangrau — Peta Tematik & Data Spasial</title>
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
  .brand-area { display: flex; align-items: center; gap: 12px; }
  .emblem {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }
  .brand-titles h1 {
    font-size: 1.05rem; font-weight: 800; color: #0f172a;
    display: flex; align-items: center; gap: 8px;
  }
  .tenant-pill {
    background: #ecfdf5; color: #059669;
    border: 1px solid #a7f3d0; font-size: 0.7rem; font-weight: 700;
    padding: 2px 8px; border-radius: 9999px;
  }
  .brand-sub { font-size: 0.74rem; color: #64748b; }
  .top-actions { display: flex; align-items: center; gap: 12px; }
  .basemap-toggle {
    display: flex; background: #f1f5f9; padding: 4px;
    border-radius: 10px; gap: 3px; border: 1px solid #e2e8f0;
  }
  .opt-btn {
    border: none; background: transparent; font-family: inherit;
    font-size: 0.78rem; font-weight: 600; padding: 6px 12px;
    border-radius: 7px; color: #64748b; cursor: pointer;
  }
  .opt-btn.active {
    background: #ffffff; color: #0f172a;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .btn-primary-action {
    background: #0f172a; color: white; font-size: 0.8rem; font-weight: 700;
    padding: 8px 16px; border-radius: 9px; display: flex; align-items: center;
    gap: 6px; text-decoration: none;
  }
  .workspace { flex: 1; display: flex; position: relative; overflow: hidden; }
  .gis-sidebar {
    width: 360px; background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(16px); border-right: 1px solid #e2e8f0;
    display: flex; flex-direction: column; z-index: 30;
    box-shadow: 4px 0 20px rgba(0,0,0,0.06);
  }
  .sidebar-section { padding: 16px 20px; border-bottom: 1px solid #f1f5f9; }
  .section-title {
    font-size: 0.7rem; font-weight: 800; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px;
  }
  .kpi-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .kpi-box {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 10px 12px;
  }
  .kpi-num { font-size: 1.25rem; font-weight: 800; color: #0f172a; }
  .kpi-label { font-size: 0.7rem; color: #64748b; font-weight: 600; margin-top: 2px; }
  .layer-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 0; border-bottom: 1px dashed #f1f5f9;
  }
  .layer-item:last-child { border-bottom: none; }
  .layer-meta { display: flex; align-items: center; gap: 10px; }
  .color-swatch { width: 14px; height: 14px; border-radius: 4px; }
  .layer-name { font-size: 0.82rem; font-weight: 600; color: #334155; }
  .layer-badge {
    font-size: 0.68rem; font-weight: 700; color: #64748b;
    background: #f1f5f9; padding: 2px 7px; border-radius: 6px;
  }
  .search-wrapper { position: relative; margin-top: 6px; }
  .search-box {
    width: 100%; padding: 9px 12px 9px 34px;
    border: 1px solid #cbd5e1; border-radius: 9px;
    font-size: 0.8rem; outline: none; background: #f8fafc;
  }
  .search-ico {
    position: absolute; left: 10px; top: 50%;
    transform: translateY(-50%); color: #94a3b8; font-size: 0.85rem;
  }
  .map-canvas { flex: 1; position: relative; background: #eef3ec; overflow: hidden; }
  .map-svg-layer { width: 100%; height: 100%; position: absolute; top: 0; left: 0; }
  .map-zoom-controls {
    position: absolute; top: 20px; right: 20px; z-index: 25;
    display: flex; flex-direction: column; gap: 6px;
  }
  .zoom-btn {
    width: 36px; height: 36px; background: white;
    border: 1px solid #cbd5e1; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 700; color: #334155;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08); cursor: pointer;
  }
  .feature-inspector-popup {
    position: absolute; bottom: 24px; left: 384px; z-index: 25;
    background: #ffffff; border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.16);
    border: 1px solid #cbd5e1; max-width: 440px;
    display: flex; flex-direction: column; gap: 8px;
  }
  .inspector-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
  .inspector-tag {
    font-size: 0.65rem; font-weight: 800; text-transform: uppercase;
    color: #059669; letter-spacing: 0.5px;
  }
  .inspector-title { font-size: 1.05rem; font-weight: 800; color: #0f172a; }
  .inspector-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;
    margin-top: 4px; background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 8px 10px;
  }
  .attr-val { font-size: 0.85rem; font-weight: 700; color: #1e293b; font-family: 'JetBrains Mono', monospace; }
  .attr-lbl { font-size: 0.65rem; color: #64748b; font-weight: 600; }
  .coords-chip {
    position: absolute; bottom: 24px; right: 24px; z-index: 25;
    background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(8px);
    color: #e2e8f0; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace;
    padding: 6px 14px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
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
  <div class="workspace">
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
      <svg class="map-svg-layer" viewBox="0 0 1080 796" preserveAspectRatio="none">
        <rect width="100%" height="100%" fill="#edf3ea"/>
        <polygon points="120,60 520,40 560,340 220,380 90,240" fill="#d9e9d3" stroke="#b4cfa9" stroke-width="2"/>
        <polygon points="560,40 980,80 920,420 540,360" fill="#d3e4cc" stroke="#b0cda4" stroke-width="2"/>
        <polygon points="140,420 480,410 460,740 100,710" fill="#deeed8" stroke="#bcd8b0" stroke-width="2"/>
        <polygon points="520,420 960,450 940,760 500,740" fill="#d7e8cf" stroke="#b4cfa9" stroke-width="2"/>
        <polygon points="260,210 640,190 710,510 320,540" fill="rgba(16, 185, 129, 0.22)" stroke="#059669" stroke-width="3" stroke-dasharray="6,4"/>
        <path d="M 0,260 Q 220,320 420,290 T 780,380 T 1080,350" fill="none" stroke="#60a5fa" stroke-width="12" stroke-linecap="round"/>
        <path d="M 420,290 Q 510,480 620,796" fill="none" stroke="#93c5fd" stroke-width="6" stroke-linecap="round"/>
        <path d="M 60,796 L 280,440 L 480,240 L 820,120 L 1080,80" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round"/>
        <path d="M 60,796 L 280,440 L 480,240 L 820,120 L 1080,80" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
        <path d="M 280,440 L 740,480 L 980,360" fill="none" stroke="#ffffff" stroke-width="6"/>
        <path d="M 280,440 L 740,480 L 980,360" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>
        <path d="M 480,240 L 520,680" fill="none" stroke="#ffffff" stroke-width="5"/>
        <path d="M 480,240 L 520,680" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="320" y="320" transform="rotate(-34, 320, 320)" fill="#475569" font-size="11" font-weight="700">Jl. Raya Karangrau</text>
        <text x="560" y="470" fill="#64748b" font-size="10" font-weight="600">Jl. Dusun Krajan</text>
        <text x="760" y="365" transform="rotate(7, 760, 365)" fill="#2563eb" font-size="11" font-weight="700">Sungai Pelus</text>
        <g transform="translate(480, 240)">
          <circle r="16" fill="#ef4444" opacity="0.2"/>
          <circle r="9" fill="#ef4444"/>
          <text x="0" y="4" fill="white" font-size="9" text-anchor="middle" font-weight="800">🏛</text>
          <text x="16" y="4" fill="#0f172a" font-size="11" font-weight="800">Balai Desa Karangrau</text>
        </g>
        <g transform="translate(680, 310)">
          <circle r="12" fill="#10b981" opacity="0.25"/>
          <circle r="7" fill="#10b981"/>
          <text x="12" y="4" fill="#0f172a" font-size="10" font-weight="700">Puskesmas Pembantu</text>
        </g>
        <g transform="translate(340, 480)">
          <circle r="12" fill="#3b82f6" opacity="0.25"/>
          <circle r="7" fill="#3b82f6"/>
          <text x="12" y="4" fill="#0f172a" font-size="10" font-weight="700">SD Negeri Karangrau</text>
        </g>
      </svg>
      <div class="map-zoom-controls">
        <button class="zoom-btn">+</button>
        <button class="zoom-btn">−</button>
        <button class="zoom-btn" title="Pusatkan Peta">⌖</button>
      </div>
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
      <div class="coords-chip">
        EPSG:4326 | Lat: -7.4294, Lng: 109.2435 | Skala: 1:5,000 | Render PostGIS GIST
      </div>
    </div>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 2. PANEN TANAM — Camera AI Scanner & Field Diagnosis (Modern Android M3)
# -----------------------------------------------------------------------------
html_panen_scan = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam — AI Scanner</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 412px;
    height: 860px;
    background: #09140d;
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .status-bar {
    height: 38px; padding: 0 18px;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 0.8rem; font-weight: 600; z-index: 30;
  }
  .camera-viewport {
    flex: 1; position: relative;
    background: radial-gradient(circle at 50% 40%, #1e4529 0%, #0d2215 60%, #050e08 100%);
    overflow: hidden; display: flex; align-items: center; justify-content: center;
  }
  .leaf-art {
    width: 260px; height: 380px; position: relative;
    display: flex; align-items: center; justify-content: center;
  }
  .ai-box {
    position: absolute;
    width: 210px; height: 260px;
    border: 2px solid #22c55e;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(34, 197, 94, 0.45), inset 0 0 15px rgba(34, 197, 94, 0.2);
  }
  .ai-box::before {
    content: ''; position: absolute; top: -6px; left: -6px;
    width: 16px; height: 16px; border-top: 3px solid #4ade80; border-left: 3px solid #4ade80;
  }
  .ai-box::after {
    content: ''; position: absolute; bottom: -6px; right: -6px;
    width: 16px; height: 16px; border-bottom: 3px solid #4ade80; border-right: 3px solid #4ade80;
  }
  .ai-label-pill {
    position: absolute; top: -14px; left: 16px;
    background: #22c55e; color: #052e16;
    font-size: 0.68rem; font-weight: 800; padding: 4px 10px;
    border-radius: 9999px; display: flex; align-items: center; gap: 4px;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
  }
  .scanner-crosshair {
    position: absolute; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #4ade80, transparent);
    top: 50%; animation: scanline 2.5s infinite ease-in-out;
  }
  .camera-top-tools {
    position: absolute; top: 12px; left: 0; right: 0;
    padding: 0 20px; display: flex; justify-content: space-between; align-items: center;
    z-index: 20;
  }
  .cam-tool-btn {
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
  }
  .diagnostic-sheet {
    background: rgba(13, 27, 18, 0.94);
    backdrop-filter: blur(20px);
    border-top: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 28px 28px 0 0;
    padding: 20px 22px 28px;
    display: flex; flex-direction: column; gap: 14px;
    z-index: 30;
  }
  .sheet-pill-handle {
    width: 40px; height: 4px; background: rgba(255, 255, 255, 0.3);
    border-radius: 2px; margin: 0 auto -4px;
  }
  .diag-title-row {
    display: flex; justify-content: space-between; align-items: flex-start;
  }
  .diag-disease-name {
    font-size: 1.15rem; font-weight: 800; color: #ffffff;
  }
  .diag-match-badge {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid #22c55e; color: #4ade80;
    font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 9999px;
  }
  .diag-details {
    font-size: 0.78rem; color: #9ca3af; line-height: 1.45;
  }
  .treatment-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px; padding: 12px 14px;
  }
  .treatment-title {
    font-size: 0.72rem; font-weight: 700; color: #4ade80;
    text-transform: uppercase; margin-bottom: 4px;
  }
  .treatment-text { font-size: 0.78rem; color: #e5e7eb; }
  .btn-save-treatment {
    background: #22c55e; color: #052e16; font-size: 0.85rem; font-weight: 800;
    padding: 12px; border-radius: 9999px; border: none; width: 100%;
    cursor: pointer; text-align: center;
  }
</style>
</head>
<body>
  <div class="status-bar">
    <span>09:41</span>
    <span>● 4G &bull; 92%</span>
  </div>
  <div class="camera-viewport">
    <div class="camera-top-tools">
      <div class="cam-tool-btn">⚡</div>
      <div style="background: rgba(0,0,0,0.5); padding: 4px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">
        Edge AI &bull; PyTorch NPU 42ms
      </div>
      <div class="cam-tool-btn">⚙</div>
    </div>
    <div class="leaf-art">
      <svg width="220" height="320" viewBox="0 0 220 320">
        <path d="M 110,20 C 180,90 200,220 110,300 C 20,220 40,90 110,20 Z" fill="#2d6a3f" stroke="#40916c" stroke-width="3"/>
        <line x1="110" y1="20" x2="110" y2="300" stroke="#52b788" stroke-width="2.5"/>
        <line x1="110" y1="90" x2="160" y2="120" stroke="#52b788" stroke-width="1.5"/>
        <line x1="110" y1="130" x2="60" y2="160" stroke="#52b788" stroke-width="1.5"/>
        <line x1="110" y1="170" x2="165" y2="200" stroke="#52b788" stroke-width="1.5"/>
        <ellipse cx="130" cy="140" rx="22" ry="14" fill="#a3702a" opacity="0.85"/>
        <ellipse cx="90" cy="180" rx="18" ry="12" fill="#8f5b1d" opacity="0.85"/>
      </svg>
      <div class="ai-box">
        <div class="ai-label-pill">✓ Hawar Daun Bakteri (97.4%)</div>
        <div class="scanner-crosshair"></div>
      </div>
    </div>
  </div>
  <div class="diagnostic-sheet">
    <div class="sheet-pill-handle"></div>
    <div class="diag-title-row">
      <div>
        <div class="diag-disease-name">Hawar Daun Bakteri (BLB)</div>
        <div style="font-size: 0.7rem; color: #4ade80;">Xanthomonas oryzae pv. oryzae</div>
      </div>
      <span class="diag-match-badge">Akurasi 97.4%</span>
    </div>
    <p class="diag-details">
      Terdeteksi bercak nekrotik kebasahan di tepian daun padi. Kondisi masih pada fase awal (keparahan 22%).
    </p>
    <div class="treatment-box">
      <div class="treatment-title">Rekomendasi Perawatan Lapang:</div>
      <div class="treatment-text">
        Semprotkan bakterisida hayati (Bacillus subtilis) 2 ml/liter air. Kurangi pupuk urea sementara dan atur sirkulasi air sawah.
      </div>
    </div>
    <button class="btn-save-treatment">Simpan Riwayat Perawatan Lahan</button>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 3. GEODIPA SPK — Enterprise Multi-Criteria Evaluation System
# -----------------------------------------------------------------------------
html_geodipa = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Geodipa SPK — Evaluasi Kinerja Karyawan</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px;
    height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc;
    color: #1e293b;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  header {
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .top-left { display: flex; align-items: center; gap: 12px; }
  .logo-square {
    width: 34px; height: 34px; background: #0284c7; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1rem;
  }
  .app-titles h1 { font-size: 0.95rem; font-weight: 800; color: #0f172a; }
  .app-sub { font-size: 0.72rem; color: #64748b; }
  .main-layout { flex: 1; display: flex; padding: 20px 24px; gap: 20px; overflow: hidden; }
  .content-col { flex: 1; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  .stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .stat-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 12px 16px;
  }
  .stat-val { font-size: 1.3rem; font-weight: 800; color: #0f172a; }
  .stat-lbl { font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 2px; }
  .table-card {
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .table-header-bar {
    padding: 12px 18px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
  }
  .table-title { font-size: 0.85rem; font-weight: 800; color: #0f172a; }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; text-align: left; }
  th {
    background: #f8fafc; padding: 10px 14px; font-weight: 700; color: #475569;
    border-bottom: 1px solid #e2e8f0; font-size: 0.72rem; text-transform: uppercase;
  }
  td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  tr:hover { background: #f8fafc; }
  .rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%;
    font-weight: 800; font-size: 0.72rem;
  }
  .rank-1 { background: #fef3c7; color: #d97706; border: 1px solid #fcd34d; }
  .rank-2 { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
  .rank-3 { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
  .score-mono { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0f172a; }
  .dept-pill {
    background: #f1f5f9; color: #475569; font-size: 0.68rem; font-weight: 600;
    padding: 2px 8px; border-radius: 9999px;
  }
</style>
</head>
<body>
  <header>
    <div class="top-left">
      <div class="logo-square">GD</div>
      <div class="app-titles">
        <h1>Sistem Pendukung Keputusan Karyawan Terbaik (SPK SAW)</h1>
        <div class="app-sub">PT Geo Dipa Energi (Persero) &bull; Periode Semester I</div>
      </div>
    </div>
    <div style="font-size: 0.78rem; font-weight: 700; background: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 8px;">
      Metode: Simple Additive Weighting (SAW)
    </div>
  </header>
  <div class="main-layout">
    <div class="content-col">
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-val">148</div>
          <div class="stat-lbl">Total Pegawai Dinilai</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">5 Kriteria</div>
          <div class="stat-lbl">Bobot SAW Terkalibrasi</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">0.942</div>
          <div class="stat-lbl">Skor Preferensi Tertinggi</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">100%</div>
          <div class="stat-lbl">Kelengkapan Penilaian Peer</div>
        </div>
      </div>

      <div class="table-card">
        <div class="table-header-bar">
          <div class="table-title">Peringkat Hasil Rekomendasi Karyawan Terbaik</div>
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
              <th>Nilai SAW (Vi)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="rank-badge rank-1">1</span></td>
              <td><b>Rizky Pratama, S.T.</b></td>
              <td>198804122019</td>
              <td><span class="dept-pill">Operasi Pembangkit</span></td>
              <td>95</td><td>94</td><td>90</td><td>92</td><td>96</td>
              <td class="score-mono" style="color: #0284c7;">0.942</td>
            </tr>
            <tr>
              <td><span class="rank-badge rank-2">2</span></td>
              <td><b>Anisa Wulandari, S.E.</b></td>
              <td>199208152020</td>
              <td><span class="dept-pill">Keuangan & SDM</span></td>
              <td>92</td><td>95</td><td>88</td><td>94</td><td>90</td>
              <td class="score-mono">0.926</td>
            </tr>
            <tr>
              <td><span class="rank-badge rank-3">3</span></td>
              <td><b>Budi Santoso, A.Md.</b></td>
              <td>198501202018</td>
              <td><span class="dept-pill">Pemeliharaan Turbin</span></td>
              <td>90</td><td>92</td><td>92</td><td>88</td><td>88</td>
              <td class="score-mono">0.908</td>
            </tr>
            <tr>
              <td><span class="rank-badge" style="background:#f8fafc; color:#64748b; border:1px solid #e2e8f0;">4</span></td>
              <td><b>Dwi Handoko, S.T.</b></td>
              <td>199011032019</td>
              <td><span class="dept-pill">Health, Safety & Environment</span></td>
              <td>88</td><td>90</td><td>86</td><td>90</td><td>85</td>
              <td class="score-mono">0.884</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 4. STOCK MANAGEMENT (BGE) — Inventory & Shopify Multi-Store Sync
# -----------------------------------------------------------------------------
html_stock_bge = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Stock Management & Shopify Sync (BGE)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px;
    height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc;
    color: #1e293b;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  header {
    height: 60px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px;
  }
  .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1rem; }
  .badge-sync {
    background: #ecfdf5; border: 1px solid #a7f3d0; color: #059669;
    font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;
  }
  .container { flex: 1; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .kpi { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px; }
  .kpi-val { font-size: 1.3rem; font-weight: 800; color: #0f172a; }
  .kpi-lbl { font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 2px; }
  .table-box {
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .table-nav {
    padding: 12px 18px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; text-align: left; }
  th { background: #f8fafc; padding: 10px 14px; font-weight: 700; color: #475569; font-size: 0.72rem; border-bottom: 1px solid #e2e8f0; }
  td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .sku-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; }
  .sync-status {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 0.7rem; font-weight: 700; color: #059669;
  }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <span>📦</span>
      <span>BGE Supply — Stock & Shopify Inventory Sync</span>
    </div>
    <div class="badge-sync">
      ● Shopify Webhook Terhubung (Sinkronisasi Otomatis 2 Arah)
    </div>
  </header>
  <div class="container">
    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-val">1,248</div>
        <div class="kpi-lbl">Total SKU Produk</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">14 SKU</div>
        <div class="kpi-lbl" style="color: #d97706;">Peringatan Stok Menipis</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">284 pcs</div>
        <div class="kpi-lbl">Barang dalam Pengiriman</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">99.8%</div>
        <div class="kpi-lbl">Akurasi Stok Toko & Online</div>
      </div>
    </div>
    <div class="table-box">
      <div class="table-nav">
        <b>Katalog Stok Produk & Alokasi Multi-Channel</b>
        <span style="font-size: 0.72rem; color: #64748b;">Diperbarui secara real-time via webhook</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Nama Barang & Varian</th>
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
            <td><span class="sku-tag">BGE-TEE-BLK-L</span></td>
            <td><b>Heavyweight Oversized Tee - Black (L)</b></td>
            <td>Apparel</td>
            <td>42 pcs</td><td>18 pcs</td><td>34 pcs</td>
            <td><b>94 pcs</b></td>
            <td><span class="sync-status">✓ Tersinkron</span></td>
          </tr>
          <tr>
            <td><span class="sku-tag">BGE-DNM-IND-32</span></td>
            <td><b>Raw Selvedge Denim 14oz - Indigo (32)</b></td>
            <td>Pants</td>
            <td>16 pcs</td><td>6 pcs</td><td>12 pcs</td>
            <td><b>34 pcs</b></td>
            <td><span class="sync-status">✓ Tersinkron</span></td>
          </tr>
          <tr>
            <td><span class="sku-tag">BGE-HOD-GRY-XL</span></td>
            <td><b>French Terry Pullover Hoodie - Heather Grey (XL)</b></td>
            <td>Outerwear</td>
            <td>5 pcs</td><td>2 pcs</td><td>4 pcs</td>
            <td><b style="color:#d97706;">11 pcs (Stok Menipis)</b></td>
            <td><span class="sync-status">✓ Tersinkron</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""

# Save render templates
renders = {
    'sig_desa.html': (html_sig_desa, f'{SCREENSHOT_DIR}/sig_desa.png', '1440,860'),
    'panen_scan.html': (html_panen_scan, f'{SCREENSHOT_DIR}/panen_tanam_scan.png', '412,860'),
    'geodipa_spk.html': (html_geodipa, f'{SCREENSHOT_DIR}/geodipa_spk.png', '1366,768'),
    'stock_bge.html': (html_stock_bge, f'{SCREENSHOT_DIR}/stock_management_bge.png', '1366,768')
}

for name, (html, out_png, dims) in renders.items():
    html_path = f'{RENDER_DIR}/{name}'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'Rendering {name} -> {out_png} ({dims})...')
    cmd = [
        'firefox', '--headless',
        '-profile', '/tmp/ff_profile',
        '--screenshot', out_png,
        f'--window-size={dims}',
        f'file://{html_path}'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if res.returncode == 0 and os.path.exists(out_png):
        print(f'   ✅ Rendered successfully: {out_png} ({os.path.getsize(out_png)} bytes)')
    else:
        print(f'   ❌ Failed: {res.stderr}')

print('Finished screenshot generation!')
