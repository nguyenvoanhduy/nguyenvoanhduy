"""Build original SVG artwork and export a seamless GIF for a GitHub profile.

Optional GIF export requires: pip install playwright pillow
Then install Chromium with: python -m playwright install chromium
"""
from pathlib import Path
import io
import math
import random
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
rng = random.Random(26092026)

stars = []
for i in range(165):
    x, y = rng.uniform(14, 946), rng.uniform(12, 388)
    radius = rng.choice([0.55, 0.7, 0.9, 1.25])
    opacity = rng.uniform(.2, .78)
    color = rng.choice(['#c8d6ff', '#8daeff', '#b4fff3', '#ffffff'])
    stars.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" opacity="{opacity:.2f}"/>')
for i in range(38):
    angle = rng.uniform(0, math.tau)
    dx, dy = math.cos(angle), math.sin(angle) * .65
    start, end = rng.uniform(35, 90), rng.uniform(180, 400)
    x1, y1 = 748 + dx * start, 178 + dy * start
    x2, y2 = 748 + dx * end, 178 + dy * end
    length = rng.uniform(3, 12)
    begin = -rng.uniform(0, 6)
    stars.append(f'''<g opacity="0">
      <line x1="0" y1="0" x2="{-dx*length:.2f}" y2="{-dy*length:.2f}" stroke="#b7d9ff" stroke-width="1" stroke-linecap="round"/>
      <animateTransform attributeName="transform" type="translate" values="{x1:.2f} {y1:.2f};{x2:.2f} {y2:.2f}" dur="6s" begin="{begin:.3f}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.75;0.65;0" keyTimes="0;0.25;0.8;1" dur="6s" begin="{begin:.3f}s" repeatCount="indefinite"/>
    </g>''')

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="400" viewBox="0 0 960 400" role="img" aria-labelledby="title desc">
  <title id="title">Anh Duy — Galaxy Explorer</title>
  <desc id="desc">A deep violet galaxy with drifting stars, an orbiting planet and a small spacecraft. Anh Duy, building ideas and exploring new worlds.</desc>
  <defs>
    <linearGradient id="space" x2="1" y2="1"><stop stop-color="#060a1c"/><stop offset=".52" stop-color="#111132"/><stop offset="1" stop-color="#090b22"/></linearGradient>
    <radialGradient id="violet"><stop stop-color="#7443d0" stop-opacity=".6"/><stop offset=".48" stop-color="#6438ae" stop-opacity=".25"/><stop offset="1" stop-color="#54249b" stop-opacity="0"/></radialGradient>
    <radialGradient id="blue"><stop stop-color="#278cc6" stop-opacity=".38"/><stop offset="1" stop-color="#278cc6" stop-opacity="0"/></radialGradient>
    <radialGradient id="planet" cx=".24" cy=".2" r=".9"><stop stop-color="#a9e8ff"/><stop offset=".3" stop-color="#458ba9"/><stop offset=".56" stop-color="#2e436d"/><stop offset=".8" stop-color="#10162d"/><stop offset="1" stop-color="#080c1d"/></radialGradient>
    <linearGradient id="ring"><stop stop-color="#7ecbfc" stop-opacity=".15"/><stop offset=".44" stop-color="#b9c2ff" stop-opacity=".85"/><stop offset="1" stop-color="#7b65bc" stop-opacity=".35"/></linearGradient>
    <linearGradient id="exhaust" x1="1" x2="0"><stop stop-color="#cefaff"/><stop offset=".25" stop-color="#50c9e9" stop-opacity=".8"/><stop offset="1" stop-color="#9571ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="rule"><stop stop-color="#7e81b7" stop-opacity=".7"/><stop offset="1" stop-color="#7e81b7" stop-opacity="0"/></linearGradient>
    <clipPath id="bounds"><rect width="960" height="400" rx="20"/></clipPath>
    <clipPath id="world"><circle cx="749" cy="169" r="60"/></clipPath>
  </defs>
  <g clip-path="url(#bounds)">
    <rect width="960" height="400" fill="url(#space)"/>
    <ellipse cx="722" cy="145" rx="385" ry="215" fill="url(#violet)" transform="rotate(-25 722 145)"/>
    <ellipse cx="595" cy="330" rx="400" ry="210" fill="url(#blue)" transform="rotate(-23 595 330)"/>
    <ellipse cx="976" cy="260" rx="270" ry="190" fill="url(#violet)"/>
    STARS
    <path d="M548 283 Q646 195 928 100" fill="none" stroke="#afbcf0" stroke-opacity=".09" stroke-width="1"/>
    <path d="M566 71 Q713 212 922 286" fill="none" stroke="#afbcf0" stroke-opacity=".09" stroke-dasharray="2 9"/>
    <ellipse cx="749" cy="169" rx="120" ry="31" fill="none" stroke="url(#ring)" stroke-width="9" transform="rotate(-25 749 169)" opacity=".55"/>
    <circle cx="749" cy="169" r="67" fill="#6cc7ff" opacity=".045"/>
    <circle cx="749" cy="169" r="62" fill="#8de4ff" opacity=".13"/>
    <circle cx="749" cy="169" r="60" fill="url(#planet)"/>
    <g clip-path="url(#world)" fill="none" stroke="#badfff" opacity=".12">
      <path d="M675 138 Q733 99 821 157" stroke-width="9"/>
      <path d="M677 162 Q732 124 827 185" stroke-width="5"/>
      <path d="M686 183 Q751 158 821 205" stroke-width="11"/>
    </g>
    <path d="M640 222 C678 229 819 184 858 118" fill="none" stroke="url(#ring)" stroke-width="7" stroke-linecap="round"/>
    <path d="M637 225 C679 235 823 185 861 115" fill="none" stroke="#d7d0ff" stroke-opacity=".26" stroke-width="1"/>
    <g transform="translate(691 277) rotate(-22)">
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;7 -4;0 0" dur="6s" repeatCount="indefinite"/>
        <path d="M-82 0 L-19 -6 L-10 0 L-19 6 Z" fill="url(#exhaust)">
          <animate attributeName="opacity" values=".6;1;.6" dur="2s" repeatCount="indefinite"/>
        </path>
        <path d="M-25 -7 L-33 -21 L3 -9 L28 0 L3 9 L-33 21 L-25 7 L-31 0 Z" fill="#aab8cf"/>
        <path d="M-18 -5 L-3 -6 L27 0 L-3 6 L-18 5 Z" fill="#e4edfa"/>
        <path d="M-4 -4 L10 -1 L13 0 L-4 2 Z" fill="#37bfe2"/>
        <path d="M-31 -19 L-14 -8 M-31 19 L-14 8" stroke="#5b708f" stroke-width="2"/>
      </g>
    </g>
    <g font-family="Segoe UI, Arial, sans-serif">
      <circle cx="55" cy="56" r="3" fill="#93e4ed"/>
      <text x="68" y="60" fill="#b9c5e9" font-size="10" letter-spacing="3">PERSONAL FLIGHT LOG / 001</text>
      <text x="52" y="154" fill="#f0f3ff" font-size="76" font-weight="700" letter-spacing="-3">ANH DUY<tspan fill="#93dce8">.</tspan></text>
      <text x="56" y="190" fill="#bfc2e6" font-size="12" letter-spacing="5">BUILD. EXPLORE. REPEAT.</text>
      <path d="M56 218 H376" stroke="url(#rule)"/>
      <text x="56" y="248" fill="#c4c9df" font-size="16">Biến ý tưởng thành sản phẩm.</text>
      <text x="56" y="274" fill="#8d99bd" font-size="14">Một hành trình khám phá, từng dòng code.</text>
      <rect x="56" y="297" width="160" height="28" rx="14" fill="#182139" stroke="#39556a" stroke-opacity=".7"/>
      <circle cx="72" cy="311" r="3" fill="#8edee0"/>
      <text x="84" y="315" fill="#bee2eb" font-size="10" letter-spacing="1.5">GALAXY EXPLORER</text>
      <path d="M56 352 H904" stroke="#454668" stroke-opacity=".45"/>
      <text x="56" y="376" fill="#8693b5" font-size="9" letter-spacing="2">@NGUYENVOANHDUY</text>
      <text x="626" y="376" fill="#8693b5" font-size="9" letter-spacing="2">DESTINATION / THE NEXT IDEA</text>
      <text x="839" y="58" fill="#8693b5" font-size="9" letter-spacing="2">SECTOR 01</text>
      <circle cx="906" cy="54" r="2" fill="#83e1df"/>
    </g>
    <rect x=".5" y=".5" width="959" height="399" rx="20" fill="none" stroke="#6478ad" stroke-opacity=".25"/>
  </g>
