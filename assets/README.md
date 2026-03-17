# Assets

PhotoDay brand assets shared across all environments (dev / test / main).

## Structure

```
assets/
├── brand.css        CSS custom properties — import this in every HTML page
├── brand-tokens.js  Same tokens as a JS object — import for Canvas rendering
├── fonts.css        Typography scale + Adobe Fonts setup instructions
└── logos/
    ├── README.md    Logo usage rules + download links
    └── *.png/svg    (place downloaded logo files here)
```

## Quick Start

```html
<head>
  <!-- 1. Adobe Fonts (swap [KIT_ID] for real Typekit kit ID) -->
  <!-- <link rel="stylesheet" href="https://use.typekit.net/[KIT_ID].css"> -->

  <!-- 2. Brand tokens + typography -->
  <link rel="stylesheet" href="assets/brand.css">
  <link rel="stylesheet" href="assets/fonts.css">
</head>
```

## Color Reference

| Token | Hex | Role |
|-------|-----|------|
| `--pd-green` | `#48af94` | Primary CTA, brand green |
| `--pd-green-medium` | `#2b6959` | Hover, dark green |
| `--pd-purple` | `#612ad7` | Accent, highlights |
| `--pd-pink` | `#ea4970` | Alerts, special callouts |
| `--pd-gold` | `#f4a42f` | AdvancePay, warnings |
| `--pd-violet-dark` | `#0e071c` | Deep background |
| `--pd-bg-dark` | `#0b0b1f` | Nav / hero background |
| `--pd-gray-dark` | `#202023` | Dark UI cards |
| `--pd-gray` | `#6b6b73` | Secondary text |
| `--pd-gray-light` | `#d3d3d5` | Borders, disabled |

## Font Reference

| Token | Value | Use |
|-------|-------|-----|
| `--pd-font-display` | `neue-haas-grotesk-display` | Headings, hero |
| `--pd-font-text` | `neue-haas-grotesk-text` | Body, UI labels |
| `--pd-font-serif` | `p22-mackinac-pro` | Editorial accents |
