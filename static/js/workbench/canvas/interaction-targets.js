(function(global){
    'use strict';

    function isEditableTarget(target, options={}){
        const element = target || options.document?.activeElement || global.document?.activeElement;
        if(!element) return false;
        const tag = element.tagName;
        if(tag === 'INPUT' || tag === 'TEXTAREA' || element.isContentEditable) return true;
        const selector = options.selector || 'select, option';
        return Boolean(element.closest?.(selector));
    }

    global.WorkbenchCanvasInteractionTargets = Object.freeze({isEditableTarget});
})(window);
