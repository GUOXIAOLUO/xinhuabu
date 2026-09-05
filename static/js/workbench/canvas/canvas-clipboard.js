(function(global){
    'use strict';

    function copyWithCopyEvent(value, documentRef=document){
        let handled = false;
        const onCopy = event => {
            event.preventDefault();
            event.clipboardData?.setData('text/plain', value);
            handled = true;
        };
        documentRef.addEventListener('copy', onCopy);
        try {
            return documentRef.execCommand('copy') && handled;
        } catch(_) {
            return false;
        } finally {
            documentRef.removeEventListener('copy', onCopy);
        }
    }

    function copyWithTextarea(value, documentRef=document){
        let textarea = null;
        try {
            textarea = documentRef.createElement('textarea');
            textarea.value = value;
            textarea.setAttribute('readonly', '');
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '0';
            textarea.style.opacity = '0';
            documentRef.body.appendChild(textarea);
            textarea.focus({preventScroll:true});
            textarea.select();
            textarea.setSelectionRange(0, textarea.value.length);
            return documentRef.execCommand('copy');
        } catch(_) {
            return false;
        } finally {
            textarea?.remove();
        }
    }

    async function matchesText(value, navigatorRef=global.navigator, isSecureContext=global.isSecureContext){
        try {
            if(navigatorRef?.clipboard?.readText && isSecureContext){
                return (await navigatorRef.clipboard.readText()) === value;
            }
        } catch(_) {}
        return null;
    }

    async function copyText(text, options={}){
        const value = String(text || '');
        if(!value) return false;
        const documentRef = options.document || global.document;
        const navigatorRef = options.navigator || global.navigator;
        const isSecureContext = options.isSecureContext ?? global.isSecureContext;
        if(copyWithCopyEvent(value, documentRef) || copyWithTextarea(value, documentRef)){
            const verified = await matchesText(value, navigatorRef, isSecureContext);
            return verified !== false;
        }
        try {
            if(navigatorRef?.clipboard?.writeText && isSecureContext !== false){
                await navigatorRef.clipboard.writeText(value);
                const verified = await matchesText(value, navigatorRef, isSecureContext);
                return verified !== false;
            }
        } catch(_) {}
        return false;
    }

    global.WorkbenchCanvasClipboard = Object.freeze({
        copyWithCopyEvent,
        copyWithTextarea,
        matchesText,
        copyText,
    });
})(window);
