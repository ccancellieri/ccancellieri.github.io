# Carlo Cancellieri — Portfolio Website

A professional, production-ready single-page portfolio website built for GitHub Pages. Clean, modern design focused on showcasing cloud-native geospatial platforms and open-source contributions.

## Live Demo

**URL:** `https://ccancellieri.github.io`

## Overview

This portfolio highlights Carlo Cancellieri's 20+ years of experience architecting cloud-native geospatial platforms for the United Nations FAO, serving 50+ countries. The site showcases:

- **DynaStore** — Geospatial data platform with 30,000+ records
- **Keystone** — Unified IAM for 25,000+ users
- **Hyrax SQL Handler** — OPeNDAP database access module (Google Summer of Code 2009–2010)
- **GeoServer Ecosystem** — Core contributions to GeoServer, GeoNetwork, GeoTools
- **CKAN Extensions** — Open data platform tooling
- **GeoID Service** — Geospatial identifier service
- **Open Source Contributions** — 1,000+ GitHub contributions per year

## Features

✨ **Modern Design**
- Dark mode with cyan/teal accent colors
- Responsive design (mobile-friendly)
- Smooth animations and transitions
- Clean, developer-focused aesthetic

🎯 **Single-Page Application**
- Self-contained HTML file (no build process needed)
- No external dependencies (fonts/icons via CDN only)
- Fast loading, great performance

📱 **Responsive Layout**
- Works seamlessly on desktop, tablet, and mobile
- Fluid typography and spacing
- Touch-friendly navigation

🔍 **SEO & Accessibility**
- Proper semantic HTML
- Meta tags for Open Graph and Twitter Cards
- Accessible focus states and navigation

🎨 **Interactive Components**
- Expandable project cards with detailed descriptions
- Smooth scroll navigation with active link highlighting
- Intersection Observer animations on scroll
- Hover effects and micro-interactions

## Sections

1. **Hero** — Name, tagline, and call-to-action
2. **About** — Professional background, tech stack, key stats
3. **Featured Projects** — 6 major projects with expandable details
4. **Open Source** — Contributions, organization memberships
5. **Experience** — Timeline of roles and responsibilities
6. **Education** — Degrees and qualifications
7. **Contact** — Multiple ways to get in touch
8. **Footer** — Links and copyright

## File Structure

```
portfolio/
├── index.html          # Single-file application
├── README.md           # This file
└── .gitignore          # Git ignore patterns (optional)
```

## Deployment to GitHub Pages

### Option 1: Deploy to `username.github.io` Repository

1. **Create a new GitHub repository** named `ccancellieri.github.io` (replace with your username)

2. **Clone the repository:**
   ```bash
   git clone https://github.com/ccancellieri/ccancellieri.github.io.git
   cd ccancellieri.github.io
   ```

3. **Copy portfolio files:**
   ```bash
   cp path/to/portfolio/index.html .
   cp path/to/portfolio/README.md .
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Initial portfolio site"
   git push origin main
   ```

5. **View your site:**
   - Visit `https://ccancellieri.github.io` in your browser

### Option 2: Deploy to a Project Repository (`gh-pages` Branch)

1. **Create or use existing repository:**
   ```bash
   git clone https://github.com/ccancellieri/portfolio.git
   cd portfolio
   ```

2. **Copy portfolio files to repo root:**
   ```bash
   cp path/to/portfolio/index.html .
   ```

3. **Create and switch to `gh-pages` branch:**
   ```bash
   git checkout --orphan gh-pages
   git add .
   git commit -m "Deploy portfolio"
   git push origin gh-pages
   ```

4. **Configure GitHub Pages:**
   - Go to repository **Settings** → **Pages**
   - Set **Source** to `gh-pages` branch
   - Save

5. **View your site:**
   - Visit `https://ccancellieri.github.io/portfolio` (or your custom domain)

## Customization

### Update Personal Information

Edit these sections in `index.html`:

- **Hero section:** Change name, tagline, description
- **Social links:** Update GitHub, LinkedIn, email URLs
- **Contact section:** Update email addresses
- **Projects:** Modify project titles, descriptions, links
- **Experience:** Update timeline entries
- **Education:** Change degrees and schools

### Customize Colors

Modify CSS variables in the `<style>` tag:

```css
:root {
    --primary: #0f172a;           /* Dark background */
    --secondary: #1e293b;          /* Card backgrounds */
    --accent: #06b6d4;             /* Cyan/teal accent */
    --accent-dark: #0891b2;        /* Darker accent */
    --text-primary: #f1f5f9;       /* Main text */
    --text-secondary: #cbd5e1;     /* Secondary text */
}
```

### Modify Fonts

Change the Google Fonts import in the `<head>` section. Current fonts:
- **Inter** — Primary body font (3–700 weights)
- **Fira Code** — Optional monospace for code blocks

### Add Your Own Logo/Avatar

Add an image section to the hero:

```html
<img src="avatar.jpg" alt="Carlo Cancellieri" style="width: 120px; height: 120px; border-radius: 50%; margin-bottom: 2rem;">
```

## Optimization Tips

### Image Optimization
If you add images, optimize them:
```bash
# Using ImageMagick
convert input.jpg -resize 800x600 -quality 85 output.jpg
```

### Performance
- The current single-file approach is optimal for GitHub Pages
- All CSS is inlined (no external stylesheets)
- Minimal JavaScript for smooth interactions
- Lighthouse scores typically 95+

### SEO
The site includes:
- Descriptive `<title>` tags
- Meta descriptions
- Open Graph tags for social sharing
- Semantic HTML structure
- Proper heading hierarchy

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

- Semantic HTML (`<section>`, `<nav>`, `<header>`, `<footer>`)
- Proper heading hierarchy (h1–h6)
- Focus states for keyboard navigation
- High contrast colors (WCAG AA compliant)
- Alt text on icons via Font Awesome
- Proper link semantics with title attributes

## Version History

- **v1.0** (2026-03) — Initial release with 6 featured projects, open-source section, timeline, education, and contact

## License

This portfolio is provided as-is for personal use. Feel free to customize and deploy.

## Support

For issues, questions, or suggestions:
- Email: [removed]
- GitHub: https://github.com/ccancellieri
- LinkedIn: https://linkedin.com/in/ccancellieri

---

**Built with ❤️ by Carlo Cancellieri**