</svg>'''.replace('STARS', '\n'.join(stars))
(ASSETS / 'galaxy-banner.svg').write_text(svg, encoding='utf-8')

with sync_playwright() as p:
    browsers = [Path('C:/Program Files/Google/Chrome/Application/chrome.exe'), Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')]
    installed = next((str(path) for path in browsers if path.exists()), None)
    browser = p.chromium.launch(executable_path=installed, headless=True)
    page = browser.new_page(viewport={'width': 960, 'height': 400}, device_scale_factor=1)
    page.goto((ASSETS / 'galaxy-banner.svg').as_uri())
    page.evaluate('document.documentElement.pauseAnimations()')
    frames = []
    for i in range(75):
        page.evaluate('(t) => document.documentElement.setCurrentTime(t)', i * .08)
        frame = Image.open(io.BytesIO(page.screenshot(omit_background=True))).convert('RGBA')
        frames.append(frame)
    frames[18].save(ASSETS / 'galaxy-preview.png')
    palette = frames[18].convert('RGB').quantize(colors=255)
    indexed = []
    for frame in frames:
        color = frame.convert('RGB').quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG)
        transparent = frame.getchannel('A').point(lambda alpha: 255 if alpha < 128 else 0)
        color.paste(255, mask=transparent)
        indexed.append(color)
    indexed[0].save(ASSETS / 'galaxy-banner.gif', save_all=True, append_images=indexed[1:], duration=80, loop=0, optimize=False, disposal=1, transparency=255)
    browser.close()
print(f'Banner exported: {(ASSETS / "galaxy-banner.gif").stat().st_size / 1024:.0f} KiB, 75 frames, 6-second loop')
