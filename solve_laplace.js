"use strict";

const X0 = 1.0;
const X1 = 40.0;
const Y0 = 0.0;
const Y1 = 40.0;
const H = 0.5;
const K = 0.5;
const OMEGA = 1.92;
const TOL = 1e-12;
const MAX_SWEEPS = 20000;

function exact(x, y) {
  return Math.log(x * x + y * y);
}

function createLaplaceStepper() {
  const nx = Math.round((X1 - X0) / H) + 1;
  const ny = Math.round((Y1 - Y0) / K) + 1;
  const values = new Float64Array(nx * ny);
  const index = (i, j) => j * nx + i;
  const xAt = (i) => X0 + i * H;
  const yAt = (j) => Y0 + j * K;

  for (let j = 0; j < ny; j += 1) {
    values[index(0, j)] = Math.log(1 + yAt(j) ** 2);
    values[index(nx - 1, j)] = Math.log(1600 + yAt(j) ** 2);
  }
  for (let i = 0; i < nx; i += 1) {
    values[index(i, 0)] = 2 * Math.log(xAt(i));
    values[index(i, ny - 1)] = Math.log(xAt(i) ** 2 + 1600);
  }

  let sweeps = 0;
  let maxUpdate = Infinity;
  function step(maxSteps = 1) {
    let completed = 0;
    while (completed < maxSteps && sweeps < MAX_SWEEPS && maxUpdate >= TOL) {
      maxUpdate = 0;
      for (let color = 0; color <= 1; color += 1) {
        for (let j = 1; j < ny - 1; j += 1) {
          for (let i = 1; i < nx - 1; i += 1) {
            if (((i + j) & 1) !== color) continue;
            const p = index(i, j);
            const average = 0.25 * (
              values[p - 1] + values[p + 1] +
              values[p - nx] + values[p + nx]
            );
            const next = values[p] + OMEGA * (average - values[p]);
            const change = Math.abs(next - values[p]);
            if (change > maxUpdate) maxUpdate = change;
            values[p] = next;
          }
        }
      }
      sweeps += 1;
      completed += 1;
    }
    return { sweeps, maxUpdate, done: sweeps >= MAX_SWEEPS || maxUpdate < TOL };
  }

  return { nx, ny, values, xAt, yAt, step, get sweeps() { return sweeps; }, get maxUpdate() { return maxUpdate; } };
}

function solveLaplace() {
  const stepper = createLaplaceStepper();
  let progress = stepper.step(MAX_SWEEPS);
  const { nx, ny, values, xAt, yAt } = stepper;
  const sweeps = progress.sweeps;
  const maxUpdate = progress.maxUpdate;
  const index = (i, j) => j * nx + i;

  let maxResidual = 0;
  let maxError = 0;
  let sumError = 0;
  let sumSquaredError = 0;
  let maxErrorI = 0;
  let maxErrorJ = 0;
  let minTemperature = Infinity;
  let maxTemperature = -Infinity;

  for (let j = 0; j < ny; j += 1) {
    for (let i = 0; i < nx; i += 1) {
      const value = values[index(i, j)];
      minTemperature = Math.min(minTemperature, value);
      maxTemperature = Math.max(maxTemperature, value);
      if (i === 0 || i === nx - 1 || j === 0 || j === ny - 1) continue;

      const p = index(i, j);
      const residual = Math.abs(
        4 * values[p] - values[p - 1] - values[p + 1] -
        values[p - nx] - values[p + nx]
      );
      maxResidual = Math.max(maxResidual, residual);

      const error = Math.abs(values[p] - exact(xAt(i), yAt(j)));
      sumError += error;
      sumSquaredError += error * error;
      if (error > maxError) {
        maxError = error;
        maxErrorI = i;
        maxErrorJ = j;
      }
    }
  }

  const interiorUnknowns = (nx - 2) * (ny - 2);
  const metrics = {
    nx,
    ny,
    interiorUnknowns,
    sweeps,
    omega: OMEGA,
    maxUpdate,
    maxResidual,
    maxAbsError: maxError,
    meanAbsError: sumError / interiorUnknowns,
    rmse: Math.sqrt(sumSquaredError / interiorUnknowns),
    maxErrorX: xAt(maxErrorI),
    maxErrorY: yAt(maxErrorJ),
    minTemperature,
    maxTemperature,
  };

  const sampleCoordinates = [
    [1.5, 1.5], [2.0, 1.0], [5.0, 5.0],
    [10.0, 10.0], [20.0, 20.0], [39.5, 39.5],
  ];
  const samples = sampleCoordinates.map(([x, y]) => {
    const i = Math.round((x - X0) / H);
    const j = Math.round((y - Y0) / K);
    const numerical = values[index(i, j)];
    const analytical = exact(x, y);
    return { x, y, numerical, analytical, absoluteError: Math.abs(numerical - analytical) };
  });

  return { nx, ny, values, metrics, samples, xAt, yAt };
}

function printResults(result, calculationMs) {
  const m = result.metrics;
  console.log("Equação de Laplace — diferenças finitas e SOR (JavaScript puro)");
  console.log(`Malha: ${m.nx} × ${m.ny} nós; ${m.interiorUnknowns} incógnitas internas.`);
  console.log(`SOR: ω = ${m.omega}; ${m.sweeps} varreduras; maior atualização = ${m.maxUpdate.toExponential(3)}.`);
  console.log(`Resíduo máximo do stencil: ${m.maxResidual.toExponential(3)}.`);
  console.log(`Erro máximo: ${m.maxAbsError.toFixed(12)} em (${m.maxErrorX}, ${m.maxErrorY}).`);
  console.log(`Erro médio: ${m.meanAbsError.toFixed(12)}; RMSE: ${m.rmse.toFixed(12)}.`);
  console.log("Comparação em pontos selecionados:");
  console.table(result.samples.map((s) => ({
    x: s.x,
    y: s.y,
    "T numérica": s.numerical.toFixed(12),
    "T analítica": s.analytical.toFixed(12),
    "Erro absoluto": s.absoluteError.toExponential(3),
  })));
  console.log(`Tempo de cálculo da malha: ${calculationMs.toFixed(3)} ms (sem contar a impressão da lista).`);
  console.log("\nLISTA COMPLETA DAS TEMPERATURAS INTERNAS");
  console.log("N | x | y | T numérica | T analítica | Erro absoluto");
  let rowNumber = 0;
  for (let j = 1; j < result.ny - 1; j += 1) {
    for (let i = 1; i < result.nx - 1; i += 1) {
      rowNumber += 1;
      const x = result.xAt(i);
      const y = result.yAt(j);
      const numerical = result.values[j * result.nx + i];
      const analytical = exact(x, y);
      const error = Math.abs(numerical - analytical);
      console.log(`${String(rowNumber).padStart(4, "0")} | ${x.toFixed(1)} | ${y.toFixed(1)} | ` +
        `${numerical.toFixed(12)} | ${analytical.toFixed(12)} | ${error.toExponential(3)}`);
    }
  }
  console.log(`Resultados impressos: ${rowNumber}.`);
}

if (typeof globalThis !== "undefined") {
  globalThis.solveLaplace = solveLaplace;
  globalThis.createLaplaceStepper = createLaplaceStepper;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { solveLaplace, exact, createLaplaceStepper };
}

function clockMilliseconds() {
  return typeof performance !== "undefined" && typeof performance.now === "function"
    ? performance.now()
    : Date.now();
}

if (typeof document === "undefined") {
  const start = clockMilliseconds();
  const result = solveLaplace();
  const calculationMs = clockMilliseconds() - start;
  printResults(result, calculationMs);
}
