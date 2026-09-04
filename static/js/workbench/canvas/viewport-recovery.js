/* Shared pure viewport fitting/recovery math. Adapters provide node bounds and
   decide when a saved viewport is considered invalid. */
(function exposeWorkbenchCanvasViewportRecovery(global) {
    'use strict';

    function finite(value, fallback) { const number = Number(value); return Number.isFinite(number) ? number : fallback; }
    function bounds(rectangles) {
        const items = Array.from(rectangles || []).map(rect => ({
            x:finite(rect?.x, 0), y:finite(rect?.y, 0),
            width:Math.max(1, finite(rect?.width, finite(rect?.w, 1))),
            height:Math.max(1, finite(rect?.height, finite(rect?.h, 1))),
        }));
        if(!items.length) return null;
        const minX = Math.min(...items.map(item => item.x));
        const minY = Math.min(...items.map(item => item.y));
        const maxX = Math.max(...items.map(item => item.x + item.width));
        const maxY = Math.max(...items.map(item => item.y + item.height));
        return Object.freeze({x:minX, y:minY, width:maxX - minX, height:maxY - minY});
    }

    function fit(rectangles, viewportSize, options) {
        const opts = options || {};
        const viewport = viewportSize || {};
        const width = Math.max(1, finite(viewport.width, 1));
        const height = Math.max(1, finite(viewport.height, 1));
        const emptyScale = finite(opts.emptyScale, .45);
        const content = bounds(rectangles);
        if(!content) return Object.freeze({scale:emptyScale, x:width / 2, y:height / 2});
        const pad = Math.max(0, finite(opts.padding, 160));
        const inset = Math.max(0, finite(opts.inset, 80));
        const minScale = Math.max(.001, finite(opts.minScale, .06));
        const maxScale = Math.max(minScale, finite(opts.maxScale, .82));
        const scale = Math.max(minScale, Math.min(maxScale, (width - inset) / Math.max(1, content.width + pad * 2), (height - inset) / Math.max(1, content.height + pad * 2)));
        return Object.freeze({
            scale,
            x:width / 2 - (content.x + content.width / 2) * scale,
            y:height / 2 - (content.y + content.height / 2) * scale,
        });
    }

    global.WorkbenchCanvasViewportRecovery = Object.freeze({bounds, fit});
}(window));
