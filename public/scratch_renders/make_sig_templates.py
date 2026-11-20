import base64, json, os, socket, subprocess, time

# 1. HTML for SIG Desa Map (Public Thematic GIS)
html_sig_map = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa Sukamaju - Peta Tematik & Batas Wilayah</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f1f5f9;
    color: #1e293b;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  /* Topbar Tenant Navigation */
  .sig-header {
    height: 60px;
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 30;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .logo-emblem {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }
  .tenant-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .tenant-badge {
    font-size: 0.7rem;
    font-weight: 600;
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
    padding: 2px 8px;
    border-radius: 9999px;
  }
  .tenant-sub {
    font-size: 0.75rem;
    color: #64748b;
  }
  .top-tools {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .basemap-switch {
    display: flex;
    background: #f1f5f9;
    padding: 3px;
    border-radius: 8px;
    gap: 2px;
    border: 1px solid #e2e8f0;
  }
  .basemap-opt {
    padding: 5px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    color: #64748b;
  }
  .basemap-opt.active {
    background: #ffffff;
    color: #0f172a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .btn-admin-login {
    background: #0f172a;
    color: white;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 7px 16px;
    border-radius: 8px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  /* Main Workspace */
  .gis-container {
    flex: 1;
    display: flex;
    position: relative;
    overflow: hidden;
  }

  /* Left Panel GIS */
  .gis-panel {
    width: 380px;
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    z-index: 20;
    box-shadow: 2px 0 12px rgba(0,0,0,0.03);
  }
  .panel-header {
    padding: 18px 20px 14px;
    border-bottom: 1px solid #f1f5f9;
  }
  .panel-header h2 {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
  }
  .panel-header p {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 2px;
  }
  .search-box {
    margin-top: 12px;
    position: relative;
  }
  .search-input {
    width: 100%;
    padding: 8px 12px 8px 34px;
    font-size: 0.8rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    outline: none;
    background: #f8fafc;
  }
  .search-icon {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 0.85rem;
  }
  .panel-content {
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .section-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 8px;
  }
  .category-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .chip {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 9999px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #475569;
    cursor: pointer;
  }
  .chip.active {
    background: #059669;
    color: white;
    border-color: #059669;
  }
  .thematic-select-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
  }
  .thematic-select-box select {
    width: 100%;
    padding: 7px 10px;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background: white;
    color: #0f172a;
    outline: none;
    margin-top: 6px;
  }
  .stat-mini-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  .stat-card-mini {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px;
  }
  .stat-card-mini .val {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0f172a;
  }
  .stat-card-mini .lbl {
    font-size: 0.68rem;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }

  /* Active Feature Detail Card */
  .active-feature-card {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 14px;
  }
  .feature-tag {
    font-size: 0.65rem;
    font-weight: 700;
    color: #059669;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .feature-name {
    font-size: 0.95rem;
    font-weight: 800;
    color: #064e3b;
    margin: 2px 0 6px;
  }
  .feature-attrs {
    font-size: 0.75rem;
    color: #047857;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .feature-attrs span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
  }

  /* Map Canvas */
  .map-canvas-wrapper {
    flex: 1;
    position: relative;
    background: #e2e8f0;
    overflow: hidden;
  }
  .leaflet-map-mock {
    width: 100%;
    height: 100%;
    position: relative;
    background: #d4e0ce; /* Cartographic terrain tone */
  }

  /* Map Controls */
  .map-nav-controls {
    position: absolute;
    top: 20px;
    left: 20px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .nav-btn {
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
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
  }
  .map-legend-hud {
    position: absolute;
    bottom: 24px;
    right: 24px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 14px 18px;
    z-index: 10;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    min-width: 240px;
  }
  .legend-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 8px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.75rem;
    color: #1e293b;
    margin-bottom: 6px;
  }
  .legend-color {
    width: 16px;
    height: 12px;
    border-radius: 3px;
    border: 1.5px solid;
  }
  .coord-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 24px;
    background: rgba(15, 23, 42, 0.85);
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    z-index: 10;
  }

  /* SVG Map Layer Elements */
  svg.map-svg-layer {
    width: 100%;
    height: 100%;
    position: absolute;
    inset: 0;
  }
  .polygon-dusun-1 {
    fill: rgba(16, 185, 129, 0.28);
    stroke: #059669;
    stroke-width: 2.5;
    stroke-linejoin: round;
    cursor: pointer;
  }
  .polygon-dusun-2 {
    fill: rgba(59, 130, 246, 0.25);
    stroke: #2563eb;
    stroke-width: 2.5;
    stroke-linejoin: round;
    cursor: pointer;
  }
  .polygon-dusun-3 {
    fill: rgba(245, 158, 11, 0.25);
    stroke: #d97706;
    stroke-width: 2.5;
    stroke-linejoin: round;
    cursor: pointer;
  }
  .river-line {
    fill: none;
    stroke: #38bdf8;
    stroke-width: 4;
    stroke-linecap: round;
  }
  .road-main {
    fill: none;
    stroke: #ffffff;
    stroke-width: 5;
    stroke-linecap: round;
    filter: drop-shadow(0 0 1px rgba(0,0,0,0.4));
  }
  .road-sub {
    fill: none;
    stroke: #fed7aa;
    stroke-width: 3;
    stroke-linecap: round;
  }
  .pin-marker {
    cursor: pointer;
    transition: transform 0.2s ease;
  }
  .pin-marker:hover {
    transform: scale(1.15);
  }
  .pin-pulse {
    animation: pulse-ring 2s infinite;
  }
  @keyframes pulse-ring {
    0% { r: 6px; opacity: 1; }
    100% { r: 18px; opacity: 0; }
  }
  .hud-badge-floating {
    position: absolute;
    top: 20px;
    right: 20px;
    background: #0f172a;
    color: white;
    padding: 8px 14px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 10;
  }
  .hud-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
  }
