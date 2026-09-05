/* A narrow compatibility wrapper around retained Canvas execution functions.
 * It is not an ExecutorRegistry and never persists, selects providers, or
 * substitutes a runtime. */
(function exposeWorkbenchCanvasExecutionCompatibility(global) {
    'use strict';

    function request(value) {
        const source = value && typeof value === 'object' ? value : {};
        const canvasKind = source.canvasKind === 'smart' ? 'smart' : source.canvasKind === 'classic' ? 'classic' : '';
        const sourceNodeId = String(source.sourceNodeId || '').trim();
        if (!canvasKind || !sourceNodeId || typeof source.execute !== 'function') {
            throw new TypeError('execution compatibility request requires canvasKind, sourceNodeId, and execute');
        }
        return Object.freeze({canvasKind, sourceNodeId, execute: source.execute});
    }

    async function run(value) {
        const normalized = request(value);
        const startedAt = Date.now();
        try {
            const result = await normalized.execute();
            return Object.freeze({status: 'completed', canvasKind: normalized.canvasKind, sourceNodeId: normalized.sourceNodeId, startedAt, finishedAt: Date.now(), result});
        } catch (error) {
            error.workbenchExecutionCompatibility = Object.freeze({status: 'failed', canvasKind: normalized.canvasKind, sourceNodeId: normalized.sourceNodeId, startedAt, finishedAt: Date.now()});
            throw error;
        }
    }

    global.WorkbenchCanvasExecutionCompatibility = Object.freeze({request, run});
}(window));
