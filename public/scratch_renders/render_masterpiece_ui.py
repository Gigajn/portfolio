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
        print(f"Error rendering {fname}: {res.stderr[:200]}")
    else:
        print(f"  ✅ Rendered {os.path.basename(out_png)}")

print("Starting Masterpiece UI Render Engine...")
