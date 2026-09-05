/* Pure intrinsic-media sizing shared by temporary Canvas adapters. */
(function exposeCanvasMediaLayout(global) {
    'use strict';

    function intrinsicSize(source, fields = ['natural_w', 'natural_h', 'width', 'height', 'w', 'h', 'layout_w', 'layout_h', 'preview_w', 'preview_h']) {
        const values = source && typeof source === 'object' ? source : {};
        const widthFields = fields.filter(field => /(?:^|_)w(?:idth)?$/i.test(field));
        const heightFields = fields.filter(field => /(?:^|_)h(?:eight)?$/i.test(field));
        const width = Number(widthFields.map(field => values[field]).find(value => Number(value) > 0) || 0);
        const height = Number(heightFields.map(field => values[field]).find(value => Number(value) > 0) || 0);
        return width > 0 && height > 0 ? {width, height} : {width:0, height:0};
    }

    function contain(size, maxWidth, maxHeight, options = {}) {
        const width = Number(size?.width || 0);
        const height = Number(size?.height || 0);
        if (!(width > 0 && height > 0)) return null;
        const minWidth = Number(options.minWidth || 0);
        const minHeight = Number(options.minHeight || 0);
        const fit = Math.min(Number(maxWidth) / width, Number(maxHeight) / height);
        return {
            width:Math.max(minWidth, Math.round(width * fit)),
            height:Math.max(minHeight, Math.round(height * fit))
        };
    }

    function thumbnailSize(source, maxSize, options = {}) {
        const limit = Math.max(Number(options.minSize ?? 28), Math.round(Number(maxSize) || 96));
        const size = intrinsicSize(source, options.fields);
        return contain(size, limit, limit, {minWidth:options.minSize ?? 28, minHeight:options.minSize ?? 28}) || {width:limit, height:limit};
    }

    global.WorkbenchCanvasMediaLayout = Object.freeze({intrinsicSize, contain, thumbnailSize});
}(window));