</style>
</head>
<body>

  <!-- Header -->
  <header class="sig-header">
    <div class="brand-group">
      <div class="logo-emblem">🗺️</div>
      <div>
        <div class="tenant-title">
          <span>Pemerintah Desa Sukamaju</span>
          <span class="tenant-badge">Tenant Aktif</span>
        </div>
        <div class="tenant-sub">Kecamatan Banyumas • Kabupaten Banyumas • Jawa Tengah</div>
      </div>
    </div>
    <div class="top-tools">
      <div class="basemap-switch">
        <div class="basemap-opt active">Peta Topografi</div>
        <div class="basemap-opt">Citra Satelit</div>
        <div class="basemap-opt">OpenStreetMap</div>
      </div>
      <a href="#" class="btn-admin-login">
        <span>🔒 Panel Admin Desa</span>
      </a>
    </div>
  </header>

  <!-- Workspace -->
  <div class="gis-container">

    <!-- Left Panel GIS -->
    <aside class="gis-panel">
      <div class="panel-header">
        <h2>Navigasi Geografis & Spasial</h2>
        <p>Eksplorasi batas wilayah, sarana desa, dan unit RT/RW</p>
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" class="search-input" value="Batas Dusun I Krajan" placeholder="Cari RT, RW, atau objek...">
        </div>
      </div>

      <div class="panel-content">
        <div>
          <div class="section-label">Filter Kategori Objek</div>
          <div class="category-chips">
            <div class="chip active">Semua (24)</div>
            <div class="chip">Pendidikan (4)</div>
            <div class="chip">Kesehatan (3)</div>
            <div class="chip">Ibadah (8)</div>
            <div class="chip">Pertanian (9)</div>
          </div>
        </div>

        <div class="thematic-select-box">
          <div class="section-label">Layer Tematik Aktif</div>
          <select>
            <option>Batas Wilayah Administratif (Dusun & RT)</option>
            <option>Peta Zonasi Pertanian & Irigasi</option>
            <option>Sebaran Fasilitas Pelayanan Publik</option>
          </select>
        </div>

        <!-- Active Feature Details Card -->
        <div class="active-feature-card">
          <div class="feature-tag">Objek Spasial Terpilih</div>
          <div class="feature-name">Dusun I Krajan (Batas Administrasi)</div>
          <div class="feature-attrs">
            <div>• Kode Unit: <span>ADM-DS-3302-01</span></div>
            <div>• Luas Wilayah: <strong>412.3 Hektar</strong></div>
            <div>• Populasi: <strong>2,140 Jiwa (684 KK)</strong></div>
            <div>• Struktur: 6 RW, 18 RT</div>
            <div>• Validasi PostGIS: <span>ST_IsValid() = TRUE</span></div>
          </div>
        </div>

        <div>
          <div class="section-label">Ringkasan Wilayah Sukamaju</div>
          <div class="stat-mini-grid">
            <div class="stat-card-mini">
              <div class="val">4,856</div>
              <div class="lbl">Total Penduduk (Jiwa)</div>
            </div>
            <div class="stat-card-mini">
              <div class="val">1,420</div>
              <div class="lbl">Kepala Keluarga (KK)</div>
            </div>
            <div class="stat-card-mini">
              <div class="val">842.5 Ha</div>
              <div class="lbl">Luas Terpetakan</div>
            </div>
            <div class="stat-card-mini">
              <div class="val">48 RT</div>
              <div class="lbl">Unit RT Terverifikasi</div>
            </div>
          </div>
        </div>

      </div>
    </aside>

    <!-- Map Canvas Area -->
    <main class="map-canvas-wrapper">

      <div class="map-nav-controls">
        <div class="nav-btn" title="Zoom In">+</div>
        <div class="nav-btn" title="Zoom Out">−</div>
        <div class="nav-btn" title="Reset Pandangan" style="font-size: 0.85rem;">⌂</div>
        <div class="nav-btn" title="Layer Switcher" style="font-size: 0.85rem;">◫</div>
      </div>

      <div class="hud-badge-floating">
        <span class="hud-dot"></span>
        <span>Host: sukamaju.sigdesa.id (Multi-Tenant Engine)</span>
      </div>

      <!-- Map SVG Cartography -->
      <svg class="map-svg-layer" viewBox="0 0 1060 840">
        <!-- Background Terrain & Fields -->
        <rect width="1060" height="840" fill="#d9e5d4"/>
        
        <!-- Farmland patterns -->
        <path d="M 0 0 L 400 0 L 350 220 L 0 180 Z" fill="#cbe0c1" opacity="0.6"/>
        <path d="M 700 0 L 1060 0 L 1060 300 L 750 260 Z" fill="#d0e5c6" opacity="0.6"/>
        <path d="M 0 600 L 320 540 L 280 840 L 0 840 Z" fill="#cbe0c1" opacity="0.6"/>
        <path d="M 800 500 L 1060 550 L 1060 840 L 760 840 Z" fill="#d0e5c6" opacity="0.6"/>

        <!-- River System (Sungai Serayu Branch) -->
        <path class="river-line" d="M 50 840 C 200 680, 240 500, 380 430 C 520 360, 680 400, 780 280 C 860 180, 920 80, 1060 20" />
        
        <!-- Main Roads Network -->
        <path class="road-main" d="M 0 380 Q 300 390 530 420 T 1060 400" />
        <path class="road-main" d="M 520 0 Q 530 380 540 840" />
        
        <!-- Sub Roads -->
        <path class="road-sub" d="M 120 180 Q 280 260 400 240 T 700 200" />
        <path class="road-sub" d="M 280 520 Q 420 620 600 590 T 900 660" />
        <path class="road-sub" d="M 720 220 Q 820 400 780 620" />

        <!-- Polygons: Boundaries of Village Dusun -->
        <!-- Dusun I Krajan (Selected & Highlighted) -->
        <g>
          <polygon class="polygon-dusun-1" points="160,190 480,180 530,390 440,540 220,510 140,360" />
          <!-- Centroid Label -->
          <rect x="235" y="325" width="180" height="42" rx="8" fill="#ffffff" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.15))"/>
          <text x="325" y="344" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="12" fill="#065f46">DUSUN I KRAJAN</text>
          <text x="325" y="359" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#047857">412.3 Ha • 2,140 Jiwa</text>
        </g>

        <!-- Dusun II Waringin -->
        <g>
          <polygon class="polygon-dusun-2" points="530,170 880,150 940,360 760,490 540,410" />
          <rect x="660" y="270" width="190" height="42" rx="8" fill="#ffffff" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.15))"/>
          <text x="755" y="289" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="12" fill="#1e40af">DUSUN II WARINGIN</text>
          <text x="755" y="304" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#2563eb">265.4 Ha • 1,620 Jiwa</text>
        </g>

        <!-- Dusun III Karanganyar -->
        <g>
          <polygon class="polygon-dusun-3" points="420,550 750,510 820,720 580,780 340,710" />
          <rect x="520" y="620" width="190" height="42" rx="8" fill="#ffffff" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.15))"/>
          <text x="615" y="639" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="12" fill="#92400e">DUSUN III KARANGANYAR</text>
          <text x="615" y="654" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#d97706">164.8 Ha • 1,096 Jiwa</text>
        </g>

        <!-- Point Markers with Icons -->
        <!-- Balai Desa Sukamaju (Main Gov Center) -->
        <g class="pin-marker" transform="translate(490, 395)">
          <circle cx="0" cy="0" r="14" fill="#ef4444" filter="drop-shadow(0 3px 6px rgba(239,68,68,0.4))"/>
          <text x="0" y="4" text-anchor="middle" font-size="12" fill="white">🏛️</text>
          <rect x="-70" y="-36" width="140" height="24" rx="6" fill="#1e293b" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.2))"/>
          <text x="0" y="-20" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="10" fill="white">Kantor Balai Desa</text>
        </g>

        <!-- Puskesmas Pembantu -->
        <g class="pin-marker" transform="translate(320, 440)">
          <circle cx="0" cy="0" r="12" fill="#0284c7" filter="drop-shadow(0 3px 6px rgba(2,132,199,0.4))"/>
          <text x="0" y="4" text-anchor="middle" font-size="11" fill="white">🏥</text>
          <rect x="-65" y="-32" width="130" height="22" rx="5" fill="#0f172a"/>
          <text x="0" y="-17" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="9" fill="white">Puskesmas Pembantu</text>
        </g>

        <!-- SD Negeri 1 Sukamaju -->
        <g class="pin-marker" transform="translate(380, 240)">
          <circle cx="0" cy="0" r="12" fill="#10b981" filter="drop-shadow(0 3px 6px rgba(16,185,129,0.4))"/>
          <text x="0" y="4" text-anchor="middle" font-size="11" fill="white">🏫</text>
          <rect x="-60" y="-32" width="120" height="22" rx="5" fill="#0f172a"/>
          <text x="0" y="-17" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="9" fill="white">SDN 1 Sukamaju</text>
        </g>

        <!-- Lumbung Pangan / Pertanian -->
        <g class="pin-marker" transform="translate(710, 360)">
          <circle cx="0" cy="0" r="12" fill="#d97706" filter="drop-shadow(0 3px 6px rgba(217,119,6,0.4))"/>
          <text x="0" y="4" text-anchor="middle" font-size="11" fill="white">🌾</text>
          <rect x="-65" y="-32" width="130" height="22" rx="5" fill="#0f172a"/>
          <text x="0" y="-17" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="9" fill="white">Lumbung Pangan Desa</text>
        </g>

      </svg>

      <!-- Map Legend Floating HUD -->
      <div class="map-legend-hud">
        <div class="legend-title">Legenda Peta Spasial</div>
        <div class="legend-item">
          <div class="legend-color" style="background: rgba(16,185,129,0.3); border-color: #059669;"></div>
          <span>Batas Dusun I Krajan</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: rgba(59,130,246,0.3); border-color: #2563eb;"></div>
          <span>Batas Dusun II Waringin</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: rgba(245,158,11,0.3); border-color: #d97706;"></div>
          <span>Batas Dusun III Karanganyar</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: #38bdf8; border-color: #0284c7; height: 3px;"></div>
          <span>Saluran Irigasi / Sungai</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: #ffffff; border-color: #64748b; height: 4px;"></div>
          <span>Jalan Utama Desa</span>
        </div>
      </div>

      <!-- Coordinate bar -->
      <div class="coord-bar">
        <span>Sistem Koordinat: WGS84 / EPSG:4326 • Proyeksi Web Mercator EPSG:3857</span>
        <span>Lat: -7.429144, Long: 109.241582 • Zoom Level: 14 • Skala 1:12.500</span>
      </div>

    </main>

  </div>

