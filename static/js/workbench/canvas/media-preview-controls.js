/* Shared native-video event isolation for temporary Canvas media adapters. */
(function exposeCanvasMediaPreviewControls(global) {
    'use strict';

    const PLAYER_EVENTS = ['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'click', 'dblclick', 'contextmenu', 'wheel'];

    function bindVideoOverlay(video, options = {}) {
        if (!video) return false;
        const boundKey = options.boundKey || 'workbenchCanvasVideoOverlayBound';
        if (video.dataset?.[boundKey] === '1') return false;
        if (video.dataset) video.dataset[boundKey] = '1';
        const overlaySelector = options.overlaySelector || '';
        const sync = () => {
            const overlay = overlaySelector ? video.parentElement?.querySelector?.(overlaySelector) : null;
            if (overlay) overlay.style.display = !video.paused && !video.ended ? 'none' : '';
        };
        ['play', 'playing', 'pause', 'ended'].forEach(type => video.addEventListener(type, sync));
        PLAYER_EVENTS.forEach(type => video.addEventListener(type, event => event.stopPropagation()));
        sync();
        return true;
    }

    function bindPreviewImageFallbacks(root, options = {}) {
        const scope = root || global.document;
        if (!scope?.querySelectorAll) return;
        const bindVideo = typeof options.bindVideoOverlay === 'function' ? options.bindVideoOverlay : () => {};
        const originalUrl = typeof options.originalUrl === 'function'
            ? options.originalUrl
            : image => image?.dataset?.originalSrc || image?.dataset?.url || '';
        const videoFallbackHtml = typeof options.videoFallbackHtml === 'function' ? options.videoFallbackHtml : null;
        scope.querySelectorAll('img[data-preview-src][data-original-src]:not([data-preview-fallback-bound])').forEach(image => {
            image.dataset.previewFallbackBound = '1';
            image.addEventListener('error', () => {
                const original = originalUrl(image);
                if (image.dataset.previewKind === 'video' && videoFallbackHtml) {
                    const documentRef = image.ownerDocument || global.document;
                    const template = documentRef?.createElement?.('template');
                    if (!template) return;
                    template.innerHTML = videoFallbackHtml(original, image.dataset.videoFallbackAttrs || '');
                    const video = template.content?.firstElementChild;
                    if (!video) return;
                    image.replaceWith(video);
                    bindVideo(video);
                    return;
                }
                if (original && image.getAttribute('src') !== original) image.src = original;
            });
        });
        const inlineVideoSelector = options.inlineVideoSelector || 'video[data-inline-video-active]';
        scope.querySelectorAll(inlineVideoSelector).forEach(bindVideo);
    }

    function preloadImage(src, options = {}) {
        if (!src) return Promise.resolve(false);
        const createImage = typeof options.createImage === 'function'
            ? options.createImage
            : () => new global.Image();
        return new Promise(resolve => {
            const image = createImage();
            image.decoding = 'async';
            image.onload = async () => {
                try { if (image.decode) await image.decode(); } catch (_error) {}
                resolve(true);
            };
            image.onerror = () => resolve(false);
            image.src = src;
        });
    }

    function loadImageDimensions(src, options = {}) {
        if (!src || /^data:/i.test(src) || /^blob:/i.test(src)) return Promise.resolve(null);
        const createImage = typeof options.createImage === 'function' ? options.createImage : () => new global.Image();
        return new Promise(resolve => {
            const image = createImage();
            image.onload = () => resolve(image.naturalWidth && image.naturalHeight ? {w:image.naturalWidth, h:image.naturalHeight} : null);
            image.onerror = () => resolve(null);
            image.src = src;
        });
    }

    function copyPositiveDimensions(source, target = {}, fields = ['natural_w', 'natural_h', 'width', 'height', 'w', 'h', 'layout_w', 'layout_h']) {
        if (!source || typeof source !== 'object') return target;
        fields.forEach(key => { const value = Number(source[key]); if (Number.isFinite(value) && value > 0) target[key] = value; });
        return target;
    }

    function collectHighResCandidates(options = {}) {
        const roots = Array.isArray(options.roots) ? options.roots.filter(Boolean) : [options.root].filter(Boolean);
        const selector = options.selector || 'img[data-preview-src][data-original-src]';
        const wantHighRes = Boolean(options.wantHighRes);
        const isNearViewport = typeof options.isNearViewport === 'function' ? options.isNearViewport : () => true;
        const originalUrl = typeof options.originalUrl === 'function' ? options.originalUrl : image => image?.dataset?.originalSrc || '';
        const resolveTarget = typeof options.resolveTarget === 'function' ? options.resolveTarget : value => value;
        const isLoaded = typeof options.isLoaded === 'function' ? options.isLoaded : () => false;
        const candidates = [];
        roots.forEach(root => root.querySelectorAll?.(selector).forEach(image => {
            if (image.dataset?.previewKind === 'video') return;
            const preview = image.dataset?.previewSrc || '';
            if (!wantHighRes || !isNearViewport(image)) {
                delete image.dataset.selectedHighResTarget;
                if (preview && image.getAttribute('src') !== preview) image.src = preview;
                return;
            }
            const target = resolveTarget(originalUrl(image), image);
            if (!target) return;
            image.dataset.selectedHighResTarget = target;
            if (isLoaded(target)) {
                if (image.getAttribute('src') !== target) image.src = target;
                return;
            }
            if (preview && image.getAttribute('src') !== preview) image.src = preview;
            candidates.push({image, target});
        }));
        return candidates;
    }

    global.WorkbenchCanvasMediaPreviewControls = Object.freeze({
        bindVideoOverlay,
        bindPreviewImageFallbacks,
        preloadImage,
        loadImageDimensions,
        copyPositiveDimensions,
        collectHighResCandidates,
    });
}(window));
