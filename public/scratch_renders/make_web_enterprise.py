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
# 1. Geodipa SPK: Main Dashboard (1366x768)
# -----------------------------------------------------------------------------
geodipa_spk_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Geodipa SPK — Evaluasi Karyawan Terbaik (Metode SAW)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f8fafc; color: #1e293b;
    display: flex; flex-direction: column; overflow: hidden;
  }
  header {
    height: 64px; background: #ffffff; border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .top-brand { display: flex; align-items: center; gap: 12px; }
  .logo-box {
    width: 38px; height: 38px; background: #0284c7; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.1rem;
  }
  .title-area h1 { font-size: 1rem; font-weight: 800; color: #0f172a; }
  .title-area p { font-size: 0.72rem; color: #64748b; font-weight: 500; }
  
  .layout-main { flex: 1; display: flex; padding: 20px 28px; gap: 20px; overflow: hidden; }
  .left-content { flex: 1; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .kpi-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  }
  .kpi-val { font-size: 1.4rem; font-weight: 800; color: #0f172a; }
  .kpi-lbl { font-size: 0.72rem; color: #64748b; font-weight: 600; margin-top: 2px; }

  .table-box {
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .table-head-bar {
    padding: 14px 20px; border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; text-align: left; }
  th {
    background: #f8fafc; padding: 12px 16px; font-weight: 700; color: #475569;
    border-bottom: 1px solid #e2e8f0; font-size: 0.72rem; text-transform: uppercase;
  }
  td { padding: 11px 16px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  
  .rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%; font-weight: 800; font-size: 0.72rem;
  }
  .rank-1 { background: #fef3c7; color: #d97706; border: 1px solid #fcd34d; }
  .rank-2 { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
  .rank-3 { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
  .score-mono { font-family: 'JetBrains Mono', monospace; font-weight: 800; color: #0f172a; }
  
  .right-side { width: 340px; display: flex; flex-direction: column; gap: 16px; }
  .side-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; }
  .crit-bar { margin-top: 10px; display: flex; flex-direction: column; gap: 4px; }
  .crit-lbl-row { display: flex; justify-content: space-between; font-size: 0.72rem; font-weight: 700; color: #475569; }
  .bar-track { height: 6px; background: #f1f5f9; border-radius: 9999px; overflow: hidden; }
  .bar-fill { height: 100%; background: #0284c7; border-radius: 9999px; }
</style>
</head>
<body>
  <header>
    <div class="top-brand">
      <div class="logo-box">GD</div>
      <div class="title-area">
        <h1>SPK Evaluasi Kinerja Karyawan Terbaik (Metode SAW)</h1>
        <p>PT Geo Dipa Energi (Persero) &bull; Unit Dieng & Patuha</p>
      </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
      <span style="font-size: 0.75rem; font-weight: 700; background: #e0f2fe; color: #0369a1; padding: 6px 14px; border-radius: 8px;">
        Periode: Semester I 2024
      </span>
      <span style="font-size: 0.75rem; font-weight: 700; background: #f0fdf4; color: #166534; padding: 6px 14px; border-radius: 8px; border: 1px solid #bbf7d0;">
        ✓ Disetujui Pimpinan
      </span>
    </div>
  </header>

  <div class="layout-main">
    <div class="left-content">
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-val">148 Pegawai</div>
          <div class="kpi-lbl">Total Populasi Ternilai</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">5 Kriteria</div>
          <div class="kpi-lbl">Bobot SAW Terstandarisasi</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">0.948</div>
          <div class="kpi-lbl">Skor Preferensi Tertinggi (V₁)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val">100%</div>
          <div class="kpi-lbl">Rekonsiliasi Peer-Review</div>
        </div>
      </div>

      <div class="table-box">
        <div class="table-head-bar">
          <div style="font-weight: 800; font-size: 0.88rem; color: #0f172a;">Hasil Akhir Perangkingan Preferensi (Vᵢ)</div>
          <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">Metode: Simple Additive Weighting</div>
        </div>
        <table>
          <thead>
            <tr>
              <th style="width: 60px;">Rank</th>
              <th>Nama Pegawai</th>
              <th>Divisi / Departemen</th>
              <th>Disiplin (25%)</th>
              <th>Kinerja (30%)</th>
              <th>Kerjasama (20%)</th>
              <th>Skor Preferensi (V)</th>
              <th>Status Kelulusan</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="rank-badge rank-1">1</span></td>
              <td><strong style="color: #0f172a;">Eko Prasetyo, S.T.</strong><br><span style="font-size: 0.7rem; color: #64748b;">NIP: 19880412-GD</span></td>
              <td><span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.72rem;">Operasi & Pemeliharaan</span></td>
              <td class="score-mono">96.0</td>
              <td class="score-mono">98.0</td>
              <td class="score-mono">92.0</td>
              <td class="score-mono" style="color: #0284c7; font-size: 0.9rem;">0.948</td>
              <td><span style="background: #fef3c7; color: #b45309; font-weight: 700; padding: 3px 10px; border-radius: 9999px; font-size: 0.7rem;">🏆 Terpilih Terbaik I</span></td>
            </tr>
            <tr>
              <td><span class="rank-badge rank-2">2</span></td>
              <td><strong style="color: #0f172a;">Siti Nurhaliza, M.M.</strong><br><span style="font-size: 0.7rem; color: #64748b;">NIP: 19910620-GD</span></td>
              <td><span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.72rem;">Keuangan & SDM</span></td>
              <td class="score-mono">94.0</td>
              <td class="score-mono">95.0</td>
              <td class="score-mono">90.0</td>
              <td class="score-mono" style="color: #0f172a;">0.925</td>
              <td><span style="background: #f0fdf4; color: #166534; font-weight: 700; padding: 3px 10px; border-radius: 9999px; font-size: 0.7rem;">Rekomendasi</span></td>
            </tr>
            <tr>
              <td><span class="rank-badge rank-3">3</span></td>
              <td><strong style="color: #0f172a;">Budi Santoso, A.Md.</strong><br><span style="font-size: 0.7rem; color: #64748b;">NIP: 19850915-GD</span></td>
              <td><span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.72rem;">K3 & Lingkungan</span></td>
              <td class="score-mono">90.0</td>
              <td class="score-mono">92.0</td>
              <td class="score-mono">88.0</td>
              <td class="score-mono" style="color: #0f172a;">0.894</td>
              <td><span style="background: #f0fdf4; color: #166534; font-weight: 700; padding: 3px 10px; border-radius: 9999px; font-size: 0.7rem;">Rekomendasi</span></td>
            </tr>
            <tr>
              <td><span class="rank-badge" style="background: #f8fafc; color: #64748b;">4</span></td>
              <td><strong style="color: #0f172a;">Dewi Lestari, S.Kom.</strong><br><span style="font-size: 0.7rem; color: #64748b;">NIP: 19940228-GD</span></td>
              <td><span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.72rem;">Teknologi Informasi</span></td>
              <td class="score-mono">88.0</td>
              <td class="score-mono">89.0</td>
              <td class="score-mono">85.0</td>
              <td class="score-mono" style="color: #0f172a;">0.871</td>
              <td><span style="background: #f1f5f9; color: #475569; font-weight: 700; padding: 3px 10px; border-radius: 9999px; font-size: 0.7rem;">Memenuhi Syarat</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="right-side">
      <div class="side-card">
        <div style="font-weight: 800; font-size: 0.85rem; color: #0f172a;">Bobot Kriteria SAW (W)</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 2px;">Normalisasi Bobot Total = 1.00</div>

        <div class="crit-bar">
          <div class="crit-lbl-row"><span>C1. Capaian Kinerja</span><span>30%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width: 30%;"></div></div>
        </div>
        <div class="crit-bar">
          <div class="crit-lbl-row"><span>C2. Kedisiplinan & Presensi</span><span>25%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width: 25%;"></div></div>
        </div>
        <div class="crit-bar">
          <div class="crit-lbl-row"><span>C3. Kerjasama Tim</span><span>20%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width: 20%;"></div></div>
        </div>
        <div class="crit-bar">
          <div class="crit-lbl-row"><span>C4. Inisiatif & Problem Solving</span><span>15%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width: 15%;"></div></div>
        </div>
        <div class="crit-bar">
          <div class="crit-lbl-row"><span>C5. Loyalitas & Core Values</span><span>10%</span></div>
          <div class="bar-track"><div class="bar-fill" style="width: 10%;"></div></div>
        </div>
      </div>

      <div class="side-card" style="background: #f0f9ff; border-color: #bae6fd;">
        <div style="font-weight: 800; font-size: 0.82rem; color: #0369a1;">Rumus Preferensi SAW</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #0284c7; margin-top: 6px; font-weight: 700;">
          V_i = ∑ (w_j * r_ij)
        </div>
        <p style="font-size: 0.72rem; color: #0369a1; margin-top: 6px; line-height: 1.4;">
          Menjumlahkan perkalian matriks ternormalisasi (R) dengan bobot kriteria (W) untuk menghasilkan perangkingan deterministik bebas bias.
        </p>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(geodipa_spk_html, 'geodipa_spk.html', f'{SC_DIR}/geodipa_spk.png', '1366,768')


# -----------------------------------------------------------------------------
# 2. Geodipa SPK: Normalized Matrix (1200x714)
# -----------------------------------------------------------------------------
geodipa_matrix_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Matriks Ternormalisasi SAW — Geodipa</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1200px; height: 714px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #ffffff; color: #1e293b;
    padding: 30px; display: flex; flex-direction: column; gap: 18px;
    overflow: hidden;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  th { background: #f8fafc; padding: 12px; border: 1px solid #e2e8f0; font-weight: 700; color: #475569; }
  td { padding: 12px; border: 1px solid #e2e8f0; text-align: center; }
  .mono { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0284c7; }
</style>
</head>
<body>
  <div>
    <h2 style="font-size: 1.2rem; font-weight: 800; color: #0f172a;">Matriks Normalisasi R_ij (Simple Additive Weighting)</h2>
    <p style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">Kalkulasi normalisasi kriteria Benefit: R_ij = X_ij / Max(X_ij)</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Alternatif (Karyawan)</th>
        <th>R1 (Disiplin)</th>
        <th>R2 (Kinerja)</th>
        <th>R3 (Kerjasama)</th>
        <th>R4 (Inisiatif)</th>
        <th>R5 (Loyalitas)</th>
        <th>Nilai Akhir (V_i)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: left; font-weight: 700;">A1 - Eko Prasetyo, S.T.</td>
        <td class="mono">0.979</td>
        <td class="mono">1.000</td>
        <td class="mono">0.968</td>
        <td class="mono">0.923</td>
        <td class="mono">1.000</td>
        <td class="mono" style="color: #166534; font-weight: 800; font-size: 0.95rem;">0.948</td>
      </tr>
      <tr>
        <td style="text-align: left; font-weight: 700;">A2 - Siti Nurhaliza, M.M.</td>
        <td class="mono">0.959</td>
        <td class="mono">0.969</td>
        <td class="mono">0.947</td>
        <td class="mono">0.961</td>
        <td class="mono">0.900</td>
        <td class="mono" style="color: #0f172a; font-weight: 800;">0.925</td>
      </tr>
      <tr>
        <td style="text-align: left; font-weight: 700;">A3 - Budi Santoso, A.Md.</td>
        <td class="mono">0.918</td>
        <td class="mono">0.938</td>
        <td class="mono">0.926</td>
        <td class="mono">0.884</td>
        <td class="mono">0.850</td>
        <td class="mono" style="color: #0f172a; font-weight: 800;">0.894</td>
      </tr>
      <tr>
        <td style="text-align: left; font-weight: 700;">A4 - Dewi Lestari, S.Kom.</td>
        <td class="mono">0.897</td>
        <td class="mono">0.908</td>
        <td class="mono">0.894</td>
        <td class="mono">0.846</td>
        <td class="mono">0.850</td>
        <td class="mono" style="color: #0f172a; font-weight: 800;">0.871</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

render(geodipa_matrix_html, 'geodipa_matrix.html', f'{SC_DIR}/geodipa_matrix_saw.png', '1200,714')


# -----------------------------------------------------------------------------
# 3. Stock Management (BGE): Main Filament 3 Dashboard (1366x768)
# -----------------------------------------------------------------------------
stock_bge_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>BGE Supply — Stock Management System & Shopify Sync</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #e2e8f0;
    display: flex; overflow: hidden;
  }
  .sidebar {
    width: 260px; background: #090d16; border-right: 1px solid #1e293b;
    padding: 24px 18px; display: flex; flex-direction: column; gap: 20px;
  }
  .brand-logo { display: flex; align-items: center; gap: 10px; }
  .logo-square {
    width: 36px; height: 36px; background: #3b82f6; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 1.1rem;
  }
  .nav-group { display: flex; flex-direction: column; gap: 4px; }
  .nav-link {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 600;
    color: #94a3b8;
  }
  .nav-active { background: #1e293b; color: #ffffff; }

  .main-panel { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #0f172a; }
  .top-navbar {
    height: 60px; border-bottom: 1px solid #1e293b;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px; background: #0b1120;
  }
  .sync-status {
    display: flex; align-items: center; gap: 8px;
    background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.4);
    color: #4ade80; padding: 6px 14px; border-radius: 9999px;
    font-size: 0.72rem; font-weight: 700;
  }

  .content-area { flex: 1; padding: 22px 28px; display: flex; flex-direction: column; gap: 18px; overflow: hidden; }
  
  .stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .stat-item {
    background: #1e293b; border: 1px solid #334155; border-radius: 12px;
    padding: 14px 18px;
  }
  .stat-val { font-size: 1.4rem; font-weight: 800; color: #ffffff; }
  .stat-lbl { font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-top: 2px; }

  .filament-table {
    flex: 1; background: #1e293b; border: 1px solid #334155; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .table-titlebar {
    padding: 14px 20px; border-bottom: 1px solid #334155;
    display: flex; justify-content: space-between; align-items: center;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; text-align: left; }
  th {
    background: #0f172a; padding: 12px 16px; font-weight: 700; color: #94a3b8;
    border-bottom: 1px solid #334155; font-size: 0.72rem; text-transform: uppercase;
  }
  td { padding: 12px 16px; border-bottom: 1px solid #334155; color: #e2e8f0; }
  
  .sku-mono { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #38bdf8; font-size: 0.75rem; }
  .badge-synced {
    background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.4);
    color: #4ade80; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;
  }
  .prod-thumb {
    width: 36px; height: 36px; border-radius: 8px; background: #334155;
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
  }
</style>
</head>
<body>
  <div class="sidebar">
    <div class="brand-logo">
      <div class="logo-square">BGE</div>
      <div>
        <div style="font-weight: 800; font-size: 0.95rem; color: white;">BGE Supply Co.</div>
        <div style="font-size: 0.7rem; color: #64748b;">Filament 3 &bull; Shopify Sync</div>
      </div>
    </div>

    <div class="nav-group">
      <div class="nav-link nav-active">📦 Katalog Produk</div>
      <div class="nav-link">🔄 Offline Staging <span style="background: #3b82f6; color: white; padding: 1px 6px; border-radius: 9999px; font-size: 0.65rem;">3</span></div>
      <div class="nav-link">⚡ Shopify Webhook Sync</div>
      <div class="nav-link">💳 Kasir POS Penjualan</div>
      <div class="nav-link">📋 Log Sinkronisasi</div>
    </div>
  </div>

  <div class="main-panel">
    <div class="top-navbar">
      <div style="font-weight: 800; font-size: 1.05rem; color: white;">Manajemen Inventaris Multi-Channel</div>
      <div class="sync-status">
        <span>●</span> Webhook Aktif (bgesupply.myshopify.com)
      </div>
    </div>

    <div class="content-area">
      <div class="stat-grid">
        <div class="stat-item">
          <div class="stat-val">1,420 SKU</div>
          <div class="stat-lbl">Total Katalog Produk</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">8,950 pcs</div>
          <div class="stat-lbl">Kuantitas Stok Gudang</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">99.8%</div>
          <div class="stat-lbl">Shopify Sync Success Rate</div>
        </div>
        <div class="stat-item">
          <div class="stat-val">Rp 16.850.000</div>
          <div class="stat-lbl">Omset Penjualan Hari Ini</div>
        </div>
      </div>

      <div class="filament-table">
        <div class="table-titlebar">
          <div style="font-weight: 800; font-size: 0.88rem; color: white;">Master Data Produk & Status Sinkronisasi Online</div>
          <span style="font-size: 0.72rem; color: #94a3b8;">Menampilkan 4 dari 1,420 Produk</span>
        </div>
        <table>
          <thead>
            <tr>
              <th style="width: 50px;">Item</th>
              <th>Nama Produk</th>
              <th>SKU Barcode</th>
              <th>Varian Ukuran</th>
              <th>Stok Fisik</th>
              <th>Stok Shopify</th>
              <th>Harga Jual</th>
              <th>Status API</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><div class="prod-thumb">👕</div></td>
              <td><strong style="color: white;">BGE Heavyweight Boxy Tee - Vintage Black</strong></td>
              <td class="sku-mono">BGE-TS-001-BLK</td>
              <td><span style="background: #334155; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">S, M, L, XL</span></td>
              <td style="font-weight: 700; color: white;">124 pcs</td>
              <td style="font-weight: 700; color: #4ade80;">124 pcs</td>
              <td style="font-weight: 700;">Rp 185.000</td>
              <td><span class="badge-synced">✓ Terhubung</span></td>
            </tr>
            <tr>
              <td><div class="prod-thumb">👖</div></td>
              <td><strong style="color: white;">BGE Technical Cargo Pants - Forest Olive</strong></td>
              <td class="sku-mono">BGE-CP-004-OLV</td>
              <td><span style="background: #334155; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">28, 30, 32, 34</span></td>
              <td style="font-weight: 700; color: white;">48 pcs</td>
              <td style="font-weight: 700; color: #4ade80;">48 pcs</td>
              <td style="font-weight: 700;">Rp 345.000</td>
              <td><span class="badge-synced">✓ Terhubung</span></td>
            </tr>
            <tr>
              <td><div class="prod-thumb">🧥</div></td>
              <td><strong style="color: white;">BGE Washed Full-Zip Hoodie - Charcoal Grey</strong></td>
              <td class="sku-mono">BGE-HD-002-CHR</td>
              <td><span style="background: #334155; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">M, L, XL</span></td>
              <td style="font-weight: 700; color: white;">62 pcs</td>
              <td style="font-weight: 700; color: #4ade80;">62 pcs</td>
              <td style="font-weight: 700;">Rp 420.000</td>
              <td><span class="badge-synced">✓ Terhubung</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(stock_bge_html, 'stock_bge.html', f'{SC_DIR}/stock_management_bge.png', '1366,768')


# -----------------------------------------------------------------------------
# 4. Stock Management: Sync Logs (1200x714)
# -----------------------------------------------------------------------------
stock_logs_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Shopify Webhook Audit Logs — BGE Supply</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1200px; height: 714px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #e2e8f0;
    padding: 24px; display: flex; flex-direction: column; gap: 16px;
    overflow: hidden;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
  th { background: #1e293b; padding: 12px; border: 1px solid #334155; text-align: left; color: #94a3b8; }
  td { padding: 10px 12px; border: 1px solid #334155; }
  .mono { font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; }
</style>
</head>
<body>
  <div>
    <h2 style="font-size: 1.15rem; font-weight: 800; color: white;">Log Audit Sinkronisasi Shopify Webhook & REST API</h2>
    <p style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Pemantauan rekonsiliasi data inventaris real-time antara kasir fisik dan toko daring</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>Waktu (UTC+7)</th>
        <th>Event Topic</th>
        <th>SKU Target</th>
        <th>Delta Stok</th>
        <th>Latency</th>
        <th>Status Respons</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="mono">2026-11-15 01:04:12</td>
        <td><code>inventory_levels/set</code></td>
        <td class="mono" style="color: #38bdf8;">BGE-TS-001-BLK-L</td>
        <td style="color: #ef4444; font-weight: 700;">-1 (Penjualan POS)</td>
        <td class="mono">118ms</td>
        <td><span style="color: #4ade80; font-weight: 700;">200 OK (Synchronized)</span></td>
      </tr>
      <tr>
        <td class="mono">2026-11-15 00:58:34</td>
        <td><code>products/update</code></td>
        <td class="mono" style="color: #38bdf8;">BGE-CP-004-OLV</td>
        <td style="color: #3b82f6; font-weight: 700;">+24 (Restock Gudang)</td>
        <td class="mono">142ms</td>
        <td><span style="color: #4ade80; font-weight: 700;">200 OK (Synchronized)</span></td>
      </tr>
      <tr>
        <td class="mono">2026-11-15 00:45:10</td>
        <td><code>orders/create</code></td>
        <td class="mono" style="color: #38bdf8;">BGE-HD-002-CHR-XL</td>
        <td style="color: #ef4444; font-weight: 700;">-2 (Order Shopify)</td>
        <td class="mono">98ms</td>
        <td><span style="color: #4ade80; font-weight: 700;">200 OK (Staging Merged)</span></td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

render(stock_logs_html, 'stock_logs.html', f'{SC_DIR}/stock_shopify_sync_logs.png', '1200,714')

print("All Geodipa & BGE enterprise screenshots rendered!")
