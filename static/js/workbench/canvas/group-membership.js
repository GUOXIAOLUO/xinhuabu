/* Shared, business-neutral membership queries for Canvas composite nodes.
   Adapters supply the set of records that act as groups. */
(function exposeWorkbenchCanvasGroupMembership(global) {
    'use strict';

    function groupItems(group) {
        return Array.isArray(group?.items)
            ? Array.from(new Set(group.items.map(String).filter(Boolean)))
            : [];
    }

    function membershipIndex(groups) {
        const index = new Map();
        Array.from(groups || []).forEach(group => {
            const groupId = String(group?.id || '');
            if(!groupId) return;
            groupItems(group).forEach(memberId => {
                if(memberId !== groupId && !index.has(memberId)) index.set(memberId, groupId);
            });
        });
        return index;
    }

    function containingGroupId(groups, nodeId) {
        return membershipIndex(groups).get(String(nodeId || '')) || '';
    }

    function scopeId(groups, groupIds, nodeId) {
        const id = String(nodeId || '');
        return containingGroupId(groups, id) || (new Set(Array.from(groupIds || [], String)).has(id) ? id : '');
    }

    global.WorkbenchCanvasGroupMembership = Object.freeze({groupItems, membershipIndex, containingGroupId, scopeId});
}(window));
