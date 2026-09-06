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

    // One owner for adopting a server-provided Canvas revision after a versioned
    // write: a positive server revision wins, the current revision is kept when
    // the write returned none, and missingFallback covers a revision-less canvas.
    function adoptRevision(canvas, revision, missingFallback) {
        const value = Number(revision) || 0;
        const current = Number(canvas && canvas.updated_at) || 0;
        const adopted = value > 0 ? value : (current > 0 ? current : Number(missingFallback) || 0);
        if (canvas) canvas.updated_at = adopted;
        return adopted;
    }

    global.WorkbenchCanvasPersistence = Object.freeze({
        load: canvasId => requestPath(canvasPath(canvasId), {method: 'GET'}),
        metadata: canvasId => requestPath(`${canvasPath(canvasId)}/meta`, {method: 'GET'}),
        save: (canvasId, record) => requestPath(canvasPath(canvasId), {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(record),
        }),
        adoptRevision,
    });
}(window));
