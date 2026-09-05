/* Shared normalization for Canvas update notifications from replaceable transports. */
(function exposeCanvasUpdateMessage(global) {
    'use strict';

    function normalizedTimestamp(value) {
        const number = Number(value);
        return Number.isFinite(number) && number > 0 ? number : 0;
    }

    function newerForCanvas(message, options) {
        const settings = options || {};
        const canvasId = String(settings.canvasId || '');
        if (!canvasId || !message || message.type !== 'canvas_updated') return null;
        if (String(message.canvas_id || '') !== canvasId) return null;
        if (message.client_id && String(message.client_id) === String(settings.clientId || '')) return null;
        const updatedAt = normalizedTimestamp(message.updated_at);
        if (updatedAt && updatedAt <= normalizedTimestamp(settings.currentUpdatedAt)) return null;
        return Object.freeze({canvasId, clientId: String(message.client_id || ''), updatedAt});
    }

    global.WorkbenchCanvasUpdateMessage = Object.freeze({newerForCanvas});
}(window));
