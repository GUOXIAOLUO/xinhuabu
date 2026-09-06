/* Shared Canvas save scheduling: debounce, in-flight coalescing, retry marking. */
(function exposeCanvasSaveScheduler(global) {
    'use strict';

    function positiveNumber(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) && number > 0 ? number : fallback;
    }

    function create(options) {
        const settings = options || {};
        if (typeof settings.run !== 'function') throw new TypeError('run callback is required');
        const debounceMs = positiveNumber(settings.debounceMs, 500);
        // allowOverlap preserves adapters whose save request may run concurrently
        // with an in-flight one; the default coalesces into one retry instead.
        const allowOverlap = settings.allowOverlap === true;
        const onRetry = typeof settings.onRetry === 'function' ? settings.onRetry : () => {};
        let timer = null;
        let inFlightCount = 0;
        let again = false;

        function schedule(delayMs) {
            if (inFlightCount > 0 && !allowOverlap) {
                clearTimeout(timer);
                timer = null;
                again = true;
                return;
            }
            clearTimeout(timer);
            timer = setTimeout(() => {
                timer = null;
                flush();
            }, positiveNumber(delayMs, debounceMs));
        }

        async function flush() {
            if (inFlightCount > 0 && !allowOverlap) {
                again = true;
                return false;
            }
            inFlightCount += 1;
            again = false;
            try {
                await settings.run();
            } finally {
                inFlightCount -= 1;
                if (inFlightCount === 0 && again) {
                    again = false;
                    onRetry();
                    setTimeout(() => { flush(); }, 0);
                }
            }
            return true;
        }

        function cancel() {
            clearTimeout(timer);
            timer = null;
        }

        function markAgain() {
            if (!allowOverlap) again = true;
        }

        return Object.freeze({
            schedule,
            flush,
            cancel,
            markAgain,
            isInFlight: () => inFlightCount > 0,
            hasPendingAgain: () => again,
            hasScheduled: () => timer !== null,
        });
    }

    global.WorkbenchCanvasSaveScheduler = Object.freeze({create});
}(window));
