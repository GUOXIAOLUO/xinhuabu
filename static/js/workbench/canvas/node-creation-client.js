/* Versioned-node API client. Existing editors do not call this until P1.7 migration. */
(function exposeNodeCreationClient(global) {
    'use strict';

    async function request(path, method, body, actorId) {
        if (!actorId) throw new Error('A local actor id is required for versioned Canvas-node requests.');
        const response = await fetch(path, {
            method,
            headers: {'Content-Type': 'application/json', 'X-User-ID': actorId},
            body: body === undefined ? undefined : JSON.stringify(body),
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(payload.detail && payload.detail.message || payload.detail || `Request failed (${response.status})`);
        return payload;
    }

    function requirePositiveRevision(command) {
        const revision = Number(command && command.expected_revision);
        if (!Number.isInteger(revision) || revision < 1) {
            throw new Error('A positive expected_revision is required for connected Canvas creation.');
        }
    }

    global.WorkbenchNodeClient = Object.freeze({
        isLoopback: () => ['127.0.0.1', '::1', 'localhost'].includes(window.location.hostname),
        isEnabled: () => new URLSearchParams(window.location.search).get('versioned_nodes') === '1',
        create: (canvasId, command, actorId) => request(`/api/v1/canvases/${encodeURIComponent(canvasId)}/nodes`, 'POST', command, actorId),
        update: (canvasId, nodeId, command, actorId) => request(`/api/v1/canvases/${encodeURIComponent(canvasId)}/nodes/${encodeURIComponent(nodeId)}`, 'PUT', command, actorId),
        remove: (canvasId, nodeId, command, actorId) => request(`/api/v1/canvases/${encodeURIComponent(canvasId)}/nodes/${encodeURIComponent(nodeId)}`, 'DELETE', command, actorId),
        createNodeAndEdge: (canvasId, command, actorId) => {
            requirePositiveRevision(command);
            return request(`/api/v1/canvases/${encodeURIComponent(canvasId)}/graph/create-node-and-edge`, 'POST', command, actorId);
        },
    });
}(window));
