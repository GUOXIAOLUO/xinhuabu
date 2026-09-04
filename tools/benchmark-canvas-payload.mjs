#!/usr/bin/env node

const counts = [100, 300];

function makeNode(index) {
  return {
    id: `benchmark-node-${index}`,
    type: "image",
    x: (index % 20) * 240,
    y: Math.floor(index / 20) * 180,
    url: "",
    name: `Benchmark node ${index}`,
  };
}

function makeCanvas(count) {
  return {
    id: `benchmark-${count}`,
    title: `Benchmark ${count}`,
    icon: "layers",
    kind: "classic",
    project: "benchmark",
    created_at: 0,
    updated_at: 0,
    nodes: Array.from({ length: count }, (_, index) => makeNode(index)),
    connections: [],
    viewport: { x: 0, y: 0, scale: 1 },
    logs: [],
    settings: {},
  };
}

for (const count of counts) {
  const startedAt = performance.now();
  const serialized = JSON.stringify(makeCanvas(count));
  const elapsedMs = performance.now() - startedAt;
  const bytes = Buffer.byteLength(serialized, "utf8");
  process.stdout.write(`${count} nodes: ${bytes} bytes, ${elapsedMs.toFixed(3)} ms serialize\n`);
}

process.stdout.write("This measures deterministic payload construction and serialization only; browser render, pan, zoom, and minimap measurements remain manual Phase 0 checks.\n");
