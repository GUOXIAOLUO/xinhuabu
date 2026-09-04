/* Shared result-placement intent for Canvas execution adapters. It only
   normalizes a safe target choice; page adapters still create, persist, and
   render their own Legacy nodes. */
(function exposeWorkbenchGenerationIntent(global) {
    'use strict';

    function sourceId(value) {
        const id = String(value || '').trim();
        if (!id) throw new TypeError('sourceId must be a non-empty string');
        return id;
    }

    function planResultTarget(options) {
        const source = options && typeof options === 'object' ? options : {};
        const createsBranch = Boolean(source.isGroup || (source.hasMedia && !source.workflowMode));
        return Object.freeze({
            sourceId: sourceId(source.sourceId),
            disposition: createsBranch ? 'branch' : 'in_place',
        });
    }

    global.WorkbenchGenerationIntent = Object.freeze({planResultTarget});
}(window));
