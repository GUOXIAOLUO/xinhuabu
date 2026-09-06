/* Pure renderer-admission boundary. Page adapters project their retained
   product policy; this module only evaluates the declared generic predicates. */
(function exposeWorkbenchRendererAdmission(global) {
    'use strict';
    function admits(policy, node) {
        const settings = policy || {};
        if (!settings.enabled || !node) return false;
        if (Array.isArray(settings.types)) return settings.types.includes(node.type);
        if (typeof settings.accepts === 'function') return Boolean(settings.accepts(node));
        return false;
    }
    global.WorkbenchRendererAdmission = Object.freeze({admits});
}(window));
