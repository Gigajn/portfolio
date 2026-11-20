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
# 1. Dairy Apps: LifeChapter Timeline (412x860)
# -----------------------------------------------------------------------------
dairy_timeline_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>LifeChapter — AI Diary & Memoir</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 412px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #fdfbf7; color: #2d312e;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .app-bar {
    padding: 38px 20px 16px; background: #ffffff;
    border-bottom: 1px solid #f1ece4;
    display: flex; justify-content: space-between; align-items: center;
  }
  .content { flex: 1; padding: 18px 20px; display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
  
  .mood-card {
    background: #ffffff; border: 1px solid #eee8df; border-radius: 16px;
    padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  }
  .mood-row { display: flex; justify-content: space-between; margin-top: 10px; }
  .mood-pill {
    padding: 8px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;
    border: 1px solid #eee8df; background: #faf8f5;
  }
  .mood-active { background: #4a6b44; color: white; border-color: #4a6b44; }

  .story-card {
    background: linear-gradient(135deg, #2d3b2f 0%, #1e2820 100%);
    color: #ffffff; border-radius: 18px; padding: 20px;
    box-shadow: 0 10px 25px -5px rgba(45, 59, 47, 0.25);
  }
  
  .entry-card {
    background: #ffffff; border: 1px solid #eee8df; border-radius: 16px;
    padding: 16px; display: flex; flex-direction: column; gap: 8px;
  }

  .nav-bar {
    height: 64px; background: #ffffff; border-top: 1px solid #eee8df;
    display: grid; grid-template-columns: repeat(4, 1fr);
    align-items: center; text-align: center; font-size: 0.68rem; font-weight: 700; color: #8c9288;
  }
  .nav-active { color: #4a6b44; }
</style>
</head>
<body>
  <div class="app-bar">
    <div>
      <div style="font-size: 0.72rem; color: #8c9288; font-weight: 600;">Kamis, 14 November 2024</div>
      <div style="font-size: 1.15rem; font-weight: 800; color: #2d3b2f;">LifeChapter</div>
    </div>
    <div style="width: 36px; height: 36px; background: #f4efe6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">
      ✍️
    </div>
  </div>

  <div class="content">
    <div class="mood-card">
      <div style="font-size: 0.72rem; font-weight: 700; color: #8c9288; text-transform: uppercase;">Mood Hari Ini</div>
      <div class="mood-row">
        <div class="mood-pill mood-active">🌿 Tenang & Fokus</div>
        <div class="mood-pill">💡 Terinspirasi</div>
        <div class="mood-pill">⚡ Bersemangat</div>
      </div>
    </div>

    <div class="story-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.7rem; font-weight: 700; color: #a3c29d; text-transform: uppercase;">✨ AI Chapter Generator</span>
        <span style="font-size: 0.68rem; opacity: 0.8;">Bab 11 &bull; Hal 42</span>
      </div>
      <div style="font-size: 0.92rem; font-weight: 700; margin-top: 8px; line-height: 1.5; color: #f2f7f1;">
        "Hari ini langkah terasa lebih mantap di antara baris kode dan kopi pagi. Bukan tentang seberapa cepat kita sampai, melainkan kejelasan arah yang kita pilih..."
      </div>
      <div style="font-size: 0.7rem; color: #a3c29d; margin-top: 8px; font-weight: 600;">
        Transformasi Narasi dari Catatan Harian 08:30 WIB
      </div>
    </div>

    <div class="entry-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong style="font-size: 0.85rem; color: #2d3b2f;">Refleksi Arsitektur Sistem</strong>
        <span style="font-size: 0.7rem; color: #8c9288;">14:15 WIB</span>
      </div>
      <p style="font-size: 0.75rem; color: #5f665a; line-height: 1.4;">
        Menyelesaikan integrasi zero-copy transport pada cluster backend. Rasa puas saat latency turun 60% tanpa mengorbankan keamanan.
      </p>
      <div style="display: flex; gap: 8px; margin-top: 4px;">
        <span style="background: #f4efe6; padding: 2px 8px; border-radius: 9999px; font-size: 0.68rem; font-weight: 700; color: #4a6b44;">#Engineering</span>
        <span style="background: #f4efe6; padding: 2px 8px; border-radius: 9999px; font-size: 0.68rem; font-weight: 700; color: #4a6b44;">#Fokus</span>
      </div>
    </div>
  </div>

  <div class="nav-bar">
    <div class="nav-active">Jurnal</div>
    <div>Memoir AI</div>
    <div>Analitik</div>
    <div>Pengaturan</div>
  </div>
</body>
</html>
"""

render(dairy_timeline_html, 'dairy_timeline.html', f'{SC_DIR}/dairy_apps_timeline.png', '412,860')
render(dairy_timeline_html, 'dairy_timeline.html', f'{SC_DIR}/dairy_apps.png', '412,860')


# -----------------------------------------------------------------------------
# 2. Jackup: Systems Terminal (1100x640)
# -----------------------------------------------------------------------------
jackup_term_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Jackup — Systems CLI & Daemon (Rust Tokio)</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1100px; height: 640px;
    font-family: 'JetBrains Mono', monospace;
    background: #0d1117; color: #c9d1d9;
    display: flex; flex-direction: column; overflow: hidden;
  }
  .term-header {
    height: 38px; background: #161b22; border-bottom: 1px solid #30363d;
    display: flex; align-items: center; padding: 0 16px; position: relative;
  }
  .dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .term-title {
    position: absolute; left: 50%; transform: translateX(-50%);
    font-size: 0.75rem; color: #8b949e; font-weight: 600;
  }
  .term-body {
    flex: 1; padding: 22px 24px; font-size: 0.85rem; line-height: 1.6;
    overflow: hidden; display: flex; flex-direction: column; gap: 6px;
  }
  .prompt { color: #58a6ff; font-weight: 700; }
  .cmd { color: #f0f6fc; font-weight: 600; }
  .info { color: #79c0ff; }
  .success { color: #56d364; }
  .warn { color: #e3b341; }
  .prog-bar { color: #56d364; font-weight: 700; }
</style>
</head>
<body>
  <div class="term-header">
    <div class="dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="term-title">kudo@thinkpad — zsh — jackup sync --volume db_data --target node-02.prod</div>
  </div>
  <div class="term-body">
    <div><span class="prompt">❯</span> <span class="cmd">jackup sync --volume db_data --target 10.240.0.12:9443 --crypto chacha20 --compress zstd</span></div>
    <div><span class="info">[2026-11-15T01:05:01Z INFO  jackup_core::daemon]</span> Handshake established with target node-02 (TLS 1.3 / mTLS verified)</div>
    <div><span class="info">[2026-11-15T01:05:01Z INFO  jackup_crypto]</span> Deriving master transport key with Argon2id (m=64MB, t=3, p=4)... <span class="success">[14ms]</span></div>
    <div><span class="info">[2026-11-15T01:05:01Z INFO  jackup_crypto]</span> AEAD cipher initialized: ChaCha20-Poly1305 stream channel active</div>
    <div><span class="info">[2026-11-15T01:05:02Z INFO  jackup_sync::scanner]</span> Scanning volume /var/lib/docker/volumes/db_data/_data</div>
    <div><span class="info">[2026-11-15T01:05:02Z INFO  jackup_sync::scanner]</span> 42,180 inodes indexed. Change delta: 8,412 modified blocks (14.2 GB)</div>
    <div><span class="info">[2026-11-15T01:05:03Z INFO  jackup_transport]</span> Spawning 8 Tokio async worker pipelines with zero-copy splicing</div>
    <div style="margin-top: 8px;">
      <span class="prog-bar">Transfer: [===================================>-------] 82.4% (11.7 GB / 14.2 GB)</span>
    </div>
    <div>Throughput: <span class="success">412.5 MB/s</span> | Active Workers: 8 Tokio tasks | ETA: 6s | Checksum: SHA-256 match</div>
    <div style="margin-top: 10px; color: #8b949e;">// Jackup: High-performance container volume migration daemon (Rust Tokio async)</div>
  </div>
</body>
</html>
"""

render(jackup_term_html, 'jackup_term.html', f'{SC_DIR}/jackup_cli.png', '1100,640')
render(jackup_term_html, 'jackup_term.html', f'{SC_DIR}/jackup_dry_run.png', '1100,640')


# -----------------------------------------------------------------------------
# 3. Games AR: Unity 3D AR Foundation Mobile Viewfinder (412x860)
# -----------------------------------------------------------------------------
char_img_path = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots/games_ar/character_10.png'
games_ar_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Interactive AR — Unity 3D & AR Foundation</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 412px; height: 860px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #181d24; color: #ffffff;
    display: flex; flex-direction: column; overflow: hidden;
    position: relative;
  }}
  .hud-top {{
    position: absolute; top: 0; left: 0; right: 0; z-index: 20;
    padding: 38px 18px 12px;
    display: flex; justify-content: space-between; align-items: center;
    background: linear-gradient(180deg, rgba(0,0,0,0.7) 0%, transparent 100%);
  }}
  .fps-pill {{
    background: rgba(0,0,0,0.5); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2); padding: 4px 10px;
    border-radius: 9999px; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;
    color: #4ade80; font-weight: 700;
  }}
  
  /* Plane Grid */
  .plane-grid {{
    position: absolute; bottom: 120px; left: 40px; right: 40px; height: 260px;
    border: 2px dashed rgba(56, 189, 248, 0.4); border-radius: 50%;
    transform: perspective(600px) rotateX(65deg);
    background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
  }}

  /* 3D Character */
  .character-stage {{
    position: absolute; top: 210px; left: 50%; transform: translateX(-50%);
    width: 280px; height: 400px; z-index: 10;
    display: flex; align-items: center; justify-content: center;
  }}
  .character-stage img {{
    max-width: 100%; max-height: 100%; object-fit: contain;
    filter: drop-shadow(0 25px 20px rgba(0,0,0,0.6));
  }}

  .hud-bottom {{
    position: absolute; bottom: 24px; left: 16px; right: 16px; z-index: 20;
    background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 16px;
    padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;
  }}
  .hud-btn {{
    background: #2563eb; color: white; border: none; padding: 8px 14px;
    border-radius: 10px; font-size: 0.75rem; font-weight: 800;
  }}
</style>
</head>
<body>
  <div class="hud-top">
    <div class="fps-pill">60.0 FPS &bull; ARCore Plane Tracked</div>
    <div style="font-size: 0.72rem; font-weight: 700; color: #cbd5e1;">Unity 3D Engine</div>
  </div>

  <div class="plane-grid"></div>

  <div class="character-stage">
    <img src="file://{char_img_path}" alt="AR Character">
  </div>

  <div class="hud-bottom">
    <div>
      <div style="font-weight: 800; font-size: 0.85rem; color: #38bdf8;">Image Target: Karakter #10</div>
      <div style="font-size: 0.7rem; color: #94a3b8;">Transformasi Pose Spasial Stabil</div>
    </div>
    <button class="hud-btn">Trigger Animasi ▶</button>
  </div>
</body>
</html>
"""

render(games_ar_html, 'games_ar.html', f'{SC_DIR}/games_ar/android_large_8.png', '412,860')


# -----------------------------------------------------------------------------
# 4. Oodin Games: Artboard Design Kit (1600x900)
# -----------------------------------------------------------------------------
oodin_dokar = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots/oodin/dokar.png'
oodin_bajaj = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots/oodin/bajaj.png'
oodin_becak = '/home/kudo/Projects/Portofolio/portfolio_rust/public/screenshots/oodin/becak.png'

oodin_artboard_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Oodin Games — 2D Traditional Transport Asset Kit</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1600px; height: 900px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #0f172a; color: #f8fafc;
    padding: 36px 48px; display: flex; flex-direction: column; gap: 28px;
    overflow: hidden;
  }}
  header {{
    display: flex; justify-content: space-between; align-items: flex-start;
    border-bottom: 1px solid #1e293b; padding-bottom: 20px;
  }}
  .vehicle-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; flex: 1;
  }}
  .vehicle-card {{
    background: #1e293b; border: 1px solid #334155; border-radius: 18px;
    padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: space-between;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
  }}
  .vehicle-img {{
    flex: 1; display: flex; align-items: center; justify-content: center;
    max-height: 200px; width: 100%;
  }}
  .vehicle-img img {{
    max-width: 90%; max-height: 190px; object-fit: contain;
    filter: drop-shadow(0 15px 15px rgba(0,0,0,0.5));
  }}
</style>
</head>
<body>
  <header>
    <div>
      <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px;">
        Game Asset Design Showcase &bull; 2D Vector Kit
      </div>
      <h1 style="font-size: 2rem; font-weight: 800; color: #ffffff; margin-top: 4px;">
        Oodin Games: Kendaraan Tradisional Nusantara
      </h1>
      <p style="font-size: 0.9rem; color: #94a3b8; margin-top: 4px;">
        Aset grafis game modular (Bajaj, Becak, Dokar) siap animasi fisika 2D untuk Unity & Godot Engine.
      </p>
    </div>
    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 10px 20px; border-radius: 12px; font-weight: 800; color: #38bdf8;">
      Atlas Sprites &bull; 4K Retina Vector
    </div>
  </header>

  <div class="vehicle-grid">
    <div class="vehicle-card">
      <div class="vehicle-img"><img src="file://{oodin_bajaj}" alt="Bajaj"></div>
      <div style="text-align: center; width: 100%; border-top: 1px solid #334155; padding-top: 14px;">
        <div style="font-weight: 800; font-size: 1.15rem; color: white;">Bajaj Klasik Metropolitan</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Komponen Modular: Roda 3, Kemudi, Mesin 2-Tak</div>
      </div>
    </div>

    <div class="vehicle-card">
      <div class="vehicle-img"><img src="file://{oodin_becak}" alt="Becak"></div>
      <div style="text-align: center; width: 100%; border-top: 1px solid #334155; padding-top: 14px;">
        <div style="font-weight: 800; font-size: 1.15rem; color: white;">Becak Kayuh Tradisional</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Komponen Modular: Sasis Rangka, Tenda, Kanopi</div>
      </div>
    </div>

    <div class="vehicle-card">
      <div class="vehicle-img"><img src="file://{oodin_dokar}" alt="Dokar"></div>
      <div style="text-align: center; width: 100%; border-top: 1px solid #334155; padding-top: 14px;">
        <div style="font-weight: 800; font-size: 1.15rem; color: white;">Dokar / Delman Wisata</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Komponen Modular: Roda Kayu Jari-Jari, Kusir</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

render(oodin_artboard_html, 'oodin_artboard.html', f'{SC_DIR}/oodin/odin_games_logo.png', '1600,900')

print("All mobile, terminal, and games screenshots rendered!")
