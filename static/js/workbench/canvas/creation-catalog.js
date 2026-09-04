/* Canonical, side-effect-free creation definitions. Page adapters may retain
   compatibility-specific availability rules while creation metadata becomes a
   stable catalog that later entry points can consume without DOM or storage. */
(function exposeWorkbenchCreationCatalog(global) {
    'use strict';

    function requiredString(value, label) {
        if (typeof value !== 'string' || !value.trim()) {
            throw new TypeError(`${label} must be a non-empty string`);
        }
        return value;
    }

    function normalize(entry) {
        if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
            throw new TypeError('creation catalog entry must be an object');
        }
        const definition = entry.definition_ref;
        if (!definition || typeof definition !== 'object' || Array.isArray(definition)) {
            throw new TypeError('definition_ref must be an object');
        }
        if (!Number.isFinite(entry.order)) {
            throw new TypeError('order must be a finite number');
        }
        const metadata = entry.metadata === undefined ? {} : entry.metadata;
        if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata)) {
            throw new TypeError('metadata must be an object');
        }
        return Object.freeze({
            id: requiredString(entry.id, 'id'),
            definition_ref: Object.freeze({
                id: requiredString(definition.id, 'definition_ref.id'),
                type: requiredString(definition.type, 'definition_ref.type'),
                version: requiredString(definition.version, 'definition_ref.version'),
            }),
            order: entry.order,
            metadata: Object.freeze({...metadata}),
        });
    }

    function create(entries) {
        if (!Array.isArray(entries)) throw new TypeError('entries must be an array');
        const byId = new Map();
        entries.forEach(entry => {
            const normalized = normalize(entry);
            if (byId.has(normalized.id)) throw new RangeError(`duplicate creation catalog id: ${normalized.id}`);
            byId.set(normalized.id, normalized);
        });
        const all = Object.freeze(Array.from(byId.values()).sort((left, right) => left.order - right.order || left.id.localeCompare(right.id)));
        return Object.freeze({
            all: () => all,
            get: id => byId.get(id) || null,
        });
    }

    global.WorkbenchCreationCatalog = Object.freeze({create, normalize});
}(window));
