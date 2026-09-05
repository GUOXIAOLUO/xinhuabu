/* Pure execution-result media extraction shared by temporary Canvas adapters. */
(function exposeCanvasMediaResultNormalizer(global) {
    'use strict';

    const DEFAULT_NESTED_KEYS = ['outputs', 'videos', 'images', 'urls', 'data', 'result'];
    const DEFAULT_ROOT_KEYS = ['items', 'outputs', 'videos', 'audios', 'texts', 'files', 'images', 'urls', 'data', 'result', 'output', 'url'];
    const VALUE_KEYS = ['url', 'path', 'src', 'uri'];
    const SCALAR_KEYS = [...VALUE_KEYS, 'output', 'output_url', 'outputUrl', 'video', 'video_url', 'videoUrl', 'mp4_url', 'mp4Url', 'download_url', 'downloadUrl', 'preview_url', 'previewUrl'];

    function extract(result, options = {}) {
        const entries = [];
        const nestedKeys = options.nestedKeys || DEFAULT_NESTED_KEYS;
        const rootKeys = options.rootKeys || DEFAULT_ROOT_KEYS;
        const copyFields = options.copyFields || [];
        const add = value => {
            if (!value) return;
            if (typeof value === 'string') { entries.push(value); return; }
            if (Array.isArray(value)) { value.forEach(add); return; }
            if (typeof value !== 'object') return;
            const url = VALUE_KEYS.map(key => value[key]).find(Boolean);
            if (url) {
                const item = {url, kind:value.kind || value.type || value.mediaKind || '', name:value.name || value.filename || ''};
                copyFields.forEach(key => {
                    const number = Number(value[key]);
                    if (Number.isFinite(number) && number > 0) item[key] = number;
                });
                entries.push(item);
            }
            nestedKeys.forEach(key => add(value[key]));
            SCALAR_KEYS.forEach(key => add(value[key]));
        };
        if (options.includeRoot) add(result);
        rootKeys.forEach(key => add(result?.[key]));
        const seen = new Set();
        return entries.map(item => {
            const url = typeof item === 'string' ? item : item?.url || '';
            return !url || seen.has(url) ? null : (seen.add(url), item);
        }).filter(Boolean);
    }

    global.WorkbenchCanvasMediaResultNormalizer = Object.freeze({extract});
}(window));
