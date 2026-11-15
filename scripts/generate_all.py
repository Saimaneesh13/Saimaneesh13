import os
import re
import html
from datetime import datetime, timedelta
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageEnhance

USERNAME = "Saimaneesh13"


# ---------------------------------------------------------
# 1. LIVE CONTRIBUTION HEATMAP SVG (contrib-heatmap.svg)
# ---------------------------------------------------------
def build_heatmap():
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    days = {}
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        d = td.get("data-date")
        lvl = td.get("data-level", "0")
        if d:
            days[d] = int(lvl)

    total_text = "Active Contributions in the last year"
    h2 = soup.find("h2", id="js-contribution-activity-description")
    if h2:
        total_text = " ".join(h2.get_text().split())

    today = datetime.utcnow().date()
    days_since_sunday = (today.weekday() + 1) % 7
    current_sunday = today - timedelta(days=days_since_sunday)
    start_sunday = current_sunday - timedelta(weeks=52)

    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    rects = []

    for w in range(53):
        for d in range(7):
            cell_date = start_sunday + timedelta(weeks=w, days=d)
            if cell_date > today:
                continue
            iso = cell_date.strftime("%Y-%m-%d")
            lvl = days.get(iso, 0)
            color = palette[min(lvl, 4)]
            x = 28 + w * 15
            y = 38 + d * 15
            delay = (w * 0.018) + (d * 0.03)
            rects.append(
                f'<rect x="{x}" y="{y}" width="11" height="11" rx="2.5" '
                f'fill="{color}" class="c" style="animation-delay:{delay:.2f}s"/>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 185" width="860" height="185">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; }}
    .txt {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8b949e; font-size: 12px; }}
    .title {{ fill: #c9d1d9; font-weight: 600; }}
    .c {{ opacity: 0; transform: translateY(-6px); animation: drop 0.35s ease-out forwards; }}
    @keyframes drop {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="859" height="184" rx="10"/>
  <text x="28" y="24" class="txt title">{html.escape(total_text)}</text>
  <text x="735" y="24" class="txt">saimaneesh13@github</text>
  {"".join(rects)}
  <text x="28" y="166" class="txt">Updated daily via GitHub Actions • Pure SVG</text>
  <text x="698" y="166" class="txt">Less</text>
  <rect x="732" y="156" width="11" height="11" rx="2.5" fill="#161b22"/>
  <rect x="746" y="156" width="11" height="11" rx="2.5" fill="#0e4429"/>
  <rect x="760" y="156" width="11" height="11" rx="2.5" fill="#006d32"/>
  <rect x="774" y="156" width="11" height="11" rx="2.5" fill="#26a641"/>
  <rect x="788" y="156" width="11" height="11" rx="2.5" fill="#39d353"/>
  <text x="806" y="166" class="txt">More</text>
</svg>'''

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 2. NEOFETCH INFO CARD SVG (info-card.svg)
# ---------------------------------------------------------
def build_info_card():
    lines = [
        ("saimaneesh13", "@", "arch-ai-ml", ""),
        ("──────────────────────────────", "", "", ""),
        ("OS", ": ", "AI / ML Engineer • Systems Builder", ""),
        ("Host", ": ", "Lovely Professional University (B.Tech CSE)", ""),
        ("Kernel", ": ", "Deep Learning · NLP · Computer Vision", ""),
        ("Experience", ": ", "ML Intern @ EduExpose (Best Award)", ""),
        ("Certs", ": ", "OCI 2025 AI Foundations (95%) · Rice Univ", ""),
        ("", "", "", ""),
        ("Portfolio", ": ", "my-portfolio-ten-bice-53.vercel.app", "#f5d76e"),
        ("Deploy [01]", ": ", "aegis-command.streamlit.app", "#39d353"),
        ("Deploy [02]", ": ", "agrodetectai.streamlit.app", "#39d353"),
        ("Deploy [03]", ": ", "facerecognitionattendance-9rc8.onrender.com", "#58a6ff"),
        ("", "", "", ""),
        ("Packages", ": ", "TensorFlow, Keras, PyTorch, OpenCV, Sklearn", ""),
        ("NLP Stack", ": ", "BERTopic, LDA, Sentence-BERT, UMAP, HDBSCAN", ""),
        ("Backend/UI", ": ", "FastAPI, Flask, Streamlit, SQLite, Vercel", ""),
        ("Mission", ": ", "Engineering Intelligence. Building What Matters.", "#d2a8ff"),
    ]

    row_svgs = []
    y = 58
    for idx, (k, sep, v, custom_col) in enumerate(lines):
        delay = 0.12 + idx * 0.09
        if idx == 0:
            row_svgs.append(
                f'<text x="24" y="{y}" class="line" style="animation-delay:{delay:.2f}s">'
                f'<tspan class="k">{k}</tspan><tspan class="sep">{sep}</tspan><tspan class="k">{v}</tspan></text>'
            )
        elif not k and not v:
            y += 8
            continue
        elif sep == "":
            row_svgs.append(
                f'<text x="24" y="{y}" class="line sep" style="animation-delay:{delay:.2f}s">{k}</text>'
            )
        else:
            val_style = f'fill:{custom_col};' if custom_col else ''
            row_svgs.append(
                f'<text x="24" y="{y}" class="line" style="animation-delay:{delay:.2f}s">'
                f'<tspan class="k">{html.escape(k)}</tspan>'
                f'<tspan class="sep">{html.escape(sep)}</tspan>'
                f'<tspan class="v" style="{val_style}">{html.escape(v)}</tspan></text>'
            )
        y += 20

    swatches = ["#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]
    dots = "".join(
        f'<rect x="{24 + i*24}" y="388" width="16" height="10" rx="2" fill="{c}" class="line" style="animation-delay:1.8s"/>'
        for i, c in enumerate(swatches)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 420" width="490" height="420">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; }}
    .bar {{ fill: #161b22; }}
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12.2px; }}
    .title {{ fill: #8b949e; font-size: 11.5px; }}
    .k {{ fill: #58a6ff; font-weight: 600; }}
    .sep {{ fill: #6e7681; }}
    .v {{ fill: #c9d1d9; }}
    .line {{ opacity: 0; transform: translateX(-8px); animation: slide 0.35s ease-out forwards; }}
    @keyframes slide {{ to {{ opacity: 1; transform: translateX(0); }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="489" height="419" rx="10"/>
  <path class="bar" d="M 1 10 Q 1 1 10 1 L 480 1 Q 489 1 489 10 L 489 32 L 1 32 Z"/>
  <circle cx="18" cy="16" r="5.5" fill="#ff5f56"/>
  <circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/>
  <circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
  <text x="175" y="20" class="title">neofetch — saimaneesh13</text>
  {"".join(row_svgs)}
  {dots}
</svg>'''

    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 3. SELF-TYPING ASCII PORTRAIT SVG (sai-ascii.svg)
# ---------------------------------------------------------
def build_ascii_portrait():
    cols, rows = 68, 42
    ramp = " .`:-=+*cs#%@"
    ascii_rows = []

    try:
        r = requests.get(f"https://github.com/{USERNAME}.png?size=400", timeout=15)
        img = Image.open(BytesIO(r.content)).convert("L")
        img = ImageOps.autocontrast(img, cutoff=2)
        img = ImageEnhance.Contrast(img).enhance(1.45)
        img = img.resize((cols, rows), Image.Resampling.LANCZOS)

        for y in range(rows):
            line = ""
            for x in range(cols):
                px = img.getpixel((x, y))
                # Map dark background edges cleanly and highlight subject features
                idx = int((px / 255.0) * (len(ramp) - 1))
                line += ramp[idx]
            ascii_rows.append(line)
    except Exception:
        ascii_rows = [" " * cols for _ in range(rows)]

    clips = []
    texts = []
    for i, line in enumerate(ascii_rows):
        y_pos = 46 + i * 8.5
        begin = i * 0.045
        clips.append(
            f'<clipPath id="r{i}"><rect x="14" y="{y_pos - 8}" width="0" height="11">'
            f'<animate attributeName="width" from="0" to="345" begin="{begin:.2f}s" dur="0.18s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        escaped = html.escape(line)
        texts.append(
            f'<text x="16" y="{y_pos:.1f}" clip-path="url(#r{i})" xml:space="preserve">{escaped}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 370 420" width="370" height="420">
  <defs>{"".join(clips)}</defs>
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; }}
    .bar {{ fill: #161b22; }}
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 7.4px; fill: #c9d1d9; letter-spacing: 0.4px; }}
    .title {{ font-size: 11.5px; fill: #8b949e; letter-spacing: 0px; }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="369" height="419" rx="10"/>
  <path class="bar" d="M 1 10 Q 1 1 10 1 L 360 1 Q 369 1 369 10 L 369 32 L 1 32 Z"/>
  <circle cx="18" cy="16" r="5.5" fill="#ff5f56"/>
  <circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/>
  <circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
  <text x="115" y="20" class="title">ascii — sai_maneesh.sh</text>
  {"".join(texts)}
</svg>'''

    with open("sai-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    build_heatmap()
    build_info_card()
    build_ascii_portrait()
