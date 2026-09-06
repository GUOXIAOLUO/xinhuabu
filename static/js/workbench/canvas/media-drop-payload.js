/* Shared DataTransfer file traversal. Media policy and Canvas mutation remain adapter-owned. */
(function exposeCanvasMediaDrop(global) {
    'use strict';

    function entryForItem(item) {
        try { return item && typeof item.webkitGetAsEntry === 'function' ? item.webkitGetAsEntry() : null; } catch (_) { return null; }
    }

    async function filesFromEntry(entry) {
        if (!entry) return [];
        if (entry.isFile) {
            return new Promise(resolve => entry.file(file => resolve(file ? [file] : []), () => resolve([])));
        }
        if (!entry.isDirectory || typeof entry.createReader !== 'function') return [];
        const reader = entry.createReader();
        const children = [];
        while (true) {
            const batch = await new Promise(resolve => reader.readEntries(resolve, () => resolve([])));
            if (!batch.length) break;
            children.push(...batch);
        }
        return (await Promise.all(children.map(filesFromEntry))).flat();
    }

    async function filesFromDataTransfer(dataTransfer, isSupportedFile) {
        if (typeof isSupportedFile !== 'function') throw new TypeError('filesFromDataTransfer requires an isSupportedFile callback');
        const items = Array.from(dataTransfer && dataTransfer.items || []);
        const entries = items.map(entryForItem).filter(Boolean);
        const raw = entries.length
            ? (await Promise.all(entries.map(filesFromEntry))).flat()
            : Array.from(dataTransfer && dataTransfer.files || []);
        return raw.filter(isSupportedFile);
    }

    function dataTypes(dataTransfer) {
        return Array.from(dataTransfer && dataTransfer.types || []).map(type => String(type || ''));
    }

    function readData(dataTransfer, type) {
        try { return dataTransfer && typeof dataTransfer.getData === 'function' ? dataTransfer.getData(type) || '' : ''; } catch (_) { return ''; }
    }

    function uniqueValues(values) {
        const seen = new Set();
        return Array.from(values || []).filter(value => {
            const key = String(value || '').trim();
            if (!key || seen.has(key)) return false;
            seen.add(key);
            return true;
        });
    }

    function decodeText(value) {
        const text = String(value || '').trim();
        if (!text) return '';
        try { return decodeURIComponent(text); } catch (_) { return text; }
    }

    function textFragments(value) {
        const text = String(value || '').trim();
        if (!text) return [];
        const fragments = [];
        if (/<img|<a\s/i.test(text) && typeof global.DOMParser === 'function') {
            const doc = new global.DOMParser().parseFromString(text, 'text/html');
            doc.querySelectorAll('img[src],a[href]').forEach(element => fragments.push(element.getAttribute('src') || element.getAttribute('href') || ''));
        }
        text.split(/\r?\n/).forEach(line => {
            const item = line.trim();
            if (item) fragments.push(item);
        });
        const downloadUrl = text.match(/^image\/[^\s:]+:(.+)$/i);
        if (downloadUrl) fragments.push(downloadUrl[1]);
        return fragments;
    }

    function textCandidates(dataTransfer, textTypes) {
        if (!dataTransfer) return [];
        const types = uniqueValues([...(textTypes || []), ...dataTypes(dataTransfer)]);
        const values = types.map(type => readData(dataTransfer, type)).filter(Boolean);
        return uniqueValues(values.flatMap(textFragments).map(decodeText)).filter(value => !value.startsWith('#'));
    }

    function payload(dataTransfer, options) {
        const settings = options && typeof options === 'object' ? options : {};
        if (typeof settings.isSupportedFile !== 'function' || typeof settings.isLocalValue !== 'function' || typeof settings.isRemoteValue !== 'function') {
            throw new TypeError('payload requires file, local-path and remote-url policy callbacks');
        }
        const files = Array.from(dataTransfer && dataTransfer.files || []).filter(settings.isSupportedFile);
        if (files.length) return {type:'files', files};
        const candidates = textCandidates(dataTransfer, settings.textTypes);
        const localPaths = uniqueValues(candidates.filter(settings.isLocalValue));
        if (localPaths.length) return {type:'localPaths', localPaths};
        const url = candidates.find(settings.isRemoteValue) || '';
        return url ? {type:'url', url} : {type:'none'};
    }

    async function resolvePayload(dataTransfer, options) {
        const settings = options && typeof options === 'object' ? options : {};
        const resolved = payload(dataTransfer, settings);
        if (resolved.type !== 'none') return resolved;
        if (typeof settings.shouldTraverse === 'function' && !settings.shouldTraverse(dataTransfer)) return resolved;
        const files = await filesFromDataTransfer(dataTransfer, settings.isSupportedFile);
        return files.length ? {type:'files', files} : resolved;
    }

    async function uploadFiles(files, options) {
        const settings = options && typeof options === 'object' ? options : {};
        if (typeof global.fetch !== 'function' || typeof global.FormData !== 'function') throw new Error('File upload requires browser fetch and FormData support.');
        const form = new global.FormData();
        Array.from(files || []).forEach(file => {
            const name = typeof settings.fileName === 'function' ? settings.fileName(file) : null;
            if (name) form.append('files', file, name);
            else form.append('files', file);
        });
        const response = await global.fetch(settings.endpoint || '/api/ai/upload', {method:'POST', body:form});
        if (settings.rejectOnError && !response.ok) {
            const message = typeof settings.errorMessage === 'function'
                ? await settings.errorMessage(response)
                : '';
            throw new Error(message || `Upload failed (${response.status})`);
        }
        const data = await response.json();
        return Array.isArray(data && data.files) ? data.files : [];
    }

    global.WorkbenchCanvasMediaDrop = Object.freeze({
        entryForItem, filesFromEntry, filesFromDataTransfer,
        dataTypes, readData, textCandidates, payload, resolvePayload, uploadFiles,
    });
}(window));
