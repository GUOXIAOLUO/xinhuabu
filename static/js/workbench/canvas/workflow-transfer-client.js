/* Transport-only workflow archive boundary shared by temporary Canvas adapters. */
(function exposeWorkflowTransferClient(global) {
    'use strict';

    async function responseError(response, fallback) {
        const payload = await response.json().catch(() => ({}));
        return payload?.detail || payload?.message || fallback;
    }

    async function exportArchive(payload, filename) {
        const response = await fetch('/api/canvas-workflows/export', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({...payload, include_resources: true, filename}),
        });
        if (!response.ok) throw new Error(await responseError(response, '导出工作流失败'));
        return response.blob();
    }

    async function importArchive(file) {
        const form = new FormData();
        form.append('file', file);
        const response = await fetch('/api/canvas-workflows/import', {method: 'POST', body: form});
        if (!response.ok) throw new Error(await responseError(response, '导入工作流失败'));
        return response.json();
    }

    global.WorkbenchCanvasWorkflowTransfer = Object.freeze({
        exportArchive,
        importArchive,
    });
}(window));
