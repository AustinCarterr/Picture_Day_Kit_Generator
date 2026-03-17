/**
 * PhotoDay Brand Tokens — JavaScript
 * Source: https://www.photoday.com/brand-guidelines
 * Last synced: 2026-03-17
 *
 * Usage (ES module):
 *   import { PD } from './assets/brand-tokens.js';
 *   ctx.fillStyle = PD.colors.green;
 *
 * Usage (inline script / canvas):
 *   <script src="assets/brand-tokens.js"></script>
 *   ctx.fillStyle = PD.colors.green;
 */

const PD = {

  // ── Colors ────────────────────────────────────────────────────────────────
  colors: {
    // Brand
    green:        '#48af94',   // Primary CTA
    greenMedium:  '#2b6959',   // Hover / dark green
    purple:       '#612ad7',   // Accent purple
    pink:         '#ea4970',   // Accent pink
    gold:         '#f4a42f',   // AdvancePay / warning
    violetLight:  '#b4a0de',   // Subtle purple tint
    violetDark:   '#0e071c',   // Deep background purple

    // Neutrals
    white:        '#ffffff',
    black:        '#000000',
    grayLight:    '#d3d3d5',
    gray:         '#6b6b73',
    grayMedium:   '#404045',
    grayDark:     '#202023',

    // Backgrounds
    bgDark:       '#0b0b1f',   // Dark hero / nav background
    bgLight:      '#f4f4f6',   // Light page background
  },

  // ── Typography ─────────────────────────────────────────────────────────────
  fonts: {
    display:  "'neue-haas-grotesk-display', 'Helvetica Neue', Arial, sans-serif",
    text:     "'neue-haas-grotesk-text', 'Helvetica Neue', Arial, sans-serif",
    serif:    "'p22-mackinac-pro', Georgia, serif",
    fallback: "'Helvetica Neue', Arial, sans-serif",
    // For Canvas (no CSS font-family shorthand needed)
    canvas: {
      heading:  'neue-haas-grotesk-display, Arial Black, Arial',
      body:     'neue-haas-grotesk-text, Arial, sans-serif',
      serif:    'p22-mackinac-pro, Georgia, serif',
    }
  },

  // ── Radii ──────────────────────────────────────────────────────────────────
  radius: {
    btn:  12,
    sm:   8,
    md:   16,
    lg:   24,
    pill: 999,
  },

  // ── Shadows ────────────────────────────────────────────────────────────────
  shadows: {
    sm:     '0 1px 3px rgba(0,0,0,0.12)',
    md:     '0 4px 16px rgba(0,0,0,0.16)',
    lg:     '0 8px 32px rgba(0,0,0,0.22)',
    purple: '0 4px 24px rgba(97,42,215,0.28)',
  },

  // ── Gradients (CSS strings) ────────────────────────────────────────────────
  gradients: {
    hero:   'linear-gradient(135deg, #0b0b1f 0%, #1a0e3a 100%)',
    green:  'linear-gradient(135deg, #48af94 0%, #2b6959 100%)',
    purple: 'linear-gradient(135deg, #612ad7 0%, #0e071c 100%)',
    gold:   'linear-gradient(135deg, #f4a42f 0%, #e08010 100%)',
  },

  // ── Logos ──────────────────────────────────────────────────────────────────
  logos: {
    // Official logo kit (EPS + PNG):
    kitZip: 'https://media.photoday.io/resources/photoday_logo_kit.zip',
    // CDN assets from brand guidelines page:
    colored:           'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/621be619cd109b80f786fe2c_guideline_colored_logo.jpeg',
    white:             'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/621be618e1c95a5574672bab_guideline_white_logo.jpeg',
    poweredByHoriz:    'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/621be6184c58051947af2b2e_guideline_powered_by_horiz.jpeg',
    poweredByVert:     'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/621be618249f2277b039e229_guideline_powered_by_vert.jpeg',
    poweredByVertLeft: 'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/621be6196349cd0a37a42996_guideline_powered_by_vertleft.jpeg',
    // Nav SVG (white version):
    navSvg: 'https://cdn.prod.website-files.com/611970eeff02f896bda0d4f4/6119cbb00651c6269a691adc_nav-logo-wht.svg',
  },

  // ── Spacing scale (px) ─────────────────────────────────────────────────────
  space: {
    xs:  4,
    sm:  8,
    md:  16,
    lg:  24,
    xl:  40,
    xxl: 64,
  },

  // ── Helper: rgba from hex ───────────────────────────────────────────────────
  rgba(hex, alpha = 1) {
    const r = parseInt(hex.slice(1,3), 16);
    const g = parseInt(hex.slice(3,5), 16);
    const b = parseInt(hex.slice(5,7), 16);
    return `rgba(${r},${g},${b},${alpha})`;
  },

};

// Export for both module and script tag usage
if (typeof module !== 'undefined') module.exports = { PD };
