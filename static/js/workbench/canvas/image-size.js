(function(global){
    'use strict';

    function apiImageSize(ratioValue, resolutionValue, options={}){
        if(resolutionValue === 'auto') return 'auto';
        if(resolutionValue === 'custom') return String(options.customSize || '').trim();
        const resolutionKey = resolutionValue || '1k';
        const sizeMap = options.sizeMap || {};
        if(ratioValue === 'custom' || ratioValue === 'source'){
            const parsed = options.parseRatio?.(options.customRatio);
            const longSide = options.longSideByResolution?.[resolutionKey] || 1024;
            if(parsed){
                const pixelLimit = options.pixelLimitByResolution?.[resolutionKey] || (longSide * longSide);
                const rawWidth = parsed >= 1 ? longSide : Math.min(longSide * parsed, Math.sqrt(pixelLimit * parsed));
                const rawHeight = parsed >= 1 ? Math.min(longSide / parsed, Math.sqrt(pixelLimit / parsed)) : longSide;
                const width = Math.floor(rawWidth / 16) * 16;
                const height = Math.floor(rawHeight / 16) * 16;
                return `${Math.max(64, width)}x${Math.max(64, height)}`;
            }
        }
        const ratioKey = ratioValue && sizeMap[ratioValue] ? ratioValue : 'square';
        return sizeMap[ratioKey]?.[resolutionKey] || sizeMap.square?.[resolutionKey] || sizeMap.square?.['1k'] || '';
    }

    global.WorkbenchCanvasImageSize = Object.freeze({apiImageSize});
})(window);
