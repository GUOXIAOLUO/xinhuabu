/* Shared semantic-zoom presentation application for Canvas editors.
   Adapters keep enablement decisions, selectors, node iteration and call
   timing; this owner applies one computed presentation model to NodeShell
   and legacy node DOM, and builds the semantic-zoom indicator. */
(function exposeWorkbenchSemanticZoomApply(global) {
    'use strict';

    const SHELL_SLOT_SELECTORS = Object.freeze({
        title: '.workbench-node-shell__title',
        status: '.workbench-node-shell__status',
        actions: '.workbench-node-shell__actions',
        content: '.workbench-node-shell__content',
        toolbar: '.workbench-node-shell__toolbar',
        footer: '.workbench-node-shell__footer',
    });

    function setVisible(element, visible, visibleDisplay = '') {
        if(!element) return;
        element.hidden = !visible;
        element.style.display = visible ? visibleDisplay : 'none';
    }

    function shellSlots(shellEl) {
        const slots = {};
        Object.entries(SHELL_SLOT_SELECTORS).forEach(([name, selector]) => {
            slots[name] = shellEl ? shellEl.querySelector(selector) : null;
        });
        return slots;
    }

    function ensureIndicator(options) {
        const settings = options || {};
        const existing = settings.container?.querySelector?.(`#${settings.id}`);
        const indicator = existing || document.createElement('output');
        indicator.id = settings.id;
        indicator.className = settings.className;
        indicator.setAttribute('aria-live', 'polite');
        const percent = Math.round(Number(settings.scale) * 100);
        indicator.value = String(percent);
        const label = settings.labels?.[settings.presentation] || settings.presentation;
        indicator.textContent = `${percent}% · ${label} · ${settings.count} 节点`;
        if(!existing && settings.container) settings.container.appendChild(indicator);
        return indicator;
    }

    function applyShellPresentation(options) {
        const settings = options || {};
        const shellEl = settings.shellEl;
        if(!shellEl) return;
        const model = settings.model;
        shellEl.dataset.semanticPresentation = model.presentation;
        if(settings.outerEl) settings.outerEl.dataset.semanticPresentation = model.presentation;
        shellEl.dataset.semanticControls = String(model.showControls);
        shellEl.dataset.semanticPorts = String(model.showPorts);
        const slots = shellSlots(shellEl);
        setVisible(slots.title, model.showTitle);
        setVisible(slots.status, model.showSummary, 'inline');
        setVisible(slots.content, model.showContent);
        [slots.actions, slots.toolbar, slots.footer].forEach(slot => setVisible(slot, model.showControls));
        (settings.portElements || []).forEach(port => setVisible(port, model.showPorts));
    }

    function resetShellPresentation(options) {
        const settings = options || {};
        const shellEl = settings.shellEl;
        if(!shellEl) return;
        ['semanticPresentation', 'semanticControls', 'semanticPorts'].forEach(key => delete shellEl.dataset[key]);
        if(settings.outerEl) delete settings.outerEl.dataset.semanticPresentation;
        Object.values(shellSlots(shellEl)).forEach(slot => {
            if(!slot) return;
            slot.hidden = false;
            slot.style.removeProperty('display');
        });
        (settings.portElements || []).forEach(port => {
            port.hidden = false;
            port.style.removeProperty('display');
        });
        (settings.menuElements || []).forEach(menu => {
            menu.hidden = false;
            menu.style.removeProperty('display');
        });
    }

    function applyLegacyPresentation(options) {
        const settings = options || {};
        const nodeEl = settings.nodeEl;
        if(!nodeEl) return;
        const model = settings.model;
        nodeEl.dataset.semanticPresentation = model.presentation;
        const targets = settings.targets || {};
        setVisible(targets.head, model.showTitle, settings.headDisplay);
        setVisible(targets.body, model.showContent);
        setVisible(targets.resize, model.showControls);
        (settings.portElements || []).forEach(port => setVisible(port, model.showPorts));
    }

    function resetLegacyPresentation(options) {
        const settings = options || {};
        const nodeEl = settings.nodeEl;
        if(!nodeEl) return;
        delete nodeEl.dataset.semanticPresentation;
        Object.values(settings.targets || {}).forEach(element => {
            if(!element) return;
            element.hidden = false;
            element.style.removeProperty('display');
        });
        (settings.portElements || []).forEach(port => {
            port.hidden = false;
            port.style.removeProperty('display');
        });
    }

    global.WorkbenchSemanticZoomApply = Object.freeze({
        setVisible,
        shellSlots,
        ensureIndicator,
        applyShellPresentation,
        resetShellPresentation,
        applyLegacyPresentation,
        resetLegacyPresentation,
    });
}(window));