</body>
</html>
"""

# 2. HTML for SIG Desa Spatial Polygon Editor (Admin PostGIS Editor)
html_sig_editor = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>SIG Desa - Spatial Boundary & GeoJSON Polygon Editor</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a;
    color: #f8fafc;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .editor-nav {
    height: 56px;
    background: #1e293b;
    border-bottom: 1px solid #334155;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 30;
  }
  .nav-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .nav-tag {
    background: #0284c7;
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.05em;
  }
  .nav-title {
    font-size: 0.95rem;
    font-weight: 700;
  }
  .nav-sub {
    font-size: 0.75rem;
    color: #94a3b8;
  }
  .nav-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .btn-save {
    background: #10b981;
    color: #064e3b;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 7px 16px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .btn-cancel {
    background: #334155;
    color: #cbd5e1;
    font-size: 0.8rem;
    padding: 7px 14px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
  }

  .editor-workspace {
    flex: 1;
    display: flex;
    position: relative;
    overflow: hidden;
  }
  .editor-viewport {
    flex: 1;
    position: relative;
    background: #090d16;
  }

  /* Floating GIS Toolbar */
  .floating-gis-bar {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 41, 59, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 20;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  }
  .tool-item {
    padding: 7px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 6px;
    color: #94a3b8;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
  }
  .tool-item.active {
    background: #38bdf8;
    color: #0c4a6e;
    font-weight: 700;
  }
  .tool-sep {
    width: 1px;
    height: 20px;
    background: #475569;
  }

  /* Right Attribute Inspector */
  .inspector-panel {
    width: 360px;
    background: #1e293b;
    border-left: 1px solid #334155;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 20;
  }
  .panel-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #f1f5f9;
    border-bottom: 1px solid #334155;
    padding-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .attr-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .attr-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .attr-input {
    background: #0f172a;
    border: 1px solid #334155;
    color: #f8fafc;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.82rem;
    outline: none;
  }
  .topology-hud {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 8px;
    padding: 12px;
  }
  .hud-head {
    font-size: 0.72rem;
    font-weight: 700;
    color: #34d399;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
  }
  .hud-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #a7f3d0;
    line-height: 1.5;
  }
  .geojson-preview-box {
    background: #090d16;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #38bdf8;
    height: 160px;
    overflow-y: auto;
  }

  /* SVG Editor Stage */
  svg.editor-svg {
    width: 100%;
    height: 100%;
    position: absolute;
    inset: 0;
  }
  .grid-pattern {
    stroke: rgba(255, 255, 255, 0.04);
    stroke-width: 1;
  }
  .vertex-node {
    fill: #38bdf8;
    stroke: #ffffff;
    stroke-width: 2.5;
    cursor: grab;
    filter: drop-shadow(0 0 6px #38bdf8);
  }
  .vertex-active {
    fill: #ef4444;
    stroke: #ffffff;
    stroke-width: 3;
    r: 7;
    filter: drop-shadow(0 0 10px #ef4444);
  }
  .guide-line {
    stroke: #38bdf8;
    stroke-width: 2;
    stroke-dasharray: 4, 4;
  }
</style>
</head>
<body>

  <header class="editor-nav">
    <div class="nav-left">
      <span class="nav-tag">ADMIN GIS</span>
      <div>
        <div class="nav-title">PostGIS Polygon Boundary Editor • RT 03 / RW 01</div>
        <div class="nav-sub">Desa Sukamaju • Layer: Batas Rukun Tetangga (Spatial PostGIS)</div>
      </div>
    </div>
    <div class="nav-actions">
      <button class="btn-cancel">Batalkan</button>
      <button class="btn-save">
        <span>💾 Simpan ke PostGIS</span>
      </button>
    </div>
  </header>

  <div class="editor-workspace">

    <div class="editor-viewport">

      <!-- Floating GIS Bar -->
      <div class="floating-gis-bar">
        <div class="tool-item">📍 Tambah Titik</div>
        <div class="tool-item active">⬡ Gambar Poligon</div>
        <div class="tool-item">✂️ Pisah Wilayah</div>
        <div class="tool-sep"></div>
        <div class="tool-item">📐 Hitung Luas (Ha)</div>
        <div class="tool-item">🧲 Snapping Node (Aktif)</div>
      </div>

      <!-- SVG Map Editor Canvas -->
      <svg class="editor-svg" viewBox="0 0 1080 840">
        <!-- Satellite / Topo Dark Grid -->
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" class="grid-pattern" />
          </pattern>
        </defs>
        <rect width="1080" height="840" fill="#0b1329" />
        <rect width="1080" height="840" fill="url(#grid)" />

        <!-- Existing Surrounding Neighbor Polygons (Ghosted) -->
        <polygon points="120,200 440,160 480,420 180,480" fill="rgba(148, 163, 184, 0.08)" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,3" />
        <text x="280" y="310" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" fill="#64748b" font-weight="600">RT 02 / RW 01 (Tetangga)</text>

        <polygon points="480,420 840,360 880,620 540,680" fill="rgba(148, 163, 184, 0.08)" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,3" />
        <text x="680" y="520" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" fill="#64748b" font-weight="600">RT 04 / RW 01 (Tetangga)</text>

        <!-- Active Edited Polygon (RT 03 / RW 01) -->
        <polygon points="440,160 820,130 840,360 480,420" fill="rgba(14, 165, 233, 0.25)" stroke="#38bdf8" stroke-width="3" />

        <!-- Distance Annotations on Edges -->
        <rect x="590" y="125" width="80" height="20" rx="4" fill="#1e293b" />
        <text x="630" y="139" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#38bdf8">382.4 m</text>

        <rect x="430" y="280" width="75" height="20" rx="4" fill="#1e293b" />
        <text x="467" y="294" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#38bdf8">268.1 m</text>

        <!-- Vertex Nodes (Interactive Handles) -->
        <circle cx="440" cy="160" r="6" class="vertex-node" />
        <circle cx="820" cy="130" r="6" class="vertex-node" />
        <circle cx="840" cy="360" r="6" class="vertex-node" />
        <!-- Selected Active Node -->
        <circle cx="480" cy="420" class="vertex-active" />

        <!-- Coordinate Tag for Active Node -->
        <rect x="495" y="405" width="165" height="28" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1" />
        <text x="505" y="423" font-family="'JetBrains Mono', monospace" font-size="10" fill="#f8fafc">Lat: -7.42851, Lon: 109.24102</text>
      </svg>

    </div>

    <!-- Right Inspector Sidebar -->
    <aside class="inspector-panel">
      <div class="panel-title">
        <span>Inspektor Fitur Spasial</span>
        <span style="font-size: 0.7rem; color: #38bdf8;">GeoJSON v2.1</span>
      </div>

      <div class="attr-group">
        <label class="attr-label">Nama Poligon Wilayah</label>
        <input type="text" class="attr-input" value="Rukun Tetangga 03 (RT 03 / RW 01)">
      </div>

      <div class="attr-group">
        <label class="attr-label">Unit Statistik Induk</label>
        <input type="text" class="attr-input" value="RW 01 • Dusun Krajan" readonly>
      </div>

      <div class="attr-group">
        <label class="attr-label">Luas Kalkulasi PostGIS (ST_Area)</label>
        <input type="text" class="attr-input" value="42.8 Hektar (428,210 m²)" readonly>
      </div>

      <div class="attr-group">
        <label class="attr-label">Jumlah Titik Vertex</label>
        <input type="text" class="attr-input" value="4 Titik (Polygon Tertutup Sempurna)" readonly>
      </div>

      <!-- Topology Health HUD -->
      <div class="topology-hud">
        <div class="hud-head">
          <span>✓</span>
          <span>Validasi Topologi Lolos</span>
        </div>
        <div class="hud-body">
          • ST_IsValid(geom) = TRUE<br>
          • 0 Self-Intersection detected<br>
          • 0 Sliver/Overlap dengan RT 02 & RT 04
        </div>
      </div>

      <div class="attr-group">
        <label class="attr-label">Pratinjau GeoJSON Tergenerasi</label>
        <div class="geojson-preview-box">
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[
      [109.2384, -7.4271],
      [109.2421, -7.4268],
      [109.2424, -7.4289],
      [109.2388, -7.4294],
      [109.2384, -7.4271]
    ]]
  },
  "properties": {
    "rt": "03",
    "rw": "01",
    "dusun": "Krajan",
    "area_ha": 42.82
  }
}
        </div>
      </div>
    </aside>

  </div>

</body>
</html>
"""

