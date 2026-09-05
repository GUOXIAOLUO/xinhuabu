/* Media-reference filtering shared by temporary Canvas adapters. */
(function exposeCanvasMediaReferences(global) {
    'use strict';

    function refsOfKind(refs, expectedKind, options = {}) {
        const kindOf = typeof options.kindOf === 'function' ? options.kindOf : () => '';
        const accept = typeof options.accept === 'function' ? options.accept : () => true;
        const values = (refs || []).filter(ref => ref?.url && kindOf(ref) === expectedKind && accept(ref));
        const limit = Number(options.limit);
        return Number.isFinite(limit) && limit >= 0 ? values.slice(0, limit) : values;
    }

    function isRemoteVideoReferenceUrl(url) {
        return /^https?:\/\//i.test(String(url || '')) || /^asset:\/\//i.test(String(url || ''));
    }

    function looksLikeImageUrl(url) {
        const text = String(url || '').trim().toLowerCase();
        if (!text) return false;
        if (text.startsWith('data:image/')) return true;
        if (text.startsWith('asset://')) return false;
        const path = text.split('?', 1)[0].split('#', 1)[0];
        return /\.(png|jpe?g|webp|gif|bmp|tiff)$/i.test(path);
    }

    global.WorkbenchCanvasMediaReferences = Object.freeze({refsOfKind, isRemoteVideoReferenceUrl, looksLikeImageUrl});
}(window));
