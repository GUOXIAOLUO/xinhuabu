/* Browser renderer registry. It resolves node-card renderers from renderer
   capability predicates and has no Canvas page, storage, or provider knowledge. */
(function exposeWorkbenchRendererRegistry(global) {
    'use strict';

    function normalizeDescriptor(descriptor) {
        if (!descriptor || typeof descriptor !== 'object') throw new TypeError('Renderer descriptor is required');
        const id = String(descriptor.id || '').trim();
        const version = String(descriptor.version || '').trim();
        if (!id || !version) throw new TypeError('Renderer descriptor requires id and version');
        if (typeof descriptor.canRender !== 'function' || typeof descriptor.mount !== 'function') {
            throw new TypeError('Renderer descriptor requires canRender and mount functions');
        }
        return Object.freeze({
            id,
            version,
            priority: Number.isFinite(Number(descriptor.priority)) ? Number(descriptor.priority) : 0,
            canRender: descriptor.canRender,
            mount: descriptor.mount,
        });
    }

    function create(initialDescriptors) {
        const descriptors = new Map();

        function key(id, version) {
            return `${String(id || '').trim()}@${String(version || '').trim()}`;
        }

        function register(descriptor) {
            const normalized = normalizeDescriptor(descriptor);
            const descriptorKey = key(normalized.id, normalized.version);
            if (descriptors.has(descriptorKey)) throw new RangeError(`renderer already registered: ${descriptorKey}`);
            descriptors.set(descriptorKey, normalized);
            return normalized;
        }

        function resolve(node, options) {
            const preferred = options && options.renderer;
            if (preferred && preferred.id && preferred.version) {
                const exact = descriptors.get(key(preferred.id, preferred.version));
                if (exact && exact.canRender(node, options || {})) return exact;
            }
            return Array.from(descriptors.values())
                .filter(descriptor => descriptor.canRender(node, options || {}))
                .sort((left, right) => right.priority - left.priority || left.id.localeCompare(right.id))[0] || null;
        }

        function requireRenderer(node, options) {
            const descriptor = resolve(node, options);
            if (!descriptor) throw new RangeError('no registered renderer accepts this node');
            return descriptor;
        }

        function all() {
            return Object.freeze(Array.from(descriptors.values()));
        }

        Array.from(initialDescriptors || []).forEach(register);
        return Object.freeze({all, register, require:requireRenderer, resolve});
    }

    global.WorkbenchRendererRegistry = Object.freeze({create});
}(window));
