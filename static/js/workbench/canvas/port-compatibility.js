/* Shared, data-only port compatibility contract for Legacy Canvas adapters.
 * Unknown Legacy ports remain `legacy.any` for read/write compatibility. */
(function exposeWorkbenchCanvasPortCompatibility(global) {
    'use strict';

    function port(value) {
        const source = value && typeof value === 'object' ? value : {};
        const direction = source.direction === 'out' ? 'out' : source.direction === 'in' ? 'in' : '';
        const dataType = String(source.dataType || 'legacy.any').trim() || 'legacy.any';
        return Object.freeze({direction, dataType});
    }

    function isCompatible(fromValue, toValue) {
        const from = port(fromValue);
        const to = port(toValue);
        if (from.direction !== 'out' || to.direction !== 'in') return false;
        return from.dataType === 'legacy.any' || to.dataType === 'legacy.any' || from.dataType === to.dataType;
    }

    global.WorkbenchCanvasPortCompatibility = Object.freeze({port, isCompatible});
}(window));
