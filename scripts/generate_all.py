import html
from datetime import datetime, timedelta
from io import BytesIO
import math
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

USERNAME = "Saimaneesh13"


# ---------------------------------------------------------
# 1. ENHANCED CONTRIBUTION HEATMAP SVG (contrib-heatmap.svg)
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

    # Calculate Active Days, Longest Streak, Current Streak
    sorted_dates = sorted(days.keys())
    active_days = sum(1 for d in sorted_dates if days[d] > 0)
    longest_streak = 0
    curr = 0
    for d in sorted_dates:
        if days[d] > 0:
            curr += 1
            if curr > longest_streak:
                longest_streak = curr
        else:
            curr = 0

    palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    rects = []
    month_labels = []
    last_month = None

    for w in range(53):
        week_date = start_sunday + timedelta(weeks=w)
        x = 46 + w * 14.8
        if week_date.month != last_month and w < 51:
            m_name = week_date.strftime("%b")
            month_labels.append(f'<text x="{x:.1f}" y="44" class="sub">{m_name}</text>')
            last_month = week_date.month

        for d in range(7):
            cell_date = start_sunday + timedelta(weeks=w, days=d)
            if cell_date > today:
                continue
            iso = cell_date.strftime("%Y-%m-%d")
            lvl = days.get(iso, 0)
            color = palette[min(lvl, 4)]
            y = 52 + d * 14.5
            delay = (w * 0.016) + (d * 0.025)
            rects.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="11" height="11" rx="2.5" '
                f'fill="{color}" class="c" style="animation-delay:{delay:.2f}s"/>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 205" width="860" height="205">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.2px; }}
    .bar {{ fill: #161b22; }}
    .txt {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #8b949e; font-size: 11.5px; }}
    .sub {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; fill: #6e7681; font-size: 10px; }}
    .title {{ fill: #e6edf3; font-weight: 600; font-size: 12.5px; }}
    .hi {{ fill: #39d353; font-weight: 600; }}
    .gold {{ fill: #f5d76e; font-weight: 600; }}
    .c {{ opacity: 0; transform: translateY(-5px); animation: drop 0.35s ease-out forwards; }}
    @keyframes drop {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect class="bg" x="0.6" y="0.6" width="858.8" height="203.8" rx="10"/>
  <path class="bar" d="M 1.2 10 Q 1.2 1.2 10 1.2 L 850 1.2 Q 858.8 1.2 858.8 10 L 858.8 28 L 1.2 28 Z"/>
  <circle cx="16" cy="14.5" r="5" fill="#ff5f56"/>
  <circle cx="32" cy="14.5" r="5" fill="#ffbd2e"/>
  <circle cx="48" cy="14.5" r="5" fill="#27c93f"/>
  <text x="70" y="18.5" class="txt title">{html.escape(total_text)}</text>
  <text x="535" y="18.5" class="txt">Active Days: <tspan class="hi">{active_days}</tspan>  •  Best Streak: <tspan class="gold">{longest_streak}d</tspan></text>
  {"".join(month_labels)}
  <text x="16" y="75" class="sub">Mon</text>
  <text x="16" y="104" class="sub">Wed</text>
  <text x="16" y="133" class="sub">Fri</text>
  {"".join(rects)}
  <text x="16" y="184" class="txt">STATUS: <tspan class="hi">● ONLINE</tspan>  •  Auto-synced daily via GitHub Actions Cron</text>
  <text x="712" y="184" class="txt">Less</text>
  <rect x="744" y="174" width="11" height="11" rx="2.5" fill="#161b22"/>
  <rect x="758" y="174" width="11" height="11" rx="2.5" fill="#0e4429"/>
  <rect x="772" y="174" width="11" height="11" rx="2.5" fill="#006d32"/>
  <rect x="786" y="174" width="11" height="11" rx="2.5" fill="#26a641"/>
  <rect x="800" y="174" width="11" height="11" rx="2.5" fill="#39d353"/>
  <text x="816" y="184" class="txt">More</text>
</svg>'''

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 2. NEOFETCH INFO CARD SVG (info-card.svg)
# ---------------------------------------------------------
def build_info_card():
    lines = [
        ("saimaneesh13", "@", "ai-ml-workstation", ""),
        ("──────────────────────────────────────────────", "", "", ""),
        ("Identity", "   : ", "Gorrela Sai Maneesh", "#f5d76e"),
        ("Role", "       : ", "AI / ML Engineer & Intelligent Systems Builder", "#58a6ff"),
        ("Education", "  : ", "B.Tech CSE (AI & ML) @ Lovely Professional Univ", ""),
        ("Experience", " : ", "ML Intern @ EduExpose (Best Performance Award)", "#3fb950"),
        ("Focus", "      : ", "Deep Learning · NLP · Computer Vision · MLOps", ""),
        ("──────────────────────────────────────────────", "", "", ""),
        ("Portfolio", "  : ", "https://my-portfolio-ten-bice-53.vercel.app", "#f5d76e"),
        ("Aegis AI", "   : ", "https://aegis-command.streamlit.app", "#39d353"),
        ("AgroDetect", " : ", "https://agrodetectai.streamlit.app", "#39d353"),
        ("FaceVision", " : ", "https://facerecognitionattendance-9rc8.onrender.com", "#79c0ff"),
        ("──────────────────────────────────────────────", "", "", ""),
        ("Languages", "  : ", "Python · C++ · Java · C · SQL · Bash", ""),
        ("DL & CV", "    : ", "TensorFlow · Keras · PyTorch · OpenCV · Sklearn", ""),
        ("NLP Core", "   : ", "BERTopic · LDA · Sentence-BERT · UMAP · HDBSCAN", ""),
        ("Backend/UI", " : ", "FastAPI · Flask · Streamlit · SQLite · Bootstrap", ""),
        ("Mission", "    : ", "Engineering Intelligence. Building What Matters.", "#d2a8ff"),
    ]

    row_svgs = []
    y = 54
    for idx, (k, sep, v, custom_col) in enumerate(lines):
        delay = 0.10 + idx * 0.08
        if idx == 0:
            row_svgs.append(
                f'<text x="22" y="{y}" class="line" style="animation-delay:{delay:.2f}s">'
                f'<tspan class="k">{k}</tspan><tspan class="sep">{sep}</tspan><tspan class="gold">{v}</tspan></text>'
            )
        elif sep == "":
            row_svgs.append(
                f'<text x="22" y="{y}" class="line sep" style="animation-delay:{delay:.2f}s">{k}</text>'
            )
        else:
            val_style = f'fill:{custom_col};font-weight:600;' if custom_col else ''
            row_svgs.append(
                f'<text x="22" y="{y}" class="line" style="animation-delay:{delay:.2f}s" xml:space="preserve">'
                f'<tspan class="k">{html.escape(k)}</tspan>'
                f'<tspan class="sep">{html.escape(sep)}</tspan>'
                f'<tspan class="v" style="{val_style}">{html.escape(v)}</tspan></text>'
            )
        y += 19.5

    swatches = ["#ff7b72", "#3fb950", "#f5d76e", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3", "#6e7681"]
    dots = "".join(
        f'<rect x="{22 + i*26}" y="406" width="18" height="10" rx="2.5" fill="{c}" class="line" style="animation-delay:1.6s"/>'
        for i, c in enumerate(swatches)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 434" width="500" height="434">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.2px; }}
    .bar {{ fill: #161b22; }}
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11.8px; }}
    .title {{ fill: #8b949e; font-size: 11.5px; }}
    .k {{ fill: #58a6ff; font-weight: 600; }}
    .gold {{ fill: #f5d76e; font-weight: 600; }}
    .sep {{ fill: #484f58; }}
    .v {{ fill: #c9d1d9; }}
    .line {{ opacity: 0; transform: translateX(-8px); animation: slide 0.32s ease-out forwards; }}
    @keyframes slide {{ to {{ opacity: 1; transform: translateX(0); }} }}
  </style>
  <rect class="bg" x="0.6" y="0.6" width="498.8" height="432.8" rx="10"/>
  <path class="bar" d="M 1.2 10 Q 1.2 1.2 10 1.2 L 490 1.2 Q 498.8 1.2 498.8 10 L 498.8 30 L 1.2 30 Z"/>
  <circle cx="16" cy="15" r="5" fill="#ff5f56"/>
  <circle cx="32" cy="15" r="5" fill="#ffbd2e"/>
  <circle cx="48" cy="15" r="5" fill="#27c93f"/>
  <text x="180" y="19" class="title">neofetch — saimaneesh13</text>
  {"".join(row_svgs)}
  {dots}
</svg>'''

    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 3. HIGH-CONTRAST SELF-TYPING ASCII PORTRAIT (sai-ascii.svg)
# ---------------------------------------------------------
def build_ascii_portrait():
    cols, rows = 78, 46
    ramp = "  .`:-=+*cs#%@"
    ascii_rows = []

    try:
        r = requests.get(f"https://github.com/{USERNAME}.png?size=460", timeout=15)
        img = Image.open(BytesIO(r.content)).convert("L")
        img = ImageOps.autocontrast(img, cutoff=3)
        img = ImageEnhance.Sharpness(img).enhance(1.8)
        img = ImageEnhance.Contrast(img).enhance(1.55)
        img = img.resize((cols, rows), Image.Resampling.LANCZOS)

        cx, cy = cols / 2.0, rows / 2.0
        for y in range(rows):
            line = ""
            for x in range(cols):
                px = img.getpixel((x, y))
                # Soft radial mask to suppress noisy corner backgrounds
                dx = (x - cx) / (cols * 0.52)
                dy = (y - cy) / (rows * 0.54)
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 1.05 and px < 75:
                    line += " "
                elif px < 28:
                    line += " "
                else:
                    idx = int((px / 255.0) * (len(ramp) - 1))
                    line += ramp[idx]
            ascii_rows.append(line)
    except Exception:
        ascii_rows = [" " * cols for _ in range(rows)]

    clips = []
    texts = []
    for i, line in enumerate(ascii_rows):
        y_pos = 46 + i * 8.1
        begin = i * 0.038
        clips.append(
            f'<clipPath id="r{i}"><rect x="12" y="{y_pos - 7.5:.1f}" width="0" height="10">'
            f'<animate attributeName="width" from="0" to="332" begin="{begin:.2f}s" dur="0.16s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        escaped = html.escape(line)
        texts.append(
            f'<text x="14" y="{y_pos:.1f}" clip-path="url(#r{i})" xml:space="preserve">{escaped}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 434" width="350" height="434">
  <defs>{"".join(clips)}</defs>
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.2px; }}
    .bar {{ fill: #161b22; }}
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 6.6px; fill: #d0d7de; letter-spacing: 0.25px; }}
    .title {{ font-size: 11.5px; fill: #8b949e; letter-spacing: 0px; }}
  </style>
  <rect class="bg" x="0.6" y="0.6" width="348.8" height="432.8" rx="10"/>
  <path class="bar" d="M 1.2 10 Q 1.2 1.2 10 1.2 L 340 1.2 Q 348.8 1.2 348.8 10 L 348.8 30 L 1.2 30 Z"/>
  <circle cx="16" cy="15" r="5" fill="#ff5f56"/>
  <circle cx="32" cy="15" r="5" fill="#ffbd2e"/>
  <circle cx="48" cy="15" r="5" fill="#27c93f"/>
  <text x="108" y="19" class="title">ascii — sai_maneesh.sh</text>
  {"".join(texts)}
</svg>'''

    with open("sai-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 4. HTOP TELEMETRY & CREDENTIALS SVG (system-telemetry.svg)
# ---------------------------------------------------------
def build_telemetry():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 230" width="860" height="230">
  <style>
    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1.2px; }
    .bar { fill: #161b22; }
    text { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11.5px; fill: #c9d1d9; }
    .title { fill: #8b949e; font-size: 11.5px; }
    .sec { fill: #f5d76e; font-weight: 600; font-size: 12px; }
    .k { fill: #58a6ff; font-weight: 600; }
    .ok { fill: #39d353; font-weight: 600; }
    .muted { fill: #8b949e; }
    .track { fill: #21262d; }
    .fill-g { fill: #2ea043; animation: grow 1.1s ease-out forwards; transform-origin: left; }
    .fill-b { fill: #1f6feb; animation: grow 1.3s ease-out forwards; transform-origin: left; }
    .fill-p { fill: #8957e5; animation: grow 1.5s ease-out forwards; transform-origin: left; }
    .fill-y { fill: #d29922; animation: grow 1.7s ease-out forwards; transform-origin: left; }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  </style>
  <rect class="bg" x="0.6" y="0.6" width="858.8" height="228.8" rx="10"/>
  <path class="bar" d="M 1.2 10 Q 1.2 1.2 10 1.2 L 850 1.2 Q 858.8 1.2 858.8 10 L 858.8 30 L 1.2 30 Z"/>
  <circle cx="16" cy="15" r="5" fill="#ff5f56"/>
  <circle cx="32" cy="15" r="5" fill="#ffbd2e"/>
  <circle cx="48" cy="15" r="5" fill="#27c93f"/>
  <text x="310" y="19" class="title">htop — ai_telemetry &amp; verified_credentials</text>

  <!-- Left Column: AI Domain Telemetry Bars -->
  <text x="24" y="54" class="sec">◈ CORE AI / ML TELEMETRY</text>

  <text x="24" y="80" class="k">01 · Machine Learning &amp; Deep Learning</text>
  <text x="368" y="80" class="ok">94%</text>
  <rect class="track" x="24" y="87" width="370" height="8" rx="4"/>
  <rect class="fill-g" x="24" y="87" width="348" height="8" rx="4"/>

  <text x="24" y="114" class="k">02 · Computer Vision (CNNs, OpenCV)</text>
  <text x="368" y="114" class="ok">92%</text>
  <rect class="track" x="24" y="121" width="370" height="8" rx="4"/>
  <rect class="fill-b" x="24" y="121" width="340" height="8" rx="4"/>

  <text x="24" y="148" class="k">03 · NLP &amp; Topic Modeling (BERTopic/LLM)</text>
  <text x="368" y="148" class="ok">90%</text>
  <rect class="track" x="24" y="155" width="370" height="8" rx="4"/>
  <rect class="fill-p" x="24" y="155" width="333" height="8" rx="4"/>

  <text x="24" y="182" class="k">04 · Backend &amp; Cloud MLOps (FastAPI/Web)</text>
  <text x="368" y="182" class="ok">88%</text>
  <rect class="track" x="24" y="189" width="370" height="8" rx="4"/>
  <rect class="fill-y" x="24" y="189" width="325" height="8" rx="4"/>

  <line x1="425" y1="42" x2="425" y2="212" stroke="#30363d" stroke-width="1"/>

  <!-- Right Column: Verified Credentials & Awards -->
  <text x="448" y="54" class="sec">◈ VERIFIED CERTIFICATIONS &amp; HONORS</text>

  <text x="448" y="82"><tspan class="ok">[✓]</tspan> <tspan font-weight="600">Oracle Cloud Infrastructure 2025 AI Foundations</tspan></text>
  <text x="476" y="98" class="muted">Certified Associate  •  Score: 95%  •  Oracle</text>

  <text x="448" y="124"><tspan class="ok">[✓]</tspan> <tspan font-weight="600">Machine Learning Intern — Best Performance Award</tspan></text>
  <text x="476" y="140" class="muted">EduExpose  •  Production ML Pipeline Delivery</text>

  <text x="448" y="166"><tspan class="ok">[✓]</tspan> <tspan font-weight="600">Interpersonal Communication for Eng. Leaders</tspan></text>
  <text x="476" y="182" class="muted">Rice University (Coursera)  •  Engineering Leadership</text>

  <text x="448" y="206"><tspan class="ok">[✓]</tspan> <tspan font-weight="600">Computational Theory &amp; Computer Communications</tspan></text>
  <text x="476" y="220" class="muted">Infosys Springboard &amp; Univ. of Colorado (4-Course Spec.)</text>
</svg>'''

    with open("system-telemetry.svg", "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    build_heatmap()
    build_info_card()
    build_ascii_portrait()
    build_telemetry()
