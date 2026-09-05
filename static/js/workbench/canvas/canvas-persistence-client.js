/* Shared Canvas-record persistence boundary for temporary editor adapters. */
(function exposeCanvasPersistenceClient(global) {
    'use strict';

    function canvasPath(canvasId) {
        if (!canvasId) throw new Error('A Canvas id is required.');
        return `/api/canvases/${encodeURIComponent(canvasId)}`;
    }

    async function requestPath(path, options) {
        const response = await fetch(path, options);
        const payload = await response.json().catch(() => ({}));
        const detail = payload && payload.detail && typeof payload.detail === 'object' ? payload.detail : {};
        return {
            ok: response.ok,
            status: response.status,
            canvas: detail.canvas || payload.canvas || null,
            updatedAt: Number(detail.updated_at || payload.updated_at || detail.canvas?.updated_at || payload.canvas?.updated_at || 0),
            payload,
        };
    }

    global.WorkbenchCanvasPersistence = Object.freeze({
        load: canvasId => requestPath(canvasPath(canvasId), {method: 'GET'}),
        metadata: canvasId => requestPath(`${canvasPath(canvasId)}/meta`, {method: 'GET'}),
        save: (canvasId, record) => requestPath(canvasPath(canvasId), {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(record),
        }),
    });
}(window));
