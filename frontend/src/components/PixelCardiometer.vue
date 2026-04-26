<script setup>
import { onMounted, onUnmounted, ref } from "vue";

const canvasRef = ref(null);
let raf = 0;
let t0 = 0;

function draw(ts) {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = "#070b12";
  ctx.fillRect(0, 0, w, h);

  const grid = 8;
  const cols = Math.floor(w / grid);
  const rows = Math.floor(h / grid);
  const beat = (ts - t0) / 1000;
  const bpm = 72;
  const phase = (beat * bpm) / 60;

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const nx = x / cols;
      const ny = y / rows;
      let v = 0;
      const cx = 0.22 + 0.08 * Math.sin(phase * Math.PI * 2);
      const cy = 0.5;
      const pulse = Math.exp(-((nx - cx) ** 2 + (ny - cy) ** 2) * 180);
      const wave = Math.sin((nx * 14 + phase * Math.PI * 2) * 1.8) * 0.12;
      const baseline = ny > 0.42 && ny < 0.58 ? 1 : 0;
      const spike =
        ny > 0.48 &&
        ny < 0.52 &&
        nx > 0.18 &&
        nx < 0.72 &&
        Math.abs(Math.sin((nx - 0.35 - (phase % 1)) * Math.PI * 6)) > 0.82
          ? 1
          : 0;
      v = Math.max(v, pulse * 0.9 + baseline * 0.08 + wave);
      v = Math.max(v, spike * 0.95);
      if (v < 0.08) continue;
      const g = Math.min(255, 40 + v * 200);
      const b = Math.min(255, 80 + v * 170);
      ctx.fillStyle = `rgb(${Math.floor(30 + v * 40)}, ${Math.floor(g)}, ${Math.floor(b)})`;
      ctx.fillRect(x * grid, y * grid, grid - 1, grid - 1);
    }
  }

  ctx.fillStyle = "rgba(94, 234, 212, 0.9)";
  ctx.font = "700 14px JetBrains Mono, monospace";
  ctx.fillText(`${bpm} BPM`, 16, 26);
  ctx.fillStyle = "rgba(139, 163, 199, 0.9)";
  ctx.font = "500 11px Outfit, sans-serif";
  ctx.fillText("PIXEL CARDIO · DÉMO VISUELLE", 16, h - 14);

  raf = requestAnimationFrame(draw);
}

onMounted(() => {
  t0 = performance.now();
  raf = requestAnimationFrame(draw);
});

onUnmounted(() => cancelAnimationFrame(raf));
</script>

<template>
  <div class="wrap">
    <canvas ref="canvasRef" width="640" height="220" class="canvas" />
  </div>
</template>

<style scoped>
.wrap {
  border-radius: var(--radius);
  overflow: hidden;
  border: 2px solid var(--border);
  box-shadow: 0 0 40px rgba(94, 234, 212, 0.12), var(--shadow);
  background: #070b12;
}

.canvas {
  display: block;
  width: 100%;
  height: auto;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
</style>
