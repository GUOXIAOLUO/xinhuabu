/* Pure screen-space placement for NodeShell toolbar and connection controls. */
(function exposeWorkbenchScreenSpaceControls(global) {
    'use strict';

    function positive(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) && number > 0 ? number : fallback;
    }

    function viewportValue(viewport, key, fallback) {
        const value = Number(viewport && viewport[key]);
        return Number.isFinite(value) ? value : fallback;
    }

    function worldToScreen(point, viewport) {
        const scale = positive(viewportValue(viewport, 'scale', 1), 1);
        return Object.freeze({
            x: viewportValue(viewport, 'x', 0) + Number(point && point.x || 0) * scale,
            y: viewportValue(viewport, 'y', 0) + Number(point && point.y || 0) * scale,
        });
    }

    function worldSizeForPixels(pixelSize, viewport) {
        return positive(pixelSize, 28) / positive(viewportValue(viewport, 'scale', 1), 1);
    }

    function controlViewModel(node, viewport, pixelSize) {
        const position = node && node.position || {};
        const size = node && node.size || {};
        const width = positive(size.width, 280);
        const height = positive(size.height, 180);
        const topCenter = worldToScreen({x: Number(position.x || 0) + width / 2, y: Number(position.y || 0)}, viewport);
        const middleLeft = worldToScreen({x: Number(position.x || 0), y: Number(position.y || 0) + height / 2}, viewport);
        const middleRight = worldToScreen({x: Number(position.x || 0) + width, y: Number(position.y || 0) + height / 2}, viewport);
        return Object.freeze({
            nodeId: String(node && node.id || ''),
            targetPixels: positive(pixelSize, 28),
            worldControlSize: worldSizeForPixels(pixelSize, viewport),
            toolbar: topCenter,
            inputPort: middleLeft,
            outputPort: middleRight,
        });
    }

    global.WorkbenchScreenSpaceControls = Object.freeze({worldToScreen, worldSizeForPixels, controlViewModel});
}(window));
