import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		// allow Vite to read the cache/ TSV files imported with the $cache alias
		fs: { allow: ['cache'] }
	}
});
