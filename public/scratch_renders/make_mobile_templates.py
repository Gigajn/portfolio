import os

# 1. Panen Tanam: Android Home Dashboard (412 x 892 px)
html_panen_home = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam - Android Home</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 412px;
    height: 892px;
    background: #0d1a12;
    color: #f1f7f3;
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  /* Android Status Bar */
  .android-status-bar {
    height: 38px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 600;
    color: #e2f0e6;
    background: transparent;
    z-index: 20;
  }
  .status-icons {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
  }

  /* App Bar */
  .app-bar {
    padding: 10px 20px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .app-brand {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .app-logo {
    font-size: 1.4rem;
  }
  .app-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
  }
  .loc-pill {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #4ade80;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
  }

  /* Scrollable Body */
  .app-body {
    flex: 1;
    overflow-y: auto;
    padding: 10px 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* Weather & Risk Card */
  .risk-card {
    background: linear-gradient(135deg, #132b1e 0%, #0e2117 100%);
    border: 1px solid rgba(74, 222, 128, 0.25);
    border-radius: 20px;
    padding: 18px;
    position: relative;
  }
  .risk-tag {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #fbbf24;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .risk-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    margin: 4px 0 8px;
  }
  .weather-row {
    display: flex;
    gap: 12px;
    margin-top: 10px;
  }
  .weather-chip {
    background: rgba(255, 255, 255, 0.06);
    padding: 6px 10px;
    border-radius: 10px;
    font-size: 0.72rem;
    color: #cbd5e1;
  }
  .weather-chip strong {
    color: #4ade80;
  }

  /* Scanner CTA Hero */
  .scanner-cta-box {
    background: linear-gradient(145deg, #16a34a 0%, #15803d 100%);
    border-radius: 22px;
    padding: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 12px 30px -5px rgba(22, 163, 74, 0.4);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
  .camera-btn-circle {
    width: 64px;
    height: 64px;
    background: #ffffff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    color: #15803d;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
  }
  .scanner-title {
    font-size: 1.05rem;
    font-weight: 800;
    margin-top: 2px;
  }
  .scanner-sub {
    font-size: 0.75rem;
    opacity: 0.9;
    max-width: 280px;
    line-height: 1.4;
  }

  /* 4-Step Preventive Protocol */
  .protocol-panel {
    background: #112217;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 16px;
  }
  .protocol-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 12px;
  }
  .protocol-steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
  .step-box {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 8px 6px;
    text-align: center;
  }
  .step-box.active {
    background: rgba(34, 197, 94, 0.15);
    border-color: #22c55e;
  }
  .step-num {
    font-size: 0.65rem;
    font-weight: 800;
    color: #4ade80;
  }
  .step-text {
    font-size: 0.65rem;
    font-weight: 600;
    margin-top: 2px;
  }

  /* Recent Detection Alert */
  .alert-card {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 14px;
    padding: 14px;
    display: flex;
    gap: 12px;
    align-items: center;
  }
  .alert-icon {
    font-size: 1.4rem;
  }
  .alert-content h4 {
    font-size: 0.82rem;
    font-weight: 700;
    color: #fca5a5;
  }
  .alert-content p {
    font-size: 0.7rem;
    color: #fecaca;
    margin-top: 2px;
    line-height: 1.4;
  }

  /* Bottom Navigation Bar */
  .android-bottom-nav {
    height: 64px;
    background: #09130d;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0 12px;
    z-index: 20;
  }
  .nav-tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 0.65rem;
    color: #94a3b8;
    cursor: pointer;
  }
  .nav-tab-item.active {
    color: #4ade80;
    font-weight: 700;
  }
  .nav-tab-icon {
    font-size: 1.2rem;
  }

  /* Android Gesture Indicator */
  .android-gesture-pill {
    width: 108px;
    height: 4px;
    background: #ffffff;
    opacity: 0.5;
    border-radius: 9999px;
    position: absolute;
    bottom: 8px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
  }
</style>
</head>
<body>

  <!-- Status Bar -->
  <div class="android-status-bar">
    <span>10:45</span>
    <div class="status-icons">
      <span>5G</span>
      <span>📶</span>
      <span>🔋 98%</span>
    </div>
  </div>

  <!-- App Bar -->
  <div class="app-bar">
    <div class="app-brand">
      <span class="app-logo">🌾</span>
      <span class="app-name">Panen Tanam</span>
    </div>
    <div class="loc-pill">Kemranjen MT-I</div>
  </div>

  <!-- Content -->
  <div class="app-body">

    <!-- Risk Prediction Banner -->
    <div class="risk-card">
      <div class="risk-tag">
        <span>⚡</span>
        <span>Prediksi Risiko Penyakit (H-7)</span>
      </div>
      <div class="risk-title">Risiko Tinggi: Hawar Daun Bakteri</div>
      <p style="font-size: 0.75rem; color: #cbd5e1; line-height: 1.5;">Kelembaban tinggi (>88% RH) memicu perkembangbiakan Xanthomonas oryzae di persawahan Banyumas.</p>
      <div class="weather-row">
        <div class="weather-chip">Suhu: <strong>29°C</strong></div>
        <div class="weather-chip">Kelembaban: <strong>91% RH</strong></div>
        <div class="weather-chip">Fase: <strong>Vegetatif</strong></div>
      </div>
    </div>

    <!-- Scanner Action CTA -->
    <div class="scanner-cta-box">
      <div class="camera-btn-circle">📸</div>
      <div class="scanner-title">Pindai Daun Padi (Kamera AI)</div>
      <div class="scanner-sub">Arahkan kamera ke helai daun yang bergejala untuk inferensi model server secara instan.</div>
    </div>

    <!-- 4 Step Preventive Protocol -->
    <div class="protocol-panel">
      <div class="protocol-label">Pendekatan 4 Tahap Terpadu</div>
      <div class="protocol-steps">
        <div class="step-box active">
          <div class="step-num">01</div>
          <div class="step-text">Monitor</div>
        </div>
        <div class="step-box active">
          <div class="step-num">02</div>
          <div class="step-text">Predict</div>
        </div>
        <div class="step-box">
          <div class="step-num">03</div>
          <div class="step-text">Prevent</div>
        </div>
        <div class="step-box">
          <div class="step-num">04</div>
          <div class="step-text">Treat</div>
        </div>
      </div>
    </div>

    <!-- Recent Diagnostic Alert -->
    <div class="alert-card">
      <div class="alert-icon">⚠️</div>
      <div class="alert-content">
        <h4>Peringatan Blok Sawah B-14</h4>
        <p>Terdeteksi gejala awal Hawar Daun Bakteri pada petak 0.75 Ha. Segera turunkan debit air irigasi.</p>
      </div>
    </div>

  </div>

  <!-- Bottom Nav Bar -->
  <div class="android-bottom-nav">
    <div class="nav-tab-item active">
      <div class="nav-tab-icon">🏠</div>
      <span>Beranda</span>
    </div>
    <div class="nav-tab-item">
      <div class="nav-tab-icon">📷</div>
      <span>Pindai AI</span>
    </div>
    <div class="nav-tab-item">
      <div class="nav-tab-icon">📋</div>
      <span>Riwayat</span>
    </div>
    <div class="nav-tab-item">
      <div class="nav-tab-icon">👤</div>
      <span>Akun</span>
    </div>
  </div>

  <div class="android-gesture-pill"></div>

</body>
</html>
"""

# 2. Panen Tanam: AI Camera Leaf Scanner Viewfinder (412 x 892 px)
html_panen_scan = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Panen Tanam - AI Scanner Viewfinder</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 412px;
    height: 892px;
    background: #000000;
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .android-status-bar {
    height: 38px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 600;
    color: #ffffff;
    z-index: 20;
    background: rgba(0,0,0,0.4);
  }
  .scanner-header {
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 20;
    background: rgba(0,0,0,0.4);
  }
  .btn-back {
    font-size: 1.2rem;
    color: white;
    background: rgba(255,255,255,0.15);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .server-inference-badge {
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid #22c55e;
    color: #4ade80;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
  }

  /* Viewfinder Area */
  .viewfinder-area {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  /* SVG Leaf & Detection Box */
  svg.leaf-viewfinder {
    width: 100%;
    height: 100%;
    position: absolute;
    inset: 0;
  }
  .bbox-rect {
    fill: rgba(239, 68, 68, 0.15);
    stroke: #ef4444;
    stroke-width: 2.5;
    stroke-dasharray: 6,4;
    animation: dash 3s linear infinite;
  }
  @keyframes dash {
    to { stroke-dashoffset: -40; }
  }

  /* Floating Detection Tag HUD */
  .detection-hud-pill {
    position: absolute;
    top: 140px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(8px);
    border: 1px solid #ef4444;
    border-radius: 9999px;
    padding: 6px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
    z-index: 15;
  }
  .hud-badge-confidence {
    background: #ef4444;
    color: white;
    font-size: 0.72rem;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 9999px;
  }

  /* Bottom Diagnostic Drawer */
  .diagnosis-drawer {
    background: #111d15;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 28px 28px 0 0;
    padding: 22px 20px 28px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    z-index: 20;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
  }
  .drawer-handle {
    width: 36px;
    height: 4px;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 9999px;
    align-self: center;
  }
  .diag-title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  .diag-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
  }
  .diag-latin {
    font-size: 0.75rem;
    color: #94a3b8;
    font-style: italic;
  }
  .diag-advice {
    font-size: 0.78rem;
    color: #d1fae5;
    line-height: 1.5;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.25);
    padding: 12px;
    border-radius: 12px;
  }
  .btn-protocol {
    background: #22c55e;
    color: #052e16;
    font-weight: 800;
    font-size: 0.88rem;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(34, 197, 94, 0.35);
  }

  .android-gesture-pill {
    width: 108px;
    height: 4px;
    background: #ffffff;
    opacity: 0.5;
    border-radius: 9999px;
    position: absolute;
    bottom: 8px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
  }
</style>
</head>
<body>

  <div class="android-status-bar">
    <span>10:46</span>
    <div style="display:flex; gap:6px;">
      <span>5G</span>
      <span>📶</span>
      <span>🔋 97%</span>
    </div>
  </div>

  <div class="scanner-header">
    <div class="btn-back">‹</div>
    <div class="server-inference-badge">● Fast-Inference Server v2.4</div>
  </div>

  <div class="viewfinder-area">

    <!-- Leaf illustration in camera viewfinder -->
    <svg class="leaf-viewfinder" viewBox="0 0 412 500">
      <!-- Dark camera background with slight blur -->
      <rect width="412" height="500" fill="#0d1b11"/>
      
      <!-- Paddy Leaf Stem & Body -->
      <path d="M 206 480 Q 190 280 206 60 Q 220 280 206 480" fill="#2d6a4f" stroke="#52b788" stroke-width="2"/>
      <path d="M 206 480 L 206 60" stroke="#74c69d" stroke-width="1.5" stroke-dasharray="2,2"/>
      
      <!-- Lesion Spot on Leaf (Hawar Daun Bakteri) -->
      <path d="M 198 160 Q 185 210 202 260 Q 215 210 198 160" fill="#b9770e" opacity="0.85"/>
      <path d="M 192 180 Q 180 220 196 250" fill="#78350f" opacity="0.9"/>

      <!-- AI Detection Bounding Box -->
      <rect x="156" y="140" width="100" height="140" rx="8" class="bbox-rect"/>
      <circle cx="156" cy="140" r="4" fill="#ef4444"/>
      <circle cx="256" cy="140" r="4" fill="#ef4444"/>
      <circle cx="156" cy="280" r="4" fill="#ef4444"/>
      <circle cx="256" cy="280" r="4" fill="#ef4444"/>
    </svg>

    <div class="detection-hud-pill">
      <span style="font-size:0.75rem; font-weight:700;">Hawar Daun Bakteri (BLB)</span>
      <span class="hud-badge-confidence">97.4%</span>
    </div>

  </div>

  <!-- Bottom Drawer -->
  <div class="diagnosis-drawer">
    <div class="drawer-handle"></div>
    <div class="diag-title-row">
      <div>
        <div class="diag-name">Hawar Daun Bakteri (BLB)</div>
        <div class="diag-latin">Patogen: Xanthomonas oryzae pv. oryzae</div>
      </div>
      <div style="font-size:0.72rem; font-weight:700; color:#ef4444; background:rgba(239,68,68,0.15); padding:4px 8px; border-radius:6px;">RISIKO TINGGI</div>
    </div>
    
    <div class="diag-advice">
      <strong>Protokol Preventif Segera:</strong><br>
      Keringkan lahan selama 3 hari berturut-turut (intermittent irrigation) dan hentikan pemupukan unsur nitrogen (Urea) berlebih.
    </div>

    <button class="btn-protocol">Buka Dosis Pengobatan Agen Hayati →</button>
  </div>

  <div class="android-gesture-pill"></div>

</body>
</html>
"""

# 3. Dairy Apps: Android Timeline & Mood Sparkline (412 x 892 px)
html_dairy_timeline = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Dairy Apps - Android Timeline</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 412px;
    height: 892px;
    background: #faf7f2;
    color: #292524;
    font-family: 'Plus Jakarta Sans', sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .android-status-bar {
    height: 38px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 600;
    color: #44403c;
    z-index: 20;
  }
  .app-header {
    padding: 12px 20px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .greeting-tag {
    font-size: 0.72rem;
    font-weight: 600;
    color: #a8a29e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .greeting-h1 {
    font-size: 1.35rem;
    font-weight: 800;
    color: #1c1917;
    margin-top: 2px;
  }
  .avatar-circle {
    width: 40px;
    height: 40px;
    background: #e7e5e4;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    border: 2px solid #d6d3d1;
  }

  .timeline-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 10px 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* Weekly Mood Sparkline Card */
  .mood-card {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.03);
  }
  .mood-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #78716c;
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
  }
  .mood-days-row {
    display: flex;
    justify-content: space-between;
    margin-top: 14px;
  }
  .day-pill {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }
  .day-emoji {
    font-size: 1.3rem;
  }
  .day-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #a8a29e;
  }
  .day-pill.active .day-label {
    color: #bc7962;
    font-weight: 800;
  }

  /* AI Companion Insight Bubble */
  .companion-card {
    background: linear-gradient(135deg, #f5ebe6 0%, #ede0d8 100%);
    border: 1px solid #e2cec4;
    border-radius: 18px;
    padding: 16px;
    display: flex;
    gap: 12px;
  }
  .companion-avatar {
    font-size: 1.5rem;
  }
  .companion-body h4 {
    font-size: 0.82rem;
    font-weight: 700;
    color: #7c2d12;
  }
  .companion-body p {
    font-size: 0.75rem;
    color: #573224;
    margin-top: 4px;
    line-height: 1.5;
  }

  /* Journal Entries Feed */
  .journal-entry-card {
    background: #ffffff;
    border: 1px solid #e7e5e4;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  }
  .entry-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  .entry-time {
    font-size: 0.7rem;
    font-weight: 600;
    color: #a8a29e;
  }
  .entry-mood-badge {
    background: #fbf7f4;
    border: 1px solid #ebd9d1;
    color: #bc7962;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 9999px;
  }
  .entry-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #1c1917;
  }
  .entry-body {
    font-size: 0.78rem;
    color: #57534e;
    line-height: 1.6;
    margin-top: 6px;
  }

  /* Audio Waveform Bar in Entry */
  .audio-waveform-box {
    background: #f5f5f4;
    border-radius: 10px;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
  }
  .play-btn {
    width: 26px;
    height: 26px;
    background: #bc7962;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.65rem;
  }
  .wave-bars {
    display: flex;
    align-items: center;
    gap: 3px;
    flex: 1;
  }
  .w-bar {
    width: 3px;
    background: #a8a29e;
    border-radius: 9999px;
  }

  /* Bottom Nav */
  .android-bottom-nav {
    height: 64px;
    background: #ffffff;
    border-top: 1px solid #e7e5e4;
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0 12px;
    z-index: 20;
  }
  .nav-tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-size: 0.65rem;
    color: #a8a29e;
  }
  .nav-tab-item.active {
    color: #bc7962;
    font-weight: 700;
  }

  .android-gesture-pill {
    width: 108px;
    height: 4px;
    background: #1c1917;
    opacity: 0.3;
    border-radius: 9999px;
    position: absolute;
    bottom: 8px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
  }
</style>
</head>
<body>

  <div class="android-status-bar">
    <span>21:15</span>
    <div style="display:flex; gap:6px;">
      <span>WiFi</span>
      <span>🔋 88%</span>
    </div>
  </div>

  <div class="app-header">
    <div>
      <div class="greeting-tag">Personal Memoir</div>
      <div class="greeting-h1">Jurnal & Refleksi Diri</div>
    </div>
    <div class="avatar-circle">🌿</div>
  </div>

  <div class="timeline-scroll">

    <!-- Weekly Mood Sparkline -->
    <div class="mood-card">
      <div class="mood-title">
        <span>Keseimbangan Emosional Pekan Ini</span>
        <span style="color:#bc7962;">Dominan: Reflektif</span>
      </div>
      <div class="mood-days-row">
        <div class="day-pill">
          <div class="day-emoji">😊</div>
          <div class="day-label">Sen</div>
        </div>
        <div class="day-pill">
          <div class="day-emoji">😌</div>
          <div class="day-label">Sel</div>
        </div>
        <div class="day-pill">
          <div class="day-emoji">🚀</div>
          <div class="day-label">Rab</div>
        </div>
        <div class="day-pill">
          <div class="day-emoji">🥰</div>
          <div class="day-label">Kam</div>
        </div>
        <div class="day-pill active">
          <div class="day-emoji">✨</div>
          <div class="day-label">Jum</div>
        </div>
      </div>
    </div>

    <!-- AI Companion Insight -->
    <div class="companion-card">
      <div class="companion-avatar">🦊</div>
      <div class="companion-body">
        <h4>Catatan Empati AI Companion</h4>
        <p>"Minggu ini kamu menyelesaikan banyak tugas rekayasa sistem yang kompleks. Jangan lupa beri apresiasi pada diri sendiri malam ini."</p>
      </div>
    </div>

    <!-- Journal Entry -->
    <div class="journal-entry-card">
      <div class="entry-header">
        <span class="entry-time">Hari ini • 21:05 WIB</span>
        <span class="entry-mood-badge">🌿 Penuh Syukur</span>
      </div>
      <div class="entry-title">Refleksi Redesain Portofolio & Arsitektur Rust</div>
      <div class="entry-body">
        Menyelesaikan transformasi seluruh sistem portofolio dengan performa tinggi. Hasilnya terasa sangat bersih dan menyenangkan untuk ditinjau kembali.
      </div>
      <div class="audio-waveform-box">
        <div class="play-btn">▶</div>
        <div class="wave-bars">
          <div class="w-bar" style="height:12px;"></div>
          <div class="w-bar" style="height:20px; background:#bc7962;"></div>
          <div class="w-bar" style="height:16px; background:#bc7962;"></div>
          <div class="w-bar" style="height:24px; background:#bc7962;"></div>
          <div class="w-bar" style="height:8px;"></div>
          <div class="w-bar" style="height:18px;"></div>
          <div class="w-bar" style="height:14px;"></div>
          <div class="w-bar" style="height:6px;"></div>
        </div>
        <span style="font-size:0.68rem; font-family:'JetBrains Mono',monospace; color:#78716c;">0:42</span>
      </div>
    </div>

  </div>

  <div class="android-bottom-nav">
    <div class="nav-tab-item active">
      <span style="font-size:1.2rem;">📖</span>
      <span>Jurnal</span>
    </div>
    <div class="nav-tab-item">
      <span style="font-size:1.2rem;">🎙️</span>
      <span>Suara</span>
    </div>
    <div class="nav-tab-item">
      <span style="font-size:1.2rem;">📊</span>
      <span>Statistik</span>
    </div>
    <div class="nav-tab-item">
      <span style="font-size:1.2rem;">⚙️</span>
      <span>Setelan</span>
    </div>
  </div>

  <div class="android-gesture-pill"></div>

</body>
</html>
"""

# 4. Jackup: Rust CLI & Systems Terminal Execution (1100 x 700 px)
html_jackup_cli = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Jackup: Cloud Repatriation Engine - Rust CLI</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1100px;
    height: 700px;
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .term-header {
    height: 42px;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
  }
  .window-dots {
    display: flex;
    gap: 8px;
  }
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .term-title {
    font-size: 0.8rem;
    color: #8b949e;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
  }
  .term-body {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    font-size: 0.82rem;
    line-height: 1.7;
  }
  .prompt { color: #58a6ff; }
  .cmd { color: #f0f6fc; font-weight: 700; }
  .badge-dev {
    display: inline-block;
    background: rgba(210, 153, 34, 0.15);
    border: 1px solid #d29922;
    color: #e3b341;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    margin-bottom: 14px;
  }
  .success { color: #3fb950; font-weight: 600; }
  .warn { color: #d29922; }
  .cyan { color: #38bdf8; }
  .dim { color: #8b949e; }
</style>
</head>
<body>

  <div class="term-header">
    <div class="window-dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="term-title">kudo@fedora: ~/Projects/Portofolio/Jackup — bash</div>
    <div style="font-size:0.75rem; color:#8b949e;">rustc 1.86.0 (Rust Edition 2024)</div>
  </div>

  <div class="term-body">
    <div class="badge-dev">⚙ STATUS PROYEK: SEDANG DALAM FASE PENGEMBANGAN AKTIF (CORE SYSTEMS & CLI)</div>
    
    <div><span class="prompt">kudo@fedora:~/Jackup$</span> <span class="cmd">cargo run --bin jackup -- status</span></div>
    <div class="dim">   Compiling jackup-core v0.1.0 (/home/kudo/Projects/Portofolio/Jackup/crates/jackup-core)</div>
    <div class="dim">   Compiling jackup-crypto v0.1.0 (/home/kudo/Projects/Portofolio/Jackup/crates/jackup-crypto)</div>
    <div class="dim">   Compiling jackup-orchestrator v0.1.0 (/home/kudo/Projects/Portofolio/Jackup/crates/jackup-orchestrator)</div>
    <div class="dim">   Compiling jackup v0.1.0 (/home/kudo/Projects/Portofolio/Jackup/crates/jackup-cli)</div>
    <div class="dim">    Finished dev [unoptimized + debuginfo] target(s) in 0.62s</div>
    <div class="dim">     Running `target/debug/jackup status`</div>
    <br>
    <div><span class="cyan">🦀 Jackup: Cloud Repatriation & Autonomous Server Migration Engine</span></div>
    <div><span class="dim">Workspace Multi-Crate Status Report:</span></div>
    <div>--------------------------------------------------------------------------------</div>
    <div>  • <span class="cyan">jackup-core</span>          : <span class="success">[OK]</span> Versioned Protocol v1.4, Zero-Alloc Frame Serializer</div>
    <div>  • <span class="cyan">jackup-crypto</span>        : <span class="success">[OK]</span> Argon2id KDF + ChaCha20-Poly1305 AEAD Secure Vault</div>
    <div>  • <span class="cyan">jackup-orchestrator</span>  : <span class="success">[OK]</span> Linux Namespaces, Cgroups v2 & Systemd Task Driver</div>
    <div>  • <span class="cyan">jackup-cli</span>           : <span class="success">[OK]</span> Headless Daemon Client & Terminal Command Router</div>
    <div>--------------------------------------------------------------------------------</div>
    <br>
    <div><span class="prompt">kudo@fedora:~/Jackup$</span> <span class="cmd">jackup plan --source aws-ap-southeast-1 --target on-premise-node-01 --dry-run</span></div>
    <div><span class="warn">[*] Running dry-run preflight checks for zero-downtime container migration...</span></div>
    <div>[+] Resolving source state: 8 storage volumes, 14 service containers (Total 48.2 GB)</div>
    <div>[+] Generating delta transfer sync plan via encrypted peer channel...</div>
    <div>[+] Cryptographic signature: <span class="cyan">ed25519:9f8a...4b12 (VERIFIED)</span></div>
    <div><span class="success">[✓] Preflight complete: 0 warnings, 0 conflicts. Estimated switchover downtime: 0.00 ms.</span></div>
    <div><span class="dim">Catatan: UI Grafis tidak diperlukan karena sistem bekerja penuh pada layer orkestrator sistem operasi Linux.</span></div>
    <br>
    <div><span class="prompt">kudo@fedora:~/Jackup$</span> <span style="animation: blink 1s infinite;">█</span></div>
  </div>

</body>
</html>
"""

with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/panen_home.html', 'w') as f:
    f.write(html_panen_home)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/panen_scan.html', 'w') as f:
    f.write(html_panen_scan)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/dairy_timeline.html', 'w') as f:
    f.write(html_dairy_timeline)
with open('/home/kudo/Projects/Portofolio/portfolio_rust/public/scratch_renders/jackup_cli.html', 'w') as f:
    f.write(html_jackup_cli)

print("Created Mobile & Systems render templates successfully!")
