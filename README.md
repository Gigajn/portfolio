# Portofolio Gigajn — Machine Learning & AI Engineer

Portofolio proyek Machine Learning, NLP, computer vision, sistem multi-agent LLM, dan rekayasa
perangkat lunak. Setiap proyek terhubung ke repositori atau demonya.

## Struktur

- `public/index.html` — halaman portofolio (HTML, CSS, JS tanpa framework).
- `public/projects.json` — data proyek. Ubah berkas ini untuk menambah atau mengedit proyek.
- `public/screenshots/` — tangkapan layar proyek.
- `src/main.rs` — server Rust (hanya `std`) untuk menjalankan situs secara lokal, beserta API
  `GET/POST/PUT/DELETE /api/projects` untuk mengelola `projects.json`.

## Menjalankan secara lokal

```bash
./run.sh            # atau: cargo run --release
# buka http://localhost:3000
```

## Deploy ke GitHub Pages

Halaman portofolio bersifat statis: `index.html` mencoba `./api/projects` lalu otomatis
memakai `projects.json` bila API tidak tersedia. Karena itu situs bisa di-hosting di GitHub Pages
tanpa server Rust.

Workflow `.github/workflows/pages.yml` berjalan setiap push ke `main`: mengecek kompilasi server
Rust, menyalin berkas situs dari `public/`, lalu mempublikasikannya.

Aktifkan sekali di **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Situs akan tersedia di `https://gigajn.github.io/portfolio/`.

API tulis (`POST/PUT/DELETE`) hanya berfungsi saat server Rust berjalan lokal; di GitHub Pages,
ubah `projects.json` lalu push.