# 3. HTML for SIG Desa Public Portal & Demographics Dashboard
html_sig_portal = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Portal Transparansi & Statistik Penduduk Desa Sukamaju</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc;
    color: #1e293b;
    padding: 32px;
  }
  .portal-wrap {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  .hero-banner {
    background: linear-gradient(135deg, #064e3b 0%, #047857 60%, #059669 100%);
    border-radius: 20px;
    padding: 32px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 30px -5px rgba(5, 150, 105, 0.3);
  }
  .hero-badge {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 9999px;
    display: inline-block;
    margin-bottom: 8px;
  }
  .hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
  }
  .hero-sub {
    font-size: 0.95rem;
    opacity: 0.9;
    max-width: 620px;
    margin-top: 6px;
    line-height: 1.5;
  }

  /* Metric Cards */
  .metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
  }
  .metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }
  .metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.04em;
  }
  .metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    margin: 6px 0 2px;
  }
  .metric-footer {
    font-size: 0.78rem;
    color: #059669;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  /* Charts & Info Grid */
  .content-grid {
    display: grid;
    grid-template-columns: 2fr 1.2fr;
    gap: 20px;
  }
  .panel-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
  }
  .panel-h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .bar-chart-row {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .bar-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .bar-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 600;
    color: #334155;
  }
  .bar-track {
    height: 10px;
    background: #f1f5f9;
    border-radius: 9999px;
    overflow: hidden;
  }
  .bar-fill {
    height: 100%;
    border-radius: 9999px;
  }

  .service-search-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin-top: 14px;
  }
  .service-input {
    width: 100%;
    padding: 10px 14px;
    font-size: 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    outline: none;
    margin-top: 8px;
  }
  .service-btn {
    width: 100%;
    background: #059669;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 10px;
    border-radius: 8px;
    border: none;
    margin-top: 10px;
    cursor: pointer;
  }
