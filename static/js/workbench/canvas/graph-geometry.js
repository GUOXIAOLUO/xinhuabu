/* Shared, business-neutral geometry for Canvas ports and edges. It has no DOM,
   storage, renderer, provider, or persisted-edge-format dependency. */
(function exposeWorkbenchCanvasGraphGeometry(global) {
    'use strict';

    function number(value, fallback) {
        const parsed = Number(value);
        return Number.isFinite(parsed) ? parsed : fallback;
    }

    function rect(value) {
        const source = value && typeof value === 'object' ? value : {};
        return Object.freeze({
            x:number(source.x, 0),
            y:number(source.y, 0),
            width:Math.max(1, number(source.width, source.w === undefined ? 1 : source.w)),
            height:Math.max(1, number(source.height, source.h === undefined ? 1 : source.h)),
        });
    }

    function portAnchor(bounds, side) {
        const box = rect(bounds);
        switch (side) {
        case 'top': return Object.freeze({x:box.x + box.width / 2, y:box.y});
        case 'bottom': return Object.freeze({x:box.x + box.width / 2, y:box.y + box.height});
        case 'right': return Object.freeze({x:box.x + box.width, y:box.y + box.height / 2});
        case 'left':
        default: return Object.freeze({x:box.x, y:box.y + box.height / 2});
        }
    }

    function horizontalBezier(from, to) {
        const start = from || {x:0, y:0};
        const end = to || {x:0, y:0};
        const dx = Math.max(50, Math.abs(number(end.x, 0) - number(start.x, 0)) * 0.45);
        return `M${number(start.x, 0)} ${number(start.y, 0)} C ${number(start.x, 0) + dx} ${number(start.y, 0)}, ${number(end.x, 0) - dx} ${number(end.y, 0)}, ${number(end.x, 0)} ${number(end.y, 0)}`;
    }

    global.WorkbenchCanvasGraphGeometry = Object.freeze({rect, portAnchor, horizontalBezier});
}(window));
