# Assets — Brand Reference

PhotoDay brand tokens and design reference for developers.

> **Note:** `index.html` is fully self-contained — all brand tokens are inlined directly
> in the `<style>` block. These files are **reference only** for when this tool gets
> folded into the main PhotoDay app or extended into multi-file components.

## Structure

```
assets/
├── brand.css        CSS custom properties — reference source of truth
├── brand-tokens.js  Same tokens as a JS object — for Canvas/React integration
├── fonts.css        Typography scale + Adobe Fonts setup instructions
└── logos/
    ├── README.md    Logo usage rules + download links
    └── *.png/svg    (place downloaded logo files here)
```

## Using in a React/Next.js context

```js
// Import tokens into a component or global stylesheet
import '../assets/brand-tokens.js'; // exposes window.PD
// or in CSS:
// @import './assets/brand.css';
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