</style>
</head>
<body>

  <div class="portal-wrap">

    <div class="hero-banner">
      <div>
        <div class="hero-badge">PORTAL PELAYANAN & STATISTIK RESMI</div>
        <div class="hero-title">Sistem Informasi Profil Desa Sukamaju</div>
        <div class="hero-sub">Pusat data terpadu kependudukan, pemetaan spasial desa, transparansi bantuan sosial, dan layanan administrasi mandiri warga.</div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 0.8rem; opacity: 0.85;">Status Sistem Multi-Tenant</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #a7f3d0; margin-top: 2px;">● Online & Terverifikasi</div>
      </div>
    </div>

    <!-- Metrics -->
    <div class="metrics-row">
      <div class="metric-card">
        <div class="metric-label">Total Penduduk</div>
        <div class="metric-value">4,856</div>
        <div class="metric-footer">✓ 2,416 Pria • 2,440 Wanita</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Kepala Keluarga (KK)</div>
        <div class="metric-value">1,420</div>
        <div class="metric-footer">✓ 100% NIK Tervalidasi Dukcapil</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Luas Wilayah Spasial</div>
        <div class="metric-value">842.5 Ha</div>
        <div class="metric-footer">✓ Terbagi dalam 3 Dusun & 16 RW</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Penerima Bantuan (Bansos)</div>
        <div class="metric-value">342 KK</div>
        <div class="metric-footer" style="color: #0284c7;">✓ Tervalidasi Desil 1 & 2</div>
      </div>
    </div>

    <!-- Content Row -->
    <div class="content-grid">
      <div class="panel-box">
        <div class="panel-h3">
          <span>Struktur Demografi Berdasarkan Wilayah Dusun</span>
          <span style="font-size: 0.75rem; color: #64748b; font-weight: 500;">Diperbarui per Maret 2026</span>
        </div>
        <div class="bar-chart-row">
          <div class="bar-item">
            <div class="bar-header">
              <span>Dusun I Krajan (6 RW • 18 RT)</span>
              <span>2,140 Jiwa (44.1%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width: 44.1%; background: #059669;"></div></div>
          </div>
          <div class="bar-item">
            <div class="bar-header">
              <span>Dusun II Waringin (5 RW • 16 RT)</span>
              <span>1,620 Jiwa (33.4%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width: 33.4%; background: #2563eb;"></div></div>
          </div>
          <div class="bar-item">
            <div class="bar-header">
              <span>Dusun III Karanganyar (5 RW • 14 RT)</span>
              <span>1,096 Jiwa (22.5%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width: 22.5%; background: #d97706;"></div></div>
          </div>
        </div>
      </div>

      <div class="panel-box">
        <div class="panel-h3">
          <span>Layanan Mandiri Warga Desa</span>
        </div>
        <p style="font-size: 0.8rem; color: #64748b; line-height: 1.5;">Masukkan NIK untuk mengecek status administrasi kependudukan dan bantuan sosial.</p>
        <div class="service-search-box">
          <div style="font-size: 0.72rem; font-weight: 700; color: #475569;">NOMOR INDUK KEPENDUDUKAN (16 DIGIT)</div>
          <input type="text" class="service-input" value="3302141508920003" placeholder="3302xxxxxxxxxxxx">
          <button class="service-btn">Cek Data Kependudukan & Bansos</button>
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""

os.makedirs('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders', exist_ok=True)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/sig_desa_map.html', 'w') as f:
    f.write(html_sig_map)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/sig_desa_editor.html', 'w') as f:
    f.write(html_sig_editor)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/sig_desa_portal.html', 'w') as f:
    f.write(html_sig_portal)

print("Created SIG Desa render templates successfully!")
