/* One normal Canvas URL plus explicit compatibility routing for historical
 * Smart records. This module does not load, persist, or reinterpret Canvas data. */
(function exposeWorkbenchCanvasEntryCompatibility(global) {
    'use strict';

    function requiredId(value, label) {
        const normalized = String(value || '').trim();
        if (!normalized) throw new TypeError(`${label} is required`);
        return normalized;
    }

    function normalCanvasUrl(canvasId, projectId) {
        return `/static/canvas.html?id=${encodeURIComponent(requiredId(canvasId, 'canvasId'))}&project=${encodeURIComponent(requiredId(projectId, 'projectId'))}`;
    }

    function requiresLegacySmartHandoff(canvas) {
        return String(canvas?.kind || 'classic').trim() === 'smart';
    }

    function legacySmartCanvasUrl(canvasId, search) {
        const params = new URLSearchParams(String(search || '').replace(/^\?/, ''));
        params.delete('id');
        const suffix = params.toString();
        return `/static/smart-canvas.html?id=${encodeURIComponent(requiredId(canvasId, 'canvasId'))}${suffix ? `&${suffix}` : ''}`;
    }

    function rememberCanvasListProject(projectId, options = {}) {
        const project = String(projectId || options.defaultProject || 'default');
        try { options.storage?.setItem?.(String(options.storageKey || ''), project); } catch (_error) {}
        return project;
    }

    function rememberedCanvasListProject(options = {}) {
        try { return options.storage?.getItem?.(String(options.storageKey || '')) || options.defaultProject || 'default'; } catch (_error) { return options.defaultProject || 'default'; }
    }

    function canvasListUrl(projectId, options = {}) {
        const project = rememberCanvasListProject(projectId, options);
        return `/static/canvas-list.html?project=${encodeURIComponent(project)}`;
    }

    global.WorkbenchCanvasEntryCompatibility = Object.freeze({normalCanvasUrl, requiresLegacySmartHandoff, legacySmartCanvasUrl, rememberCanvasListProject, rememberedCanvasListProject, canvasListUrl});
}(window));
