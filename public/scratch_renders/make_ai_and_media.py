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
# 1. Klasifikasi Stunting: Clinical AI Dashboard (1366x768)
# -----------------------------------------------------------------------------
stunting_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Childer Growth Guardian — Deteksi Stunting (WHO Standards)</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
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
    padding: 0 28px;
  }
  .layout { flex: 1; display: flex; padding: 20px 28px; gap: 20px; overflow: hidden; }
  .panel-left { width: 440px; background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 22px; display: flex; flex-direction: column; gap: 14px; }
  .panel-right { flex: 1; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  
  .form-group { display: flex; flex-direction: column; gap: 4px; }
  .form-lbl { font-size: 0.72rem; font-weight: 700; color: #475569; text-transform: uppercase; }
  .form-val { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 12px; font-size: 0.8rem; font-weight: 600; }
  
  .diag-card {
    background: #fef2f2; border: 1px solid #fecaca; border-radius: 14px;
    padding: 16px 20px; display: flex; justify-content: space-between; align-items: center;
  }
  .chart-box {
    flex: 1; background: white; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 20px; display: flex; flex-direction: column; position: relative;
  }
</style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 36px; height: 36px; background: #0f766e; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.1rem;">CG</div>
      <div>
        <div style="font-weight: 800; font-size: 1rem; color: #0f172a;">Childer Growth Guardian — Skrining Antropometri Balita</div>
        <div style="font-size: 0.72rem; color: #64748b;">Model Artificial Neural Network (Keras / TensorFlow) &bull; Standar Baku WHO</div>
      </div>
    </div>
    <div style="font-size: 0.75rem; font-weight: 700; background: #ccfbf1; color: #0f766e; padding: 6px 14px; border-radius: 9999px;">
      Akurasi Model: 96.4%
    </div>
  </header>

  <div class="layout">
    <div class="panel-left">
      <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
        Parameter Antropometri Pasien
      </div>
      <div class="form-group">
        <div class="form-lbl">Nama Balita</div>
        <div class="form-val">Muhammad Rizky Pratama</div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="form-group">
          <div class="form-lbl">Usia Pasien</div>
          <div class="form-val">24 Bulan</div>
        </div>
        <div class="form-group">
          <div class="form-lbl">Jenis Kelamin</div>
          <div class="form-val">Laki-laki</div>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="form-group">
          <div class="form-lbl">Tinggi Badan (TB)</div>
          <div class="form-val" style="color: #b91c1c; font-weight: 800;">78.2 cm (-2.8 SD)</div>
        </div>
        <div class="form-group">
          <div class="form-lbl">Berat Badan (BB)</div>
          <div class="form-val">9.4 kg (-2.3 SD)</div>
        </div>
      </div>
      <div class="form-group">
        <div class="form-lbl">Lingkar Kepala</div>
        <div class="form-val">47.0 cm (Normal)</div>
      </div>
      
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px; margin-top: auto; font-size: 0.72rem; color: #166534; line-height: 1.4;">
        <strong>Protokol Medis Kemenkes:</strong> Rujuk ke Puskesmas Pembantu untuk Pemberian Makanan Tambahan (PMT) Pemulihan dan asupan protein hewani tinggi.
      </div>
    </div>

    <div class="panel-right">
      <div class="diag-card">
        <div>
          <div style="font-size: 0.72rem; font-weight: 700; color: #991b1b; text-transform: uppercase;">Diagnosis Prediktif AI</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: #b91c1c; margin-top: 2px;">
            ⚠️ Terindikasi Stunting (Severely Stunted)
          </div>
          <div style="font-size: 0.75rem; color: #7f1d1d; margin-top: 2px;">
            Tinggi badan berada di bawah -2 Standar Deviasi kurva pertumbuhan WHO (TB/U: -2.8 SD)
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 1.8rem; font-weight: 800; color: #b91c1c;">96.4%</div>
          <div style="font-size: 0.7rem; font-weight: 700; color: #7f1d1d;">ANN Confidence</div>
        </div>
      </div>

      <div class="chart-box">
        <div style="display: flex; justify-content: space-between; margin-bottom: 14px;">
          <div>
            <div style="font-weight: 800; font-size: 0.9rem; color: #0f172a;">Kurva Pertumbuhan WHO (Tinggi Badan menurut Usia Balita)</div>
            <div style="font-size: 0.72rem; color: #64748b;">Standar WHO Child Growth Standards (Boys 0-36 Bulan)</div>
          </div>
          <div style="display: flex; gap: 12px; font-size: 0.7rem; font-weight: 600;">
            <span style="color: #166534;">● Rentang Normal (-2SD s/d +2SD)</span>
            <span style="color: #b91c1c;">● Titik Pasien (-2.8 SD)</span>
          </div>
        </div>

        <svg style="flex: 1; width: 100%;" viewBox="0 0 800 360">
          <!-- Grid Lines -->
          <line x1="60" y1="30" x2="60" y2="310" stroke="#e2e8f0" stroke-width="1"/>
          <line x1="60" y1="310" x2="760" y2="310" stroke="#cbd5e1" stroke-width="1.5"/>
          <line x1="60" y1="240" x2="760" y2="240" stroke="#f1f5f9" stroke-width="1"/>
          <line x1="60" y1="170" x2="760" y2="170" stroke="#f1f5f9" stroke-width="1"/>
          <line x1="60" y1="100" x2="760" y2="100" stroke="#f1f5f9" stroke-width="1"/>

          <!-- WHO Normal Green Band Area -->
          <polygon points="60,260 230,220 410,170 590,130 760,90 760,180 590,220 410,250 230,280 60,300" 
                   fill="rgba(34, 197, 94, 0.15)"/>
          
          <!-- +2 SD line -->
          <path d="M 60 260 Q 410 170 760 90" fill="none" stroke="#22c55e" stroke-width="2"/>
          <!-- Median (0 SD) line -->
          <path d="M 60 280 Q 410 210 760 135" fill="none" stroke="#16a34a" stroke-width="2" stroke-dasharray="6,4"/>
          <!-- -2 SD Stunting Threshold line -->
          <path d="M 60 300 Q 410 250 760 180" fill="none" stroke="#eab308" stroke-width="2"/>
          <!-- -3 SD Severe Stunting line -->
          <path d="M 60 310 Q 410 270 760 210" fill="none" stroke="#ef4444" stroke-width="2"/>

          <!-- Patient Data Point at Month 24 (X=590, Y=255) -->
          <circle cx="590" cy="255" r="7" fill="#dc2626" stroke="#ffffff" stroke-width="2.5"/>
          <circle cx="590" cy="255" r="14" fill="none" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,3"/>
          <text x="590" y="285" fill="#b91c1c" font-size="12" font-weight="800" text-anchor="middle">Rizky (78.2 cm)</text>

          <!-- Axes Labels -->
          <text x="60" y="330" fill="#64748b" font-size="11" font-weight="600">0 Bln</text>
          <text x="230" y="330" fill="#64748b" font-size="11" font-weight="600">8 Bln</text>
          <text x="410" y="330" fill="#64748b" font-size="11" font-weight="600">16 Bln</text>
          <text x="590" y="330" fill="#64748b" font-size="11" font-weight="800">24 Bulan</text>
          <text x="760" y="330" fill="#64748b" font-size="11" font-weight="600">32 Bln</text>
        </svg>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(stunting_html, 'stunting.html', f'{SC_DIR}/klasifikasi_stunting.png', '1366,768')


# -----------------------------------------------------------------------------
# 2. Klasifikasi Bansos: Civic ML Dashboard (1366x768)
# -----------------------------------------------------------------------------
bansos_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Sistem Rekomendasi Bansos — Desa Karangrau</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
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
    padding: 0 28px;
  }
  .layout { flex: 1; display: flex; padding: 20px 28px; gap: 20px; overflow: hidden; }
  .card-left { width: 440px; background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
  .card-right { flex: 1; display: flex; flex-direction: column; gap: 16px; }
  
  .metric-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 16px 20px; display: flex; justify-content: space-between; align-items: center;
  }
</style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 36px; height: 36px; background: #1e3a8a; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.1rem;">BS</div>
      <div>
        <div style="font-weight: 800; font-size: 1rem; color: #0f172a;">Sistem Rekomendasi Kelayakan Bantuan Sosial (PKH & BPNT)</div>
        <div style="font-size: 0.72rem; color: #64748b;">Desa Karangrau &bull; Algoritma: XGBoost Classifier & Random Forest (OvR/OvO)</div>
      </div>
    </div>
    <div style="display: flex; gap: 10px;">
      <span style="font-size: 0.75rem; font-weight: 700; background: #dbeafe; color: #1e40af; padding: 6px 14px; border-radius: 9999px;">
        F1-Score: 0.924
      </span>
    </div>
  </header>

  <div class="layout">
    <div class="card-left">
      <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
        Profil Demografi & Kemiskinan KK
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Nama KK:</span>
        <strong style="color: #0f172a;">Suparman</strong>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">NIK:</span>
        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">3302120804750002</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Alamat:</span>
        <span>RT 03 / RW 02 Karangrau</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Kondisi Dinding:</span>
        <strong style="color: #b45309;">Anyaman Bambu / Gedek</strong>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Jenis Lantai:</span>
        <strong style="color: #b45309;">Tanah</strong>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Sanitasi & MCK:</span>
        <span>MCK Umum Bersama</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Daya Listrik:</span>
        <span>450 VA Non-Subsidi</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
        <span style="color: #64748b;">Tanggungan Sekolah:</span>
        <strong style="color: #1e40af;">3 Anak (SD, SMP)</strong>
      </div>
    </div>

    <div class="card-right">
      <div class="metric-card" style="border-left: 5px solid #16a34a;">
        <div>
          <div style="font-size: 0.72rem; font-weight: 700; color: #166534; text-transform: uppercase;">Rekomendasi Bantuan 1</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: #15803d; margin-top: 2px;">
            ✓ SANGAT LAYAK MENERIMA PKH
          </div>
          <div style="font-size: 0.75rem; color: #475569; margin-top: 2px;">Komponen: Anak Usia Sekolah & Kesejahteraan Keluarga</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 1.8rem; font-weight: 800; color: #16a34a;">89.2%</div>
          <div style="font-size: 0.7rem; font-weight: 700; color: #166534;">XGBoost Probabilitas</div>
        </div>
      </div>

      <div class="metric-card" style="border-left: 5px solid #2563eb;">
        <div>
          <div style="font-size: 0.72rem; font-weight: 700; color: #1e40af; text-transform: uppercase;">Rekomendasi Bantuan 2</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: #1d4ed8; margin-top: 2px;">
            ✓ LAYAK MENERIMA BPNT (SEMBAKO)
          </div>
          <div style="font-size: 0.75rem; color: #475569; margin-top: 2px;">Komponen: Indikator Kerawanan Pangan & Pendapatan Rendah</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 1.8rem; font-weight: 800; color: #2563eb;">92.5%</div>
          <div style="font-size: 0.7rem; font-weight: 700; color: #1e40af;">Random Forest Probabilitas</div>
        </div>
      </div>

      <div style="background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; flex: 1;">
        <div style="font-weight: 800; font-size: 0.85rem; color: #0f172a; margin-bottom: 10px;">Prioritas Seleksi Desa (Musyawarah Dusun)</div>
        <div style="font-size: 0.75rem; color: #64748b;">
          Berdasarkan perangkingan probabilitas gabungan, Suparman berada pada <strong>Peringkat #2</strong> dari 45 calon penerima di Dusun Karangrau II. Rekomendasi siap diekspor ke berita acara musyawarah desa.
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(bansos_html, 'bansos.html', f'{SC_DIR}/klasifikasi_bansos.png', '1366,768')


# -----------------------------------------------------------------------------
# 3. TikTok Scraper: Threat Intel & NLP Judol Filter (1366x768)
# -----------------------------------------------------------------------------
tiktok_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>TikTok Comment NLP Filter — Threat Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #090d16; color: #e2e8f0;
    display: flex; flex-direction: column; overflow: hidden;
  }
  header {
    height: 60px; background: #0b1120; border-bottom: 1px solid #1e293b;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px;
  }
  .layout { flex: 1; display: flex; flex-direction: column; padding: 20px 28px; gap: 16px; overflow: hidden; }
  
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .kpi-card { background: #131b2e; border: 1px solid #1e293b; border-radius: 12px; padding: 14px 18px; }
  
  .stream-box {
    flex: 1; background: #131b2e; border: 1px solid #1e293b; border-radius: 14px;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .comment-item {
    padding: 12px 18px; border-bottom: 1px solid #1e293b;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem;
  }
  .tag-danger {
    background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444;
    color: #f87171; padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.7rem;
  }
  .tag-clean {
    background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e;
    color: #4ade80; padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.7rem;
  }
  .token-pill {
    background: rgba(239, 68, 68, 0.3); color: #fca5a5;
    padding: 1px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  }
</style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 36px; height: 36px; background: #e11d48; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.1rem;">TK</div>
      <div>
        <div style="font-weight: 800; font-size: 1rem; color: #ffffff;">TikTok Comment Scraper & NLP Judol Spam Detector</div>
        <div style="font-size: 0.72rem; color: #94a3b8;">Playwright Headless Stealth &bull; TF-IDF Vectorizer &bull; Multinomial Naive Bayes</div>
      </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
      <span style="font-size: 0.75rem; font-weight: 700; background: rgba(34, 197, 94, 0.15); color: #4ade80; padding: 6px 14px; border-radius: 9999px; border: 1px solid rgba(34, 197, 94, 0.3);">
        ● Stealth Worker Connected
      </span>
    </div>
  </header>

  <div class="layout">
    <div class="kpi-row">
      <div class="kpi-card">
        <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff;">1,850</div>
        <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 600;">Komentar Terpanen</div>
      </div>
      <div class="kpi-card">
        <div style="font-size: 1.4rem; font-weight: 800; color: #f87171;">342 (18.5%)</div>
        <div style="font-size: 0.72rem; color: #f87171; font-weight: 600;">Promosi Judol Terdeteksi</div>
      </div>
      <div class="kpi-card">
        <div style="font-size: 1.4rem; font-weight: 800; color: #fbbf24;">128 (6.9%)</div>
        <div style="font-size: 0.72rem; color: #fbbf24; font-weight: 600;">Spam Afiliasi & Bot</div>
      </div>
      <div class="kpi-card">
        <div style="font-size: 1.4rem; font-weight: 800; color: #4ade80;">1,380 (74.6%)</div>
        <div style="font-size: 0.72rem; color: #4ade80; font-weight: 600;">Komentar Alami Bersih</div>
      </div>
    </div>

    <div class="stream-box">
      <div style="padding: 12px 18px; border-bottom: 1px solid #1e293b; font-weight: 800; font-size: 0.85rem; color: white;">
        Feed Komentar Terklasifikasi Real-Time
      </div>
      
      <div class="comment-item">
        <div>
          <div style="font-weight: 700; color: #ffffff;">@bocah_gacor99</div>
          <div style="color: #cbd5e1; margin-top: 2px;">
            MODAL RECEH PASTI JP <span class="token-pill">gacor</span> MAXWIN klik link bio admin WA 0812xxxx
          </div>
          <div style="margin-top: 4px; font-size: 0.7rem; color: #94a3b8;">Trigger Tokens: gacor [0.98], maxwin [0.95], link bio [0.91]</div>
        </div>
        <span class="tag-danger">⛔ JUDI ONLINE (99.4%)</span>
      </div>

      <div class="comment-item">
        <div>
          <div style="font-weight: 700; color: #ffffff;">@situs_resmi_asia</div>
          <div style="color: #cbd5e1; margin-top: 2px;">
            Situs terpercaya anti rungkad deposit 10rb langsung cuan gais cek profil
          </div>
        </div>
        <span class="tag-danger">⛔ JUDI ONLINE (98.7%)</span>
      </div>

      <div class="comment-item">
        <div>
          <div style="font-weight: 700; color: #ffffff;">@dani_gamers</div>
          <div style="color: #cbd5e1; margin-top: 2px;">
            Keren banget pembahasannya bang, build itemnya cocok buat rank Mythic
          </div>
        </div>
        <span class="tag-clean">✓ KOMENTAR NORMAL</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(tiktok_html, 'tiktok.html', f'{SC_DIR}/tiktok_scraper.png', '1366,768')


# -----------------------------------------------------------------------------
# 4. Split Downloader: Audio Extractor & Waveform Splitter (1366x768)
# -----------------------------------------------------------------------------
split_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>YouTube Split Downloader & Audio Workstation</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1366px; height: 768px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #e2e8f0;
    display: flex; flex-direction: column; overflow: hidden;
  }
  header {
    height: 60px; background: #0b1120; border-bottom: 1px solid #1e293b;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px;
  }
  .layout { flex: 1; padding: 22px 28px; display: flex; flex-direction: column; gap: 18px; overflow: hidden; }
  
  .album-box {
    background: #1e293b; border: 1px solid #334155; border-radius: 14px;
    padding: 18px 24px; display: flex; gap: 20px; align-items: center;
  }
  .waveform-card {
    flex: 1; background: #1e293b; border: 1px solid #334155; border-radius: 14px;
    padding: 20px; display: flex; flex-direction: column; gap: 14px; overflow: hidden;
  }
  .track-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 14px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;
    font-size: 0.78rem;
  }
  .mono { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #38bdf8; }
</style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 36px; height: 36px; background: #f59e0b; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #000; font-weight: 800; font-size: 1.1rem;">YT</div>
      <div>
        <div style="font-weight: 800; font-size: 1rem; color: #ffffff;">YouTube Split Downloader & Audio Track Slicer</div>
        <div style="font-size: 0.72rem; color: #94a3b8;">yt-dlp Engine &bull; FFmpeg Audio Slicing &bull; Multithreaded Background Job Manager</div>
      </div>
    </div>
    <div style="font-size: 0.75rem; font-weight: 700; background: rgba(245, 158, 11, 0.15); color: #fbbf24; padding: 6px 14px; border-radius: 9999px; border: 1px solid rgba(245, 158, 11, 0.3);">
      MP3 320 kbps &bull; Lossless Slicing
    </div>
  </header>

  <div class="layout">
    <div class="album-box">
      <div style="width: 80px; height: 80px; background: #334155; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 2.2rem;">
        🎵
      </div>
      <div style="flex: 1;">
        <div style="font-size: 1.1rem; font-weight: 800; color: white;">Lofi Beats for Coding & Deep Focus [Full Album]</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">
          Durasi: 01:08:42 &bull; 8 Chapters Terdeteksi &bull; Kanal: Chillhop Music
        </div>
      </div>
      <button style="background: #2563eb; color: white; border: none; font-weight: 800; padding: 12px 20px; border-radius: 10px; font-size: 0.82rem;">
        📦 Ekspor Semua Track (.ZIP)
      </button>
    </div>

    <div class="waveform-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="font-weight: 800; font-size: 0.88rem; color: white;">Waveform Audio & Pemotong Otomatis Berdasarkan Timestamp</div>
        <div style="font-size: 0.72rem; color: #4ade80; font-weight: 700;">● Worker #1 Aktif (8 Threads)</div>
      </div>

      <!-- Waveform Bars -->
      <div style="height: 60px; background: #0f172a; border: 1px solid #334155; border-radius: 10px; display: flex; align-items: center; gap: 3px; padding: 0 10px;">
        <div style="width: 4px; height: 35px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 50px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 28px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 42px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 20px; background: #f59e0b; border-radius: 2px;"></div>
        <div style="width: 4px; height: 48px; background: #f59e0b; border-radius: 2px;"></div>
        <div style="width: 4px; height: 32px; background: #f59e0b; border-radius: 2px;"></div>
        <div style="width: 4px; height: 40px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 25px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 52px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 30px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 44px; background: #38bdf8; border-radius: 2px;"></div>
        <div style="width: 4px; height: 18px; background: #38bdf8; border-radius: 2px;"></div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div class="track-row">
          <div>
            <strong>Track 01. Dawn Reflections</strong>
            <span class="mono" style="margin-left: 10px;">00:00 - 04:15</span>
          </div>
          <span style="color: #4ade80; font-weight: 700;">✓ Selesai Terpotong</span>
        </div>
        <div class="track-row">
          <div>
            <strong>Track 02. Rainy Terminal</strong>
            <span class="mono" style="margin-left: 10px;">04:15 - 08:32</span>
          </div>
          <span style="color: #4ade80; font-weight: 700;">✓ Selesai Terpotong</span>
        </div>
        <div class="track-row">
          <div>
            <strong>Track 03. Midnight Async</strong>
            <span class="mono" style="margin-left: 10px;">08:32 - 13:10</span>
          </div>
          <span style="color: #38bdf8; font-weight: 700;">Memproses (78%)...</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(split_html, 'split.html', f'{SC_DIR}/split_downloader.png', '1366,768')

print("All AI & Media screenshots rendered!")
