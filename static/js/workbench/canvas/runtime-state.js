/* Shared, business-neutral Canvas runtime state. This module owns no DOM,
   storage, network, renderer, provider, or node-family behavior. */
(function exposeWorkbenchCanvasRuntime(global) {
    'use strict';

    const COMMANDS = Object.freeze({
        VIEWPORT_SET: 'canvas.viewport.set',
        VIEWPORT_PAN: 'canvas.viewport.pan',
        VIEWPORT_ZOOM_AT: 'canvas.viewport.zoom-at',
        SELECTION_REPLACE: 'canvas.selection.replace',
        SELECTION_TOGGLE: 'canvas.selection.toggle',
        SELECTION_CLEAR: 'canvas.selection.clear',
        GEOMETRY_REPLACE: 'canvas.geometry.replace',
        NODE_MOVE: 'canvas.node.move',
        NODE_RESIZE: 'canvas.node.resize',
    });

    function finite(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) ? number : fallback;
    }

    function clamp(value, minimum, maximum) {
        return Math.max(minimum, Math.min(maximum, value));
    }

    function normalizeLimits(options) {
        const minimum = Math.max(0.001, finite(options && options.minScale, 0.06));
        const maximum = Math.max(minimum, finite(options && options.maxScale, 8));
        return Object.freeze({minScale: minimum, maxScale: maximum});
    }

    function normalizeViewport(value, options) {
        const source = value && typeof value === 'object' ? value : {};
        const fallback = options && options.fallback && typeof options.fallback === 'object' ? options.fallback : {};
        const limits = normalizeLimits(options);
        return Object.freeze({
            x: finite(source.x, finite(fallback.x, 0)),
            y: finite(source.y, finite(fallback.y, 0)),
            scale: clamp(finite(source.scale, finite(fallback.scale, 1)), limits.minScale, limits.maxScale),
        });
    }

    function normalizePoint(value) {
        const source = value && typeof value === 'object' ? value : {};
        return Object.freeze({x: finite(source.x, 0), y: finite(source.y, 0)});
    }

    function screenToWorld(point, viewport) {
        const screen = normalizePoint(point);
        const view = normalizeViewport(viewport);
        return Object.freeze({
            x: (screen.x - view.x) / view.scale,
            y: (screen.y - view.y) / view.scale,
        });
    }

    function worldToScreen(point, viewport) {
        const world = normalizePoint(point);
        const view = normalizeViewport(viewport);
        return Object.freeze({
            x: world.x * view.scale + view.x,
            y: world.y * view.scale + view.y,
        });
    }

    function normalizeSelection(ids, availableIds) {
        const allowed = availableIds ? new Set(Array.from(availableIds, String)) : null;
        const seen = new Set();
        return Object.freeze(Array.from(ids || []).map(String).filter(id => {
            if (!id || seen.has(id) || (allowed && !allowed.has(id))) return false;
            seen.add(id);
            return true;
        }));
    }

    function normalizeGeometryItem(value) {
        const source = value && typeof value === 'object' ? value : {};
        const id = String(source.id || '');
        if (!id) return null;
        return Object.freeze({
            id,
            x: finite(source.x, 0),
            y: finite(source.y, 0),
            width: Math.max(1, finite(source.width, finite(source.w, 1))),
            height: Math.max(1, finite(source.height, finite(source.h, 1))),
        });
    }

    function geometryMap(values) {
        const result = new Map();
        Array.from(values || []).forEach(value => {
            const item = normalizeGeometryItem(value);
            if (item) result.set(item.id, item);
        });
        return result;
    }

    function serializeGeometry(geometry) {
        return Object.freeze(Array.from(geometry.values(), item => Object.freeze({...item})));
    }

    function create(options) {
        const settings = options || {};
        const limits = normalizeLimits(settings);
        let viewport = normalizeViewport(settings.viewport, limits);
        let geometry = geometryMap(settings.geometry || settings.nodes);
        let selection = normalizeSelection(settings.selectedIds, geometry.size ? geometry.keys() : null);
        let revision = 0;
        const listeners = new Set();

        function snapshot() {
            return Object.freeze({
                revision,
                viewport,
                selectedIds: selection,
                geometry: serializeGeometry(geometry),
            });
        }

        function publish(command, previous) {
            const event = Object.freeze({command:Object.freeze({...command}), previous, current:snapshot()});
            listeners.forEach(listener => listener(event));
            return event.current;
        }

        function replaceGeometry(values) {
            geometry = geometryMap(values);
            selection = normalizeSelection(selection, geometry.keys());
        }

        function updateGeometry(id, update) {
            const current = geometry.get(String(id || ''));
            if (!current) throw new RangeError(`unknown Canvas node: ${String(id || '')}`);
            geometry.set(current.id, Object.freeze({...current, ...update}));
        }

        function dispatch(command) {
            if (!command || typeof command !== 'object' || !String(command.type || '')) {
                throw new TypeError('Canvas runtime command requires a type');
            }
            const previous = snapshot();
            switch (command.type) {
            case COMMANDS.VIEWPORT_SET:
                viewport = normalizeViewport(command.viewport, {...limits, fallback:viewport});
                break;
            case COMMANDS.VIEWPORT_PAN:
                viewport = normalizeViewport({
                    x: viewport.x + finite(command.dx, 0),
                    y: viewport.y + finite(command.dy, 0),
                    scale: viewport.scale,
                }, limits);
                break;
            case COMMANDS.VIEWPORT_ZOOM_AT: {
                const anchor = normalizePoint(command.anchor);
                const worldAnchor = screenToWorld(anchor, viewport);
                const nextScale = clamp(finite(command.scale, viewport.scale), limits.minScale, limits.maxScale);
                viewport = normalizeViewport({
                    x: anchor.x - worldAnchor.x * nextScale,
                    y: anchor.y - worldAnchor.y * nextScale,
                    scale: nextScale,
                }, limits);
                break;
            }
            case COMMANDS.SELECTION_REPLACE:
                selection = normalizeSelection(command.ids, geometry.size ? geometry.keys() : null);
                break;
            case COMMANDS.SELECTION_TOGGLE: {
                const id = String(command.id || '');
                if (!id || (geometry.size && !geometry.has(id))) break;
                selection = selection.includes(id)
                    ? normalizeSelection(selection.filter(selectedId => selectedId !== id))
                    : normalizeSelection([...selection, id]);
                break;
            }
            case COMMANDS.SELECTION_CLEAR:
                selection = Object.freeze([]);
                break;
            case COMMANDS.GEOMETRY_REPLACE:
                replaceGeometry(command.geometry || command.nodes);
                break;
            case COMMANDS.NODE_MOVE:
                updateGeometry(command.id, {x:finite(command.x, 0), y:finite(command.y, 0)});
                break;
            case COMMANDS.NODE_RESIZE: {
                const current = geometry.get(String(command.id || ''));
                if (!current) throw new RangeError(`unknown Canvas node: ${String(command.id || '')}`);
                updateGeometry(current.id, {
                    width: Math.max(1, finite(command.width, current.width)),
                    height: Math.max(1, finite(command.height, current.height)),
                });
                break;
            }
            default:
                throw new RangeError(`unsupported Canvas runtime command: ${command.type}`);
            }
            revision += 1;
            return publish(command, previous);
        }

        function subscribe(listener) {
            if (typeof listener !== 'function') throw new TypeError('Canvas runtime listener must be a function');
            listeners.add(listener);
            return () => listeners.delete(listener);
        }

        return Object.freeze({dispatch, snapshot, subscribe});
    }

    global.WorkbenchCanvasRuntime = Object.freeze({
        COMMANDS,
        create,
        normalizeSelection,
        normalizeViewport,
        screenToWorld,
        worldToScreen,
    });
}(window));
