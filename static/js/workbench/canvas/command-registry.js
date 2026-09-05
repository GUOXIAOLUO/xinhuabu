/* Shared Canvas command catalog. Page adapters own behavior; this module owns
   stable command IDs and which canvas modes may expose them. */
(function exposeWorkbenchCanvasCommands(global) {
    'use strict';

    if (!global.WorkbenchCreationCatalog) throw new Error('WorkbenchCreationCatalog must load before WorkbenchCanvasCommands');

    const compatibilityCreateEntries = [
        ['canvas.create.image', 'image', ['classic', 'smart'], 10, ['classic', 'smart'], ['smart']],
        ['canvas.create.prompt', 'prompt', ['classic', 'smart'], 20, ['classic', 'smart'], ['smart']],
        ['canvas.create.loop', 'loop', ['classic', 'smart'], 30, ['classic', 'smart'], ['smart']],
        ['canvas.create.group', 'group', ['classic', 'smart'], 40, ['classic', 'smart'], ['classic', 'smart']],
        ['canvas.create.minimax', 'minimax', ['classic', 'smart'], 50, ['smart'], ['smart']],
        ['canvas.create.llm', 'llm', ['classic'], 60, [], []],
        ['canvas.create.generator', 'generator', ['classic'], 70, [], []],
        ['canvas.create.midjourney', 'midjourney', ['classic'], 80, [], []],
        ['canvas.create.msgen', 'msgen', ['classic'], 90, [], []],
        ['canvas.create.video', 'video', ['classic'], 100, [], []],
        ['canvas.create.rh', 'rh', ['classic'], 110, [], []],
        ['canvas.create.comfy', 'comfy', ['classic'], 120, [], []],
        ['canvas.create.ltx-director', 'ltxDirector', ['classic'], 130, [], []],
        ['canvas.create.output', 'output', ['classic'], 140, ['classic'], []],
    ].map(([id, createType, canvasKinds, order, versionedBlankCanvasKinds, versionedConnectedCanvasKinds]) => ({
        id,
        definition_ref: {id: createType, type: 'legacy-node', version: '0'},
        order,
        metadata: {
            createType,
            canvasKinds: Object.freeze(canvasKinds),
            versionedBlankCanvasKinds: Object.freeze(versionedBlankCanvasKinds),
            versionedConnectedCanvasKinds: Object.freeze(versionedConnectedCanvasKinds),
        },
    }));
    const createCommands = Object.freeze(global.WorkbenchCreationCatalog.create(compatibilityCreateEntries).all().map(entry => Object.freeze({
        id: entry.id,
        createType: entry.metadata.createType,
        canvasKinds: entry.metadata.canvasKinds,
        versionedBlankCanvasKinds: entry.metadata.versionedBlankCanvasKinds,
        versionedConnectedCanvasKinds: entry.metadata.versionedConnectedCanvasKinds,
        order: entry.order,
        definition_ref: entry.definition_ref,
    })));

    const selectionCommands = Object.freeze([
        Object.freeze({id:'canvas.selection.group', canvasKinds:Object.freeze(['classic', 'smart'])}),
    ]);

    const graphCommands = Object.freeze([
        Object.freeze({id:'canvas.graph.connect', canvasKinds:Object.freeze(['classic', 'smart'])}),
        Object.freeze({id:'canvas.graph.create-connected', canvasKinds:Object.freeze(['classic', 'smart'])}),
        Object.freeze({id:'canvas.group.add-member', canvasKinds:Object.freeze(['classic', 'smart'])}),
    ]);

    const nodeCommands = Object.freeze([
        Object.freeze({id:'canvas.node.inspect', canvasKinds:Object.freeze(['classic', 'smart'])}),
    ]);

    function supports(command, canvasKind) {
        return Boolean(command && command.canvasKinds.includes(canvasKind));
    }

    function createCommand(createType, canvasKind) {
        return createCommands.find(command => command.createType === createType && supports(command, canvasKind)) || null;
    }

    function selectionCommand(commandId, canvasKind) {
        return selectionCommands.find(command => command.id === commandId && supports(command, canvasKind)) || null;
    }

    function graphCommand(commandId, canvasKind) {
        return graphCommands.find(command => command.id === commandId && supports(command, canvasKind)) || null;
    }

    function nodeCommand(commandId, canvasKind) {
        return nodeCommands.find(command => command.id === commandId && supports(command, canvasKind)) || null;
    }

    function createCommandsFor(canvasKind) {
        return Object.freeze(createCommands.filter(command => supports(command, canvasKind)).sort((left, right) => left.order - right.order));
    }

    function creationCatalogFor(canvasKind) {
        return Object.freeze(createCommandsFor(canvasKind).map(command => Object.freeze({
            id: command.id,
            definition_ref: command.definition_ref,
            order: command.order,
        })));
    }

    function usesVersionedBlankCreation(command, canvasKind) {
        return Boolean(command && command.versionedBlankCanvasKinds.includes(canvasKind));
    }

    function usesVersionedConnectedCreation(command, canvasKind) {
        return Boolean(command && command.versionedConnectedCanvasKinds.includes(canvasKind));
    }

    function orderCreateMenuItems(items, catalog) {
        if (!Array.isArray(catalog)) throw new TypeError('catalog must be an array');
        const byId = new Map(Array.from(items || []).map(item => [item.dataset && item.dataset.canvasCommand, item]));
        const allowedIds = new Set(catalog.map(command => command.id));
        byId.forEach((item, id) => { item.hidden = !allowedIds.has(id); });
        return Object.freeze(catalog.map(command => byId.get(command.id)).filter(Boolean));
    }

    global.WorkbenchCanvasCommands = Object.freeze({createCommand, createCommandsFor, creationCatalogFor, graphCommand, nodeCommand, orderCreateMenuItems, selectionCommand, usesVersionedBlankCreation, usesVersionedConnectedCreation});
}(window));
