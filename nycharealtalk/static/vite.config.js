import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig(({ mode }) => {
    const isDev = mode === 'development'

    return {
        build: {
            outDir: './js/dist',
            emptyOutDir: false,
            minify: isDev ? false : 'esbuild',
            sourcemap: isDev ? 'inline' : false,
            commonjsOptions: {
                include: /.*/,
                transformMixedEsModules: true,
            },
            rollupOptions: {
                input: 'js/main.js',
                external: ['jquery'],
                output: {
                    entryFileNames: isDev ? 'bundle.dev.js' : 'bundle.min.js',
                    format: 'iife',
                    name: 'app',
                    strict: false,
                    globals: {
                        jquery: 'jQuery',
                    },
                },
            },
        },
        resolve: {
            alias: {
                bootstrap_button:     path.resolve('node_modules/bootstrap/js/button.js'),
                bootstrap_collapse:   path.resolve('node_modules/bootstrap/js/collapse.js'),
                bootstrap_dropdown:   path.resolve('node_modules/bootstrap/js/dropdown.js'),
                bootstrap_modal:      path.resolve('node_modules/bootstrap/js/modal.js'),
                bootstrap_tooltip:    path.resolve('node_modules/bootstrap/js/tooltip.js'),
                bootstrap_transition: path.resolve('node_modules/bootstrap/js/transition.js'),
                'leaflet-plugins-bing': path.resolve('node_modules/leaflet-plugins/layer/tile/Bing.js'),
            },
        },
    }
})
