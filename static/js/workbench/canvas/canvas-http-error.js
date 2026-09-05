/* Shared HTTP error formatting for temporary Canvas editor adapters. */
(function exposeCanvasHttpError(global) {
    'use strict';

    function message(data, fallback = '请求失败') {
        if (!data) return fallback;
        if (typeof data === 'string') return data || fallback;
        const detail = data.detail ?? data.error ?? data.message;
        if (typeof detail === 'string') return detail || fallback;
        if (Array.isArray(detail)) {
            const messages = detail.map(item => {
                if (typeof item === 'string') return item;
                const location = Array.isArray(item?.loc) ? item.loc.filter(value => value !== 'body').join('.') : '';
                const itemMessage = item?.msg || item?.message || JSON.stringify(item);
                return location ? `${location}: ${itemMessage}` : itemMessage;
            }).filter(Boolean);
            return messages.join('\n') || fallback;
        }
        if (detail && typeof detail === 'object') return detail.message || detail.msg || JSON.stringify(detail);
        try {
            return JSON.stringify(data);
        } catch (_) {
            return fallback;
        }
    }

    async function responseMessage(response, fallback = '请求失败') {
        try {
            return message(await response.clone().json(), fallback);
        } catch (_) {
            try {
                return (await response.text()) || fallback;
            } catch (_) {
                return fallback;
            }
        }
    }

    global.WorkbenchCanvasHttpError = Object.freeze({message, responseMessage});
}(window));
