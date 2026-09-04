/* Pure semantic-zoom policy for NodeShell renderers. */
(function exposeWorkbenchSemanticZoom(global) {
    'use strict';

    const LEVELS = Object.freeze(['full', 'summary']);

    function normalizedScale(value) {
        const scale = Number(value);
        return Number.isFinite(scale) && scale > 0 ? scale : 1;
    }

    function presentationForScale(value) {
        const scale = normalizedScale(value);
        return scale >= 0.75 ? 'full' : 'summary';
    }

    function viewModel(node, viewportScale) {
        const presentation = presentationForScale(viewportScale);
        return Object.freeze({
            nodeId: String(node && node.id || ''),
            presentation,
            showContent: presentation === 'full',
            showSummary: presentation === 'summary',
            showTitle: true,
            showControls: presentation === 'full',
            showPorts: true,
        });
    }

    function viewModels(nodes, viewportScale) {
        return (Array.isArray(nodes) ? nodes : []).map(node => viewModel(node, viewportScale));
    }

    global.WorkbenchSemanticZoom = Object.freeze({LEVELS, presentationForScale, viewModel, viewModels});
}(window));
