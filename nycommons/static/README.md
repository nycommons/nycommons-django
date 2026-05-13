# Frontend — nycha-realtalk

JavaScript and CSS assets for the site. Built with [Vite](https://vitejs.dev/) (JS) and [Less](https://lesscss.org/) (CSS).

## Setup

```bash
npm install
```

## Development

Run both watchers in separate terminals:

```bash
npm run dev       # JS: rebuilds js/dist/bundle.dev.js on change
npm run css:watch # CSS: rebuilds css/dist/style.dev.css on change
```

Or compile CSS once without watching:

```bash
npm run css:dev
```

Django's dev server serves the compiled files as static assets — there is no Vite dev server to run.

## Production build

```bash
npm run build
```

Outputs `js/dist/bundle.min.js` and `css/dist/style.min.css`. The Django template at `templates/_includes.html` switches between dev and production files based on the `debug` context variable.

## How it works

| Tool | Role |
|------|------|
| Vite + Rollup | Bundles `js/main.js` and all its `require()` dependencies into a single IIFE |
| Less CLI | Compiles `css/style.less` (including Bootstrap 3 and Leaflet CSS from node_modules) |
| `less-plugin-lists` | Provides `.for-each` / `at()` used in `css/filters.less`; requires Less 2.x |

jQuery is loaded from CDN in the Django template and treated as an external global — it is not bundled.

## Output files

| File | When used |
|------|-----------|
| `js/dist/bundle.dev.js` | `DEBUG=True` (includes inline sourcemaps, unminified) |
| `js/dist/bundle.min.js` | `DEBUG=False` (minified) |
| `css/dist/style.dev.css` | `DEBUG=True` (includes sourcemap) |
| `css/dist/style.min.css` | `DEBUG=False` |

## Adding a new JS module

Source files use CommonJS (`require()`/`module.exports`). New files can use either CommonJS or ES module syntax (`import`/`export`) — Vite handles both.

Bootstrap components are aliased in `vite.config.js` (e.g. `require('bootstrap_modal')` resolves to the individual Bootstrap 3 file). Add new aliases there if needed.
