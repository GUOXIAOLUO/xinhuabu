/* Generic LegacyRenderer adapter. It has no per-node-family render branches. */
(function exposeWorkbenchLegacyRenderer(global) {
    'use strict';

    function legacyPayload(node) {
        const extensions = node && node.extensions;
        const legacy = extensions && extensions.legacy;
        return legacy && legacy.payload && typeof legacy.payload === 'object' ? legacy.payload : null;
    }

    function canRender(node) {
        return Boolean(node && node.renderer && node.renderer.id === 'legacy' && legacyPayload(node));
    }

    function mount(shell, node, options) {
        if (!shell || !shell.contentHost) throw new TypeError('LegacyRenderer requires a NodeShell content host');
        if (!canRender(node)) throw new TypeError('LegacyRenderer requires a legacy payload and legacy renderer reference');
        const documentRef = (options && options.document) || shell.contentHost.ownerDocument || global.document;
        const payload = legacyPayload(node);
        const root = documentRef.createElement('div');
        root.className = 'workbench-legacy-renderer';
        root.dataset.legacyType = String(payload.type || node.definition_ref.id || 'unknown');
        const legacyContent = options && options.legacyContent;
        if (legacyContent) {
            root.append(legacyContent);
            shell.contentHost.replaceChildren(root);
            return Object.freeze({element: root, destroy: () => root.remove()});
        }

        const type = documentRef.createElement('span');
        type.className = 'workbench-legacy-renderer__type';
        type.textContent = root.dataset.legacyType;
        const summary = documentRef.createElement('span');
        summary.className = 'workbench-legacy-renderer__summary';
        summary.textContent = String(payload.name || payload.title || node.title || root.dataset.legacyType);
        root.append(type, summary);
        shell.contentHost.replaceChildren(root);

        return Object.freeze({element: root, destroy: () => root.remove()});
    }

    if(global.WorkbenchNodeInspector){
        global.WorkbenchNodeInspector.registerSectionProvider({id: 'legacy', version: '1'}, 'legacy-adapter', node => {
            const payload = legacyPayload(node) || {};
            const mediaCount = Array.isArray(payload.images) ? payload.images.length : 0;
            return {
                id: 'legacy-renderer',
                title: '兼容适配',
                fields: [
                    {id: 'renderer', label: '渲染器', value: 'Legacy · 1'},
                    {id: 'media-count', label: '素材', value: mediaCount ? `${mediaCount} 项` : '—'},
                ],
            };
        });
    }

    global.WorkbenchLegacyRenderer = Object.freeze({canRender, mount});
}(window));
