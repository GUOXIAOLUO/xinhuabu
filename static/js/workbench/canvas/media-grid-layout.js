/* Pure media-grid fitting shared by temporary Canvas adapters. */
(function exposeCanvasMediaGridLayout(global) {
    'use strict';

    function fitSquareGrid(count, explicitW, explicitH, maxThumb, options = {}) {
        const pad = Number(options.pad ?? 32);
        const gap = Number(options.gap ?? 8);
        const maxVisibleRows = Number(options.maxVisibleRows ?? 4);
        const fallbackMaxVisibleRows = Number(options.fallbackMaxVisibleRows ?? maxVisibleRows);
        let best = null;
        for (let cols = 1; cols <= count; cols++) {
            const rows = Math.ceil(count / cols);
            const visibleRows = Math.min(Math.max(1, maxVisibleRows), rows);
            const availableW = explicitW - pad - (cols - 1) * gap;
            const availableH = explicitH - pad - (visibleRows - 1) * gap;
            if (availableW <= 0 || availableH <= 0) continue;
            const rawThumb = Math.floor(Math.min(availableW / cols, availableH / visibleRows));
            const fittedThumb = Math.max(28, Math.min(maxThumb, rawThumb));
            const fits = rawThumb >= 28;
            const usedW = cols * fittedThumb + (cols - 1) * gap + pad;
            const usedH = visibleRows * fittedThumb + (visibleRows - 1) * gap + pad;
            const spareW = Math.max(0, explicitW - usedW);
            const spareH = Math.max(0, explicitH - usedH);
            const score = [fits ? 1 : 0, fittedThumb, fittedThumb >= maxThumb ? cols : 0, -(spareW + spareH * 0.35), -rows];
            let better = !best;
            if (best) {
                for (let index = 0; index < score.length; index++) {
                    if (score[index] === best.score[index]) continue;
                    better = score[index] > best.score[index];
                    break;
                }
            }
            if (better) best = {cols, rows, visibleRows, thumb:fittedThumb, score};
        }
        const fallbackCols = Math.min(count, 2);
        const fallbackRows = Math.ceil(count / fallbackCols);
        return best || {cols:fallbackCols, rows:fallbackRows, visibleRows:Math.min(fallbackMaxVisibleRows, fallbackRows), thumb:28};
    }

    global.WorkbenchCanvasMediaGridLayout = Object.freeze({fitSquareGrid});
}(window));
