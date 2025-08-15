// @ts-check
import { defineConfig } from 'astro/config';

import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
    site: 'https://www.vxit.io',
    i18n: {
        locales: ["en", "it", "es", "et", "fr", "de"],
        defaultLocale: "en",
        routing: {
            prefixDefaultLocale: true
        }
    },

    integrations: [sitemap()]
});