/* Read-only, renderer-neutral node inspector view model. */
(function exposeWorkbenchNodeInspector(global) {
    'use strict';

    const sectionProviders = new Map();
    const STATE_DESCRIPTIONS = Object.freeze({
        draft: '草稿，尚未准备执行',
        ready: '已准备，可执行',
        missing_input: '缺少必要输入',
        queued: '已排队等待执行',
        running: '正在执行',
        waiting_user: '等待用户操作',
        waiting_approval: '等待人工审批',
        completed: '已完成',
        failed: '执行失败',
        outdated: '依赖已变化，结果待更新',
        frozen: '结果已冻结',
    });

    function text(value, fallback) {
        const normalized = String(value ?? '').trim();
        return normalized || fallback;
    }

    function finite(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) ? number : fallback;
    }

    function field(id, label, value) {
        return Object.freeze({id, label, value: text(value, '—')});
    }

    function coordinate(value) {
        return String(Math.round(finite(value, 0)));
    }

    function rendererKey(renderer) {
        const source = renderer && typeof renderer === 'object' ? renderer : {};
        const id = text(source.id, '');
        const version = text(source.version, '');
        if(!id || !version) throw new TypeError('Inspector section providers require a renderer id and version');
        return `${id}@${version}`;
    }

    function normalizeSection(section) {
        if(!section || typeof section !== 'object') return null;
        const id = text(section.id, '');
        const title = text(section.title, '');
        if(!id || !title || !Array.isArray(section.fields)) return null;
        const fields = section.fields.map(item => {
            if(!item || typeof item !== 'object') return null;
            const fieldId = text(item.id, '');
            const label = text(item.label, '');
            if(!fieldId || !label) return null;
            return field(fieldId, label, item.value);
        }).filter(Boolean);
        return fields.length ? Object.freeze({id, title, fields: Object.freeze(fields)}) : null;
    }

    function registeredSections(node) {
        let providers;
        try { providers = sectionProviders.get(rendererKey(node?.renderer)); }
        catch(error) { return []; }
        if(!providers) return [];
        return [...providers.values()].flatMap(provider => {
            try {
                const result = provider(node);
                const candidates = Array.isArray(result) ? result : [result];
                return candidates.map(normalizeSection).filter(Boolean);
            } catch(error) {
                // Inspector extensions are optional diagnostics and must never block a canvas render.
                return [];
            }
        });
    }

    function registerSectionProvider(renderer, providerId, provider) {
        if(typeof providerId === 'function') {
            provider = providerId;
            providerId = 'default';
        }
        if(typeof provider !== 'function') throw new TypeError('Inspector section provider must be a function');
        const key = rendererKey(renderer);
        const id = text(providerId, '');
        if(!id) throw new TypeError('Inspector section providers require a provider id');
        const providers = sectionProviders.get(key) || new Map();
        if(providers.has(id)) throw new Error(`Inspector section provider is already registered: ${key}/${id}`);
        providers.set(id, provider);
        sectionProviders.set(key, providers);
    }

    function endpointNodeId(value) {
        if(typeof value === 'string') return value;
        if(!value || typeof value !== 'object') return '';
        return text(value.node_id || value.nodeId || value.id, '');
    }

    function connectionTotals(nodeId, context) {
        const source = context && typeof context === 'object' ? context : {};
        const connections = Array.isArray(source.connections) ? source.connections : [];
        return connections.reduce((result, edge) => {
            if(!edge || typeof edge !== 'object' || edge.state === 'disabled') return result;
            const from = endpointNodeId(edge.from || edge.source);
            const to = endpointNodeId(edge.to || edge.target);
            if(to === nodeId) result.input += 1;
            if(from === nodeId) result.output += 1;
            return result;
        }, {input: 0, output: 0});
    }

    function versionSection(node) {
        const source = node && typeof node === 'object' ? node : {};
        const revision = Math.max(1, Math.floor(finite(source.revision, 1)));
        const metadata = source.metadata && typeof source.metadata === 'object' ? source.metadata : {};
        const originLabel = text(metadata.inspector_origin_label, '');
        const origin = originLabel || (text(source.provenance_ref, '') ? '已关联来源' : '未记录');
        return Object.freeze({
            id: 'version',
            title: '版本与来源',
            fields: Object.freeze([
                field('revision', '版本', `r${revision}`),
                field('origin', '来源', origin),
            ]),
        });
    }

    function timestamp(value) {
        let milliseconds = Number(value);
        if(Number.isFinite(milliseconds) && milliseconds > 0) {
            if(milliseconds < 100000000000) milliseconds *= 1000;
            const date = new Date(milliseconds);
            if(!Number.isNaN(date.valueOf())) return `${date.toISOString().slice(0, 16).replace('T', ' ')} UTC`;
        }
        if(typeof value === 'string') {
            const date = new Date(value);
            if(!Number.isNaN(date.valueOf())) return `${date.toISOString().slice(0, 16).replace('T', ' ')} UTC`;
        }
        return '未记录';
    }

    function statusSection(node) {
        const source = node && typeof node === 'object' ? node : {};
        const metadata = source.metadata && typeof source.metadata === 'object' ? source.metadata : {};
        const state = text(source.state, 'ready');
        const changedAt = source.state_changed_at || source.stateChangedAt || metadata.state_changed_at;
        return Object.freeze({
            id: 'status',
            title: '状态说明',
            fields: Object.freeze([
                field('description', '说明', STATE_DESCRIPTIONS[state] || '未知状态'),
                field('changed-at', '状态时间', timestamp(changedAt)),
            ]),
        });
    }

    function referencesSection(node, context) {
        const source = node && typeof node === 'object' ? node : {};
        const inputs = Array.isArray(source.input_bindings) ? source.input_bindings.length : 0;
        const outputs = Array.isArray(source.output_refs) ? source.output_refs.length : 0;
        const connections = connectionTotals(text(source.id, ''), context);
        return Object.freeze({
            id: 'input-output',
            title: '输入与输出',
            fields: Object.freeze([
                field('input-references', '输入引用', `${inputs} 项`),
                field('output-references', '输出引用', `${outputs} 项`),
                field('input-connections', '输入连接', `${connections.input} 条`),
                field('output-connections', '输出连接', `${connections.output} 条`),
            ]),
        });
    }

    function selectionViewModel(nodes) {
        const records = Array.isArray(nodes) ? nodes.filter(node => node && typeof node === 'object') : [];
        const nodeIds = records.map(node => text(node.id, '')).filter(Boolean).sort();
        const typeIds = new Set(records.map(node => {
            const definition = node.definition_ref && typeof node.definition_ref === 'object' ? node.definition_ref : {};
            return text(definition.id, text(node.kind, 'unknown'));
        }));
        const stateCounts = new Map();
        records.forEach(node => {
            const state = text(node.state, 'ready');
            stateCounts.set(state, (stateCounts.get(state) || 0) + 1);
        });
        const stateSummary = [...stateCounts.entries()]
            .map(([state, count]) => `${state} ${count}`)
            .join(' · ');
        return Object.freeze({
            nodeId: `selection:${nodeIds.join('|')}`,
            title: `已选中 ${records.length} 个节点`,
            sections: Object.freeze([
                Object.freeze({
                    id: 'identity', title: '选择',
                    fields: Object.freeze([
                        field('selected-count', '节点', `${records.length} 个`),
                        field('type-count', '类型', `${typeIds.size} 种`),
                    ]),
                }),
                Object.freeze({
                    id: 'status', title: '状态',
                    fields: Object.freeze([field('state-summary', '分布', stateSummary || '未记录')]),
                }),
            ]),
        });
    }

    function viewModel(node, context) {
        const source = node && typeof node === 'object' ? node : {};
        const definition = source.definition_ref && typeof source.definition_ref === 'object'
            ? source.definition_ref
            : {};
        const position = source.position && typeof source.position === 'object' ? source.position : {};
        const size = source.size && typeof source.size === 'object' ? source.size : {};
        const title = text(source.title, text(definition.id, '节点'));
        const kind = text(source.kind, 'unknown');
        const type = text(definition.id, kind);
        const state = text(source.state, 'ready');
        const genericSections = [
            Object.freeze({
                id: 'identity', title: '节点',
                fields: Object.freeze([field('type', '类型', type), field('state', '状态', state)]),
            }),
            Object.freeze({
                id: 'geometry', title: '画布',
                fields: Object.freeze([
                    field('position', '位置', `${coordinate(position.x)}, ${coordinate(position.y)}`),
                    field('size', '尺寸', `${coordinate(size.width)} × ${coordinate(size.height)}`),
                ]),
            }),
        ];
        return Object.freeze({
            nodeId: text(source.id, ''),
            title,
            sections: Object.freeze([...genericSections, statusSection(source), versionSection(source), referencesSection(source, context), ...registeredSections(source)]),
        });
    }

    global.WorkbenchNodeInspector = Object.freeze({registerSectionProvider, selectionViewModel, viewModel});
}(window));
