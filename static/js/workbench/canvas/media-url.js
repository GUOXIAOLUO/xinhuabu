/* Pure media URL normalization and preview routing shared by Canvas adapters. */
(function exposeCanvasMediaUrl(global) {
    'use strict';

    const DEFAULT_MEDIA_EXTENSIONS = /\.(png|jpe?g|webp|gif|bmp|avif|tiff?|mp4|webm|mov|m4v|avi|mkv)(\?|#|$)/i;

    function originalUrl(value, locationOrigin) {
        const raw = typeof value === 'string' ? value : (value?.url || '');
        const text = String(raw || '');
        if (!text) return '';
        try {
            const parsed = new URL(text, locationOrigin || global.location?.origin || 'http://localhost');
            if (parsed.pathname === '/api/media-preview') {
                return parsed.searchParams.get('url') || text;
            }
        } catch (_error) {
            // Keep an unparseable legacy URL unchanged.
        }
        return text;
    }

    function previewUrl(value, options = {}) {
        const raw = originalUrl(value, options.locationOrigin);
        const displayUrl = typeof options.displayUrl === 'function' ? options.displayUrl : () => raw;
        const fallback = displayUrl(raw);
        if (!raw) return fallback || '';
        if (raw.startsWith('data:') || raw.startsWith('blob:')) {
            return options.keepInlineUrl ? raw : fallback;
        }
        if (!raw.startsWith('/output/') && !raw.startsWith('/assets/')) return fallback;
        const extensions = options.extensions instanceof RegExp ? options.extensions : DEFAULT_MEDIA_EXTENSIONS;
        if (!extensions.test(raw)) return options.keepUnsupportedUrl ? raw : fallback;
        const width = Math.max(64, Math.min(2048, Math.round(Number(options.size) || 512)));
        return `/api/media-preview?w=${width}&url=${encodeURIComponent(raw)}`;
    }

    global.WorkbenchCanvasMediaUrl = Object.freeze({
        originalUrl,
        previewUrl,
    });
}(window));
