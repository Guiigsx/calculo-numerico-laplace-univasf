from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"
SOURCE = ROOT / "solve_laplace.js"
LOGO = ROOT / "univasf.png"

TEMPLATE = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0289e0">
  <meta name="description" content="Demonstração acadêmica da solução numérica da equação de Laplace por diferenças finitas e SOR.">
  <title>Equação de Laplace | UNIVASF · Cálculo Numérico</title>
  <style>
    :root {
      color-scheme: light;
      --blue: #0289e0;
      --gold: #f9ac03;
      --navy: #17324d;
      --ink: #263746;
      --muted: #657584;
      --line: #dce5eb;
      --paper: #ffffff;
      --page: #f3f6f8;
      --pale-blue: #edf7fd;
      --shadow: 0 12px 34px rgba(23, 50, 77, .08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(ellipse at 92% 0%, rgba(2,137,224,.08), transparent 28rem),
        var(--page);
      font: 15px/1.58 "Segoe UI", Arial, sans-serif;
    }
    main { width: min(1160px, calc(100% - 40px)); margin: 28px auto 56px; }
    .masthead, .hero, .panel, .results-block, .data-panel {
      background: var(--paper); border: 1px solid var(--line); border-radius: 16px; box-shadow: var(--shadow);
    }
    .masthead { position: relative; overflow: hidden; padding: 22px 28px; }
    .masthead::before { content: ""; position: absolute; inset: 0 0 auto; height: 5px; background: linear-gradient(90deg,var(--blue) 0 74%,var(--gold) 74%); }
    .brand-row { display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap; }
    .brand-lockup { display:flex; align-items:center; gap:22px; min-width:0; }
    .brand-signature { display:grid; justify-items:start; width:280px; flex:0 0 auto; }
    .brand-signature img { width:280px; max-width:100%; height:auto; display:block; }
    .signature-rule { width:100%; height:1px; margin:8px 0 5px; background:#343434; }
    .signature-unit { color:#343434; font:12px Arial,sans-serif; letter-spacing:.01em; }
    .brand-divider { width:1px; height:54px; background:var(--line); }
    .institution { display:grid; gap:3px; }
    .institution strong { color:var(--navy); font:700 14px Arial,sans-serif; letter-spacing:.025em; }
    .institution span { color:var(--muted); font-size:13px; }
    .course-tag { border-left:3px solid var(--gold); padding:5px 0 5px 13px; color:var(--navy); font-size:12px; font-weight:700; letter-spacing:.09em; text-transform:uppercase; }
    .students { display:grid; grid-template-columns:100px minmax(0,1fr); gap:12px 24px; margin-top:20px; padding-top:16px; border-top:1px solid var(--line); }
    .students h2 { margin:0; color:var(--muted); font:600 12px/1.58 "Segoe UI",Arial,sans-serif; letter-spacing:.08em; text-transform:uppercase; }
    .student-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px 28px; margin:0; padding:0; list-style:none; color:var(--navy); font-size:14px; font-weight:500; }
    .student-list li { min-width:0; overflow-wrap:anywhere; }
    .hero { margin-top:18px; padding:34px 38px 32px; color:white; border:0; background:linear-gradient(116deg,#17324d 0%,#1c527b 72%,#17679b 100%); position:relative; overflow:hidden; }
    .hero::after { content:""; position:absolute; right:-92px; top:-155px; width:360px; height:360px; border:1px solid rgba(255,255,255,.14); border-radius:50%; box-shadow:0 0 0 34px rgba(255,255,255,.035),0 0 0 70px rgba(255,255,255,.025); pointer-events:none; }
    .eyebrow { position:relative; z-index:1; display:flex; align-items:center; gap:9px; color:#cae8f8; font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }
    .sun-dot { width:8px; height:8px; border-radius:50%; background:var(--gold); box-shadow:0 0 0 4px rgba(249,172,3,.16); }
    h1 { position:relative; z-index:1; margin:9px 0 8px; max-width:800px; font:600 clamp(27px,4vw,42px)/1.16 Georgia,"Times New Roman",serif; letter-spacing:-.02em; }
    .hero-meta { position:relative; z-index:1; display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-top:23px; }
    .equation-display { position:relative; z-index:1; display:inline-block; margin-top:21px; padding:12px 22px; border:1px solid rgba(255,255,255,.24); border-radius:10px; background:rgba(255,255,255,.08); }
    .equation-display math, .equation-display math * { color:white; font-family:"Segoe UI",Arial,sans-serif; font-size:clamp(23px,3vw,30px); }
    .method-chip { border:1px solid rgba(255,255,255,.18); border-radius:999px; padding:7px 12px; color:#f5f8fa; font-size:12px; }
    .control-row { display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin:21px 0 16px; }
    .animation-controls { margin:12px 0 10px; }
    .sor-progress { display:block; width:100%; height:8px; margin:0 0 12px; accent-color:var(--blue); }
    button { border:0; border-radius:9px; padding:12px 18px; color:white; background:var(--blue); font:700 14px "Segoe UI",Arial,sans-serif; cursor:pointer; transition:transform .15s ease,filter .15s ease,box-shadow .15s ease; box-shadow:0 6px 15px rgba(2,137,224,.2); }
    button:hover { filter:brightness(.94); transform:translateY(-1px); }
    button:disabled { opacity:.66; cursor:wait; transform:none; }
    #status { color:var(--muted); font-size:14px; }
    #results[hidden] { display:none; }
    .section-head { display:flex; align-items:end; justify-content:space-between; gap:18px; margin:30px 2px 14px; }
    .section-head h2 { margin:0; color:var(--navy); font:600 25px/1.2 Georgia,"Times New Roman",serif; }
    .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(165px,1fr)); gap:12px; }
    .card { position:relative; overflow:hidden; min-height:100px; padding:15px 16px; background:white; border:1px solid var(--line); border-radius:12px; }
    .card::before { content:""; position:absolute; inset:0 auto 0 0; width:3px; background:var(--blue); }
    .card:nth-child(3n)::before { background:var(--gold); }
    .card span { display:block; color:var(--muted); font-size:12px; }
    .card strong { display:block; margin-top:7px; color:var(--navy); font:600 19px/1.2 "Segoe UI",Arial,sans-serif; font-variant-numeric:tabular-nums; overflow-wrap:anywhere; }
    .grid-panels { display:grid; grid-template-columns:1fr; gap:16px; }
    .panel { padding:19px 20px 16px; }
    .convergence-panel { margin-top:16px; }
    .panel-title { display:flex; justify-content:space-between; align-items:flex-start; gap:18px; margin:0 0 13px; }
    .panel-title h3 { margin:0; color:var(--navy); font-size:16px; }
    .panel-kicker { white-space:nowrap; padding:5px 9px; background:var(--pale-blue); color:#14608d; border-radius:999px; font-size:11px; font-weight:700; }
    canvas.chart { display:block; width:100%; height:auto; border:1px solid #e1e8ed; border-radius:10px; background:#fff; }
    .point-map-panel { margin-top:16px; }
    .point-readout { display:flex; align-items:center; flex-wrap:wrap; gap:7px 18px; min-height:48px; margin:0 0 12px; padding:10px 13px; border-left:3px solid var(--blue); border-radius:8px; background:var(--pale-blue); color:var(--ink); font-size:13px; font-variant-numeric:tabular-nums; }
    .point-readout strong { color:var(--navy); }
    .point-tooltip { position:fixed; z-index:100; width:min(290px,calc(100vw - 24px)); padding:12px 14px; border:1px solid var(--line); border-radius:10px; background:var(--paper); box-shadow:0 10px 26px rgba(23,50,77,.2); color:var(--ink); font-size:12px; line-height:1.45; font-variant-numeric:tabular-nums; pointer-events:none; }
    .point-tooltip[hidden] { display:none; }
    .point-tooltip-title { margin-bottom:7px; color:var(--navy); font-size:13px; font-weight:700; }
    .point-tooltip-row { display:flex; justify-content:space-between; gap:12px; margin-top:3px; }
    .point-tooltip-label { color:var(--muted); }
    .point-tooltip-value { color:var(--ink); font-weight:600; text-align:right; }
    .grid-scroll { max-width:100%; overflow:auto; border:1px solid var(--line); border-radius:10px; background:#fff; }
    canvas.chart.interactive-grid { width:1000px; max-width:none; border:0; border-radius:0; cursor:crosshair; }
    .results-block { margin-top:16px; padding:19px 20px; }
    .table-wrap { overflow:auto; border:1px solid var(--line); border-radius:10px; background:white; }
    table { width:100%; border-collapse:collapse; min-width:650px; }
    th,td { padding:10px 12px; border-bottom:1px solid #e8edf1; text-align:right; font-variant-numeric:tabular-nums; }
    th { background:#eaf5fc; color:var(--navy); font-size:12px; letter-spacing:.02em; }
    th:first-child,td:first-child { text-align:center; }
    tbody tr:nth-child(even) { background:#f8fafb; }
    details.data-panel { margin-top:16px; padding:0; overflow:hidden; }
    details.data-panel summary { display:flex; align-items:center; justify-content:space-between; gap:14px; padding:17px 20px; color:var(--navy); font-weight:700; cursor:pointer; list-style:none; }
    details.data-panel summary::-webkit-details-marker { display:none; }
    details.data-panel summary::after { content:"＋"; color:var(--blue); font-size:19px; }
    details.data-panel[open] summary::after { content:"−"; }
    .details-body { padding:0 20px 20px; }
    .results-scroll { max-height:460px; overflow:auto; border:1px solid var(--line); border-radius:9px; background:#f7f9fb; }
    pre { margin:0; padding:14px; white-space:pre; overflow:auto; font:12px/1.55 Consolas,"Courier New",monospace; }
    #source { max-height:460px; }
    .small-button { margin:0 0 12px; padding:9px 13px; font-size:12px; box-shadow:none; }
    @media (max-width:700px) {
      main { width:calc(100% - 22px); margin:12px auto 30px; }
      .masthead { padding:19px 18px; }
      .brand-lockup { gap:14px; flex-wrap:wrap; }
      .brand-signature { width:min(240px,64vw); }
      .brand-signature img { width:100%; }
      .signature-unit { font-size:11px; }
      .brand-divider { display:none; }
      .institution strong { font-size:11px; }
      .institution span { font-size:11px; }
      .students { grid-template-columns:1fr; gap:8px; }
      .student-list { grid-template-columns:1fr; }
      .hero { padding:25px 22px; }
      .section-head { align-items:flex-start; flex-direction:column; }
      .panel { padding:14px; }
      .panel-title { flex-direction:column; gap:7px; }
      .panel-kicker { white-space:normal; }
    }
  </style>
</head>
<body>
<main>
  <header class="masthead">
    <div class="brand-row">
      <div class="brand-lockup">
        <div class="brand-signature">
          <img src="{{LOGO_DATA_URI}}" alt="Marca oficial da Universidade Federal do Vale do São Francisco">
          <span class="signature-rule" aria-hidden="true"></span>
          <span class="signature-unit">MATM0048 — Cálculo Numérico</span>
        </div>
        <span class="brand-divider" aria-hidden="true"></span>
        <div class="institution">
          <strong>UNIVERSIDADE FEDERAL DO VALE DO SÃO FRANCISCO</strong>
          <span>Prof. Sergio Floquet</span>
          <span>Colegiados CCIVIL, CENEL, CPROD e CENMEC</span>
        </div>
      </div>
      <div class="course-tag">Demonstração<br>acadêmica interativa</div>
    </div>
    <div class="students" aria-labelledby="students-title">
      <h2 id="students-title">Discentes</h2>
      <ul class="student-list">
        <li>Cecília Moura Reis Frota</li>
        <li>Guilherme Hilário Schmitz da Silva</li>
        <li>Guilherme Torres de Miranda</li>
        <li>Luiz Felipe Monte de Oliveira</li>
      </ul>
    </div>
  </header>

  <section class="hero" aria-labelledby="page-title">
    <div class="eyebrow"><span class="sun-dot"></span> Equações diferenciais parciais</div>
    <h1 id="page-title">Equação de Laplace em uma placa</h1>
    <div class="equation-display" aria-label="Equação diferencial de Laplace">
      <math display="block" aria-label="Derivada parcial segunda de T em relação a x, mais derivada parcial segunda de T em relação a y, igual a zero">
        <mrow>
          <mfrac>
            <mrow><msup><mo>∂</mo><mn>2</mn></msup><mi>T</mi></mrow>
            <mrow><mo>∂</mo><msup><mi>x</mi><mn>2</mn></msup></mrow>
          </mfrac>
          <mo>+</mo>
          <mfrac>
            <mrow><msup><mo>∂</mo><mn>2</mn></msup><mi>T</mi></mrow>
            <mrow><mo>∂</mo><msup><mi>y</mi><mn>2</mn></msup></mrow>
          </mfrac>
          <mo>=</mo><mn>0</mn>
        </mrow>
      </math>
    </div>
    <div class="hero-meta">
      <span class="method-chip">h = k = 0,5</span>
      <span class="method-chip">Sobrerrelaxação sucessiva · SOR</span>
    </div>
  </section>

  <div class="control-row">
    <button id="run" type="button">Executar cálculo</button>
    <span id="status" role="status" aria-live="polite">Pronto para calcular no navegador.</span>
  </div>
  <section id="results" hidden aria-live="polite">
    <div class="section-head">
      <h2>Resultados da execução</h2>
    </div>
    <div class="cards" id="cards"></div>

    <section class="panel convergence-panel" aria-labelledby="convergence-title">
      <div class="panel-title"><div><h3 id="convergence-title">Evolução das temperaturas durante o cálculo</h3></div><span class="panel-kicker">Convergência SOR</span></div>
      <div class="control-row animation-controls">
        <button id="playConvergence" type="button">Reproduzir animação</button>
        <span id="convergenceStatus" role="status" aria-live="polite">Execute o cálculo para preparar a visualização.</span>
      </div>
      <progress class="sor-progress" id="sorProgress" value="0" max="479" aria-label="Progresso das varreduras SOR">0%</progress>
      <canvas id="convergenceMap" class="chart" width="1000" height="500" aria-label="Animação da temperatura na malha ao longo das varreduras do método SOR"></canvas>
    </section>

    <div class="section-head"><h2>Visualização da solução</h2></div>
    <div class="grid-panels">
      <article class="panel">
        <div class="panel-title"><div><h3>Superfície tridimensional</h3></div><span class="panel-kicker">Perspectiva isométrica</span></div>
        <canvas id="surface" class="chart" width="1000" height="500" aria-label="Superfície tridimensional da temperatura, com os quatro cantos da placa identificados"></canvas>
      </article>
      <article class="panel">
        <div class="panel-title"><div><h3>Mapa de temperatura</h3></div><span class="panel-kicker">Escala contínua</span></div>
        <canvas id="heatmap" class="chart" width="1000" height="500" aria-label="Mapa de calor da temperatura na placa, com eixos x e y"></canvas>
      </article>
    </div>

    <section class="panel point-map-panel" aria-labelledby="point-map-title">
      <div class="panel-title"><div><h3 id="point-map-title">Planta interativa da malha</h3></div><span class="panel-kicker">79 × 81 pontos</span></div>
      <div id="selectedPointInfo" class="point-readout" role="status" aria-live="polite">Selecione um quadrado para consultar suas coordenadas e temperaturas; com o foco na planta, use as setas do teclado para percorrer os pontos.</div>
      <div class="grid-scroll"><canvas id="pointMap" class="chart interactive-grid" width="1000" height="900" tabindex="0" aria-label="Planta interativa da malha. Clique em um ponto ou use as setas do teclado para selecioná-lo."></canvas></div>
    </section>

    <section class="results-block">
      <div class="section-head"><h2>Comparação pontual</h2></div>
      <div class="table-wrap"><table>
        <thead><tr><th>x</th><th>y</th><th>T numérica</th><th>T analítica</th><th>Erro absoluto</th></tr></thead>
        <tbody id="samples"></tbody>
      </table></div>
    </section>

    <details class="data-panel">
      <summary>Lista completa das 6.083 temperaturas internas</summary>
      <div class="details-body">
        <button class="small-button" id="downloadCsv" type="button">Baixar resultados em CSV</button>
        <div class="results-scroll"><pre id="allRows"></pre></div>
      </div>
    </details>
    <details class="data-panel">
      <summary>Ver o código JavaScript puro</summary>
      <div class="details-body"><div class="results-scroll"><pre id="source"></pre></div></div>
    </details>
  </section>

</main>
<div id="pointTooltip" class="point-tooltip" hidden aria-hidden="true"></div>

{{SOLVER_SCRIPT}}
<script>
"use strict";
const sourceText = {{SOURCE_JSON}};
const button = document.getElementById("run");
const statusLine = document.getElementById("status");
const resultPanel = document.getElementById("results");
let lastSolutionResult = null;
const pointMapCanvas = document.getElementById("pointMap");
const pointInfo = document.getElementById("selectedPointInfo");
const pointTooltip = document.getElementById("pointTooltip");
let pointMapResult = null;
let selectedGridPoint = null;
document.getElementById("source").textContent = sourceText;

function fmt(value, digits=6) {
  return Number(value).toLocaleString("pt-BR", {minimumFractionDigits:digits, maximumFractionDigits:digits});
}
function expfmt(value) { return Number(value).toExponential(3).replace(".", ","); }
function sciHtml(value) {
  const [coefficient, exponentText] = Number(value).toExponential(2).split("e");
  const exponent = Number(exponentText);
  const sign = exponent < 0 ? "−" : "";
  return `${coefficient.replace(".", ",")} × 10<sup>${sign}${Math.abs(exponent)}</sup>`;
}

function showMetrics(result, calculationMs, listPreparationMs) {
  const m = result.metrics;
  const cards = [
    ["Pontos da malha", `${m.nx} × ${m.ny}`],
    ["Pontos internos calculados", m.interiorUnknowns.toLocaleString("pt-BR")],
    ["Varreduras SOR", m.sweeps.toLocaleString("pt-BR")],
    ["Resíduo máximo", sciHtml(m.maxResidual)],
    ["Erro máximo", fmt(m.maxAbsError, 6)],
    ["Erro absoluto médio", fmt(m.meanAbsError, 6)],
    ["RMSE", fmt(m.rmse, 6)],
    ["Ponto de erro máximo", `(${fmt(m.maxErrorX,1)}; ${fmt(m.maxErrorY,1)})`],
    ["Tempo de cálculo", `${fmt(calculationMs,2)} ms`],
    ["Preparação da lista", `${fmt(listPreparationMs,2)} ms`],
  ];
  document.getElementById("cards").innerHTML = cards.map(([label,value]) =>
    `<div class="card"><span>${label}</span><strong>${value}</strong></div>`).join("");
  document.getElementById("samples").innerHTML = result.samples.map(s =>
    `<tr><td>${fmt(s.x,1)}</td><td>${fmt(s.y,1)}</td><td>${fmt(s.numerical,12)}</td><td>${fmt(s.analytical,12)}</td><td>${expfmt(s.absoluteError)}</td></tr>`).join("");
}

let csvContent = "";
function prepareFullList(result) {
  const lines = ["N | i | j | x | y | T numerica | T analitica | erro absoluto"];
  const csvLines = ["N;i;j;x;y;T_numerica;T_analitica;erro_absoluto"];
  let n = 0;
  for(let j=1;j<result.ny-1;j++) for(let i=1;i<result.nx-1;i++) {
    n++;
    const x=result.xAt(i), y=result.yAt(j), numerical=result.values[j*result.nx+i];
    const analytical=Math.log(x*x+y*y), error=Math.abs(numerical-analytical);
    lines.push(`${String(n).padStart(4,"0")} | ${i} | ${j} | ${fmt(x,1)} | ${fmt(y,1)} | ${fmt(numerical,12)} | ${fmt(analytical,12)} | ${expfmt(error)}`);
    csvLines.push(`${n};${i};${j};${x.toFixed(1)};${y.toFixed(1)};${numerical.toFixed(12)};${analytical.toFixed(12)};${error.toExponential(12)}`);
  }
  csvContent=csvLines.join("\n");
  document.getElementById("allRows").textContent=lines.join("\n");
  return n;
}

const colorStops = [
  [249,172,3], [50,177,207], [2,137,224], [20,58,94]
];
function colorAt(t) {
  const p = Math.max(0,Math.min(1,t)) * (colorStops.length-1);
  const a = Math.floor(p), b = Math.min(a+1,colorStops.length-1), f = p-a;
  const c = colorStops[a].map((v,i) => Math.round(v*(1-f)+colorStops[b][i]*f));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function drawHeatmap(result, canvasId="heatmap", annotation="") {
  const canvas = document.getElementById(canvasId), ctx = canvas.getContext("2d");
  const {nx,ny,values,metrics:m} = result;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const plot = {x:92,y:30,w:790,h:390};
  const cw=plot.w/nx, ch=plot.h/ny;
  for(let j=0;j<ny;j++) for(let i=0;i<nx;i++) {
    const t=(values[j*nx+i]-m.minTemperature)/(m.maxTemperature-m.minTemperature);
    ctx.fillStyle=colorAt(t);
    ctx.fillRect(plot.x+i*cw,plot.y+(ny-1-j)*ch,cw+0.5,ch+0.5);
  }
  ctx.strokeStyle="#24313d"; ctx.lineWidth=1.5; ctx.strokeRect(plot.x,plot.y,plot.w,plot.h);
  ctx.fillStyle="#263746"; ctx.font="15px Segoe UI, Arial"; ctx.textAlign="center";
  ctx.fillText("x",plot.x+plot.w/2,465);
  ctx.save(); ctx.translate(26,plot.y+plot.h/2); ctx.rotate(-Math.PI/2); ctx.fillText("y",0,0); ctx.restore();
  const xTicks=[1,10,20,30,40], yTicks=[0,10,20,30,40];
  ctx.textAlign="center";
  for(const tick of xTicks) {
    const x=plot.x+(tick-1)/(40-1)*plot.w;
    ctx.strokeStyle="rgba(255,255,255,.42)"; ctx.lineWidth=.7;
    ctx.beginPath(); ctx.moveTo(x,plot.y); ctx.lineTo(x,plot.y+plot.h); ctx.stroke();
    ctx.fillStyle="#263746"; ctx.fillText(String(tick),x,442);
  }
  for(const tick of yTicks) {
    const y=plot.y+(40-tick)/40*plot.h;
    ctx.strokeStyle="rgba(255,255,255,.42)"; ctx.lineWidth=.7;
    ctx.beginPath(); ctx.moveTo(plot.x,y); ctx.lineTo(plot.x+plot.w,y); ctx.stroke();
    ctx.fillStyle="#263746"; ctx.textAlign="right"; ctx.fillText(String(tick),plot.x-10,y+5);
  }
  const grad=ctx.createLinearGradient(0,plot.y,0,plot.y+plot.h);
  colorStops.forEach((_,i)=>grad.addColorStop(i/(colorStops.length-1),colorAt(1-i/(colorStops.length-1))));
  ctx.fillStyle=grad; ctx.fillRect(915,plot.y,24,plot.h); ctx.strokeStyle="#53616d"; ctx.strokeRect(915,plot.y,24,plot.h);
  ctx.fillStyle="#263746"; ctx.textAlign="left"; ctx.fillText(fmt(m.maxTemperature,2),946,plot.y+6); ctx.fillText(fmt(m.minTemperature,2),946,plot.y+plot.h);
  ctx.font="11px Segoe UI,Arial"; ctx.fillText("mais quente",946,plot.y-9); ctx.fillText("mais fria",946,plot.y+plot.h+18);
  if(annotation) { ctx.font="13px Segoe UI,Arial"; ctx.fillStyle="#17324d"; ctx.textAlign="left"; ctx.fillText(annotation,plot.x,19); }
}
function drawInteractiveMap(result) {
  const ctx=pointMapCanvas.getContext("2d"), {nx,ny,values,metrics:m}=result;
  const grid={x:85,y:35,cell:8,gap:2,pitch:10};
  const width=(nx-1)*grid.pitch+grid.cell, height=(ny-1)*grid.pitch+grid.cell;
  ctx.clearRect(0,0,pointMapCanvas.width,pointMapCanvas.height);
  for(let row=0;row<ny;row++) for(let i=0;i<nx;i++) {
    const j=ny-1-row, x=grid.x+i*grid.pitch, y=grid.y+row*grid.pitch;
    const value=values[j*nx+i], t=(value-m.minTemperature)/(m.maxTemperature-m.minTemperature);
    ctx.fillStyle=colorAt(t); ctx.fillRect(x,y,grid.cell,grid.cell);
    if(selectedGridPoint && selectedGridPoint.i===i && selectedGridPoint.j===j) {
      ctx.strokeStyle="#17324d"; ctx.lineWidth=2; ctx.strokeRect(x-1,y-1,grid.cell+2,grid.cell+2);
    }
  }

  ctx.fillStyle="#263746"; ctx.font="13px Segoe UI,Arial"; ctx.textAlign="center";
  for(const tick of [1,10,20,30,40]) {
    const i=Math.round((tick-1)/H), x=grid.x+i*grid.pitch+grid.cell/2;
    ctx.fillText(String(tick),x,grid.y+height+22);
  }
  for(const tick of [0,10,20,30,40]) {
    const j=Math.round(tick/K), row=ny-1-j, y=grid.y+row*grid.pitch+grid.cell/2;
    ctx.textAlign="right"; ctx.fillText(String(tick),grid.x-12,y+4);
  }
  ctx.textAlign="center"; ctx.fillText("x",grid.x+width/2,grid.y+height+46);
  ctx.save(); ctx.translate(22,grid.y+height/2); ctx.rotate(-Math.PI/2); ctx.fillText("y",0,0); ctx.restore();

  const legendX=895, legendY=grid.y, legendW=18, legendH=height;
  const gradient=ctx.createLinearGradient(0,legendY,0,legendY+legendH);
  colorStops.forEach((_,i)=>gradient.addColorStop(i/(colorStops.length-1),colorAt(1-i/(colorStops.length-1))));
  ctx.fillStyle=gradient; ctx.fillRect(legendX,legendY,legendW,legendH);
  ctx.fillStyle="#263746"; ctx.font="12px Segoe UI,Arial"; ctx.textAlign="left";
  ctx.fillText(fmt(m.maxTemperature,2),legendX+25,legendY+5);
  ctx.fillText(fmt(m.minTemperature,2),legendX+25,legendY+legendH);
  ctx.font="11px Segoe UI,Arial"; ctx.fillText("mais quente",legendX+25,legendY-9); ctx.fillText("mais fria",legendX+25,legendY+legendH+18);
}
function selectGridPoint(i,j,anchor=null) {
  if(!pointMapResult) return;
  selectedGridPoint={i,j};
  const {nx,values,xAt,yAt}=pointMapResult;
  const x=xAt(i), y=yAt(j), numerical=values[j*nx+i], analytical=exact(x,y);
  const error=Math.abs(numerical-analytical);
  const onBoundary=i===0 || i===nx-1 || j===0 || j===pointMapResult.ny-1;
  pointInfo.innerHTML=`<strong>Ponto (${fmt(x,1)}; ${fmt(y,1)})</strong><span>${onBoundary?"Borda":"Interior"}</span><span><b>T numérica:</b> ${fmt(numerical,8)}</span><span><b>T analítica:</b> ${fmt(analytical,8)}</span><span><b>Erro absoluto:</b> ${fmt(error,9)}</span>`;
  pointMapCanvas.setAttribute("aria-label",`Ponto selecionado: x ${fmt(x,1)}, y ${fmt(y,1)}; ${onBoundary?"borda":"interior"}; temperatura numérica ${fmt(numerical,8)}; temperatura analítica ${fmt(analytical,8)}; erro ${fmt(error,9)}. Use as setas para percorrer os pontos.`);
  pointTooltip.innerHTML=`<div class="point-tooltip-title">Ponto (${fmt(x,1)}; ${fmt(y,1)}) · ${onBoundary?"Borda":"Interior"}</div><div class="point-tooltip-row"><span class="point-tooltip-label">T numérica</span><span class="point-tooltip-value">${fmt(numerical,8)}</span></div><div class="point-tooltip-row"><span class="point-tooltip-label">T analítica</span><span class="point-tooltip-value">${fmt(analytical,8)}</span></div><div class="point-tooltip-row"><span class="point-tooltip-label">Erro absoluto</span><span class="point-tooltip-value">${fmt(error,9)}</span></div>`;
  pointTooltip.hidden=false;
  if(!anchor) {
    const rect=pointMapCanvas.getBoundingClientRect(), row=pointMapResult.ny-1-j;
    anchor={
      x:rect.left+(85+i*10+4)*rect.width/pointMapCanvas.width,
      y:rect.top+(35+row*10+4)*rect.height/pointMapCanvas.height,
    };
  }
  let left=anchor.x+14, top=anchor.y+14;
  const tooltipWidth=pointTooltip.offsetWidth, tooltipHeight=pointTooltip.offsetHeight;
  if(left+tooltipWidth>window.innerWidth-8) left=anchor.x-tooltipWidth-14;
  if(top+tooltipHeight>window.innerHeight-8) top=anchor.y-tooltipHeight-14;
  pointTooltip.style.left=`${Math.max(8,Math.min(left,window.innerWidth-tooltipWidth-8))}px`;
  pointTooltip.style.top=`${Math.max(8,Math.min(top,window.innerHeight-tooltipHeight-8))}px`;
  drawInteractiveMap(pointMapResult);
}
function gridPointAtPointer(event) {
  if(!pointMapResult) return null;
  const rect=pointMapCanvas.getBoundingClientRect();
  const px=(event.clientX-rect.left)*pointMapCanvas.width/rect.width;
  const py=(event.clientY-rect.top)*pointMapCanvas.height/rect.height;
  const grid={x:85,y:35,cell:8,gap:2,pitch:10};
  const {nx,ny}=pointMapResult;
  const maxX=grid.x+(nx-1)*grid.pitch+grid.cell, maxY=grid.y+(ny-1)*grid.pitch+grid.cell;
  if(px<grid.x-grid.gap/2 || px>maxX+grid.gap/2 || py<grid.y-grid.gap/2 || py>maxY+grid.gap/2) return null;
  const i=Math.max(0,Math.min(nx-1,Math.round((px-grid.x-grid.cell/2)/grid.pitch)));
  const row=Math.max(0,Math.min(ny-1,Math.round((py-grid.y-grid.cell/2)/grid.pitch)));
  return {i,j:ny-1-row};
}
pointMapCanvas.addEventListener("click",event=>{
  const point=gridPointAtPointer(event);
  if(point) selectGridPoint(point.i,point.j,{x:event.clientX,y:event.clientY});
  else pointTooltip.hidden=true;
});
pointMapCanvas.addEventListener("keydown",event=>{
  if(!pointMapResult) return;
  const {nx,ny}=pointMapResult;
  const current=selectedGridPoint||{i:Math.floor(nx/2),j:Math.floor(ny/2)};
  let i=current.i,j=current.j;
  if(event.key==="ArrowRight") i=Math.min(nx-1,i+1);
  else if(event.key==="ArrowLeft") i=Math.max(0,i-1);
  else if(event.key==="ArrowUp") j=Math.min(ny-1,j+1);
  else if(event.key==="ArrowDown") j=Math.max(0,j-1);
  else return;
  event.preventDefault(); selectGridPoint(i,j);
});
document.addEventListener("pointerdown",event=>{
  if(!pointMapCanvas.contains(event.target)) pointTooltip.hidden=true;
});
window.addEventListener("scroll",()=>{ pointTooltip.hidden=true; },true);
window.addEventListener("resize",()=>{ pointTooltip.hidden=true; });
function drawSurface(result) {
  const canvas=document.getElementById("surface"),ctx=canvas.getContext("2d");
  const {nx,ny,values,metrics:m}=result;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cx=canvas.width/2, sx=4.25, sy=1.85, sz=220, originY=100;
  function normalized(i,j) { return (values[j*nx+i]-m.minTemperature)/(m.maxTemperature-m.minTemperature); }
  function point(i,j) { return [cx+(i-j)*sx,originY+(i+j)*sy-normalized(i,j)*sz]; }
  for(let diagonal=0;diagonal<nx+ny-2;diagonal++) {
    const iMin=Math.max(0,diagonal-(ny-2)), iMax=Math.min(nx-2,diagonal);
    for(let i=iMin;i<=iMax;i++) {
      const j=diagonal-i;
      const pts=[point(i,j),point(i+1,j),point(i+1,j+1),point(i,j+1)];
      const avg=(values[j*nx+i]+values[j*nx+i+1]+values[(j+1)*nx+i+1]+values[(j+1)*nx+i])/4;
      ctx.beginPath(); ctx.moveTo(pts[0][0],pts[0][1]);
      for(let q=1;q<pts.length;q++) ctx.lineTo(pts[q][0],pts[q][1]);
      ctx.closePath(); ctx.fillStyle=colorAt((avg-m.minTemperature)/(m.maxTemperature-m.minTemperature)); ctx.fill();
      ctx.strokeStyle="rgba(255,255,255,.25)"; ctx.lineWidth=.42; ctx.stroke();
    }
  }
  function corner(i,j,label,dx,dy) {
    const p=point(i,j); ctx.beginPath(); ctx.arc(p[0],p[1],4,0,2*Math.PI); ctx.fillStyle="#17324d"; ctx.fill();
    ctx.font="bold 13px Segoe UI, Arial"; ctx.textAlign="center"; ctx.lineWidth=4; ctx.strokeStyle="rgba(255,255,255,.94)"; ctx.strokeText(label,p[0]+dx,p[1]+dy); ctx.fillStyle="#17324d"; ctx.fillText(label,p[0]+dx,p[1]+dy);
  }
  corner(0,0,"(1, 0)",0,-15);
  corner(nx-1,0,"(40, 0)",29,-2);
  corner(0,ny-1,"(1, 40)",-31,-2);
  corner(nx-1,ny-1,"(40, 40)",0,23);
  ctx.fillStyle="#263746"; ctx.font="bold 14px Segoe UI, Arial"; ctx.textAlign="center";
  ctx.fillText("Eixo x: 1 → 40",cx+206,405);
  ctx.fillText("Eixo y: 0 → 40",cx-207,405);
  ctx.fillText("T",cx+440,90);
  const grad=ctx.createLinearGradient(0,55,0,220);
  colorStops.forEach((_,i)=>grad.addColorStop(i/(colorStops.length-1),colorAt(1-i/(colorStops.length-1))));
  ctx.fillStyle=grad; ctx.fillRect(945,65,18,160); ctx.strokeStyle="#526271"; ctx.strokeRect(945,65,18,160);
  ctx.fillStyle="#263746"; ctx.font="12px Segoe UI,Arial"; ctx.textAlign="left";
  ctx.fillText(fmt(m.maxTemperature,2),970,72); ctx.fillText(fmt(m.minTemperature,2),970,225);
  ctx.font="11px Segoe UI,Arial"; ctx.fillText("mais quente",916,52); ctx.fillText("mais fria",916,246);
  ctx.save(); ctx.translate(992,150); ctx.rotate(-Math.PI/2); ctx.textAlign="center"; ctx.fillText("temperatura T",0,0); ctx.restore();
}

const playConvergenceButton=document.getElementById("playConvergence");
const convergenceStatus=document.getElementById("convergenceStatus");
const sorProgress=document.getElementById("sorProgress");
function drawConvergence(stepper,totalSweeps) {
  drawHeatmap({
    nx:stepper.nx,
    ny:stepper.ny,
    values:stepper.values,
    metrics:{minTemperature:0,maxTemperature:Math.log(3200)},
  },"convergenceMap",`Varredura SOR: ${stepper.sweeps} / ${totalSweeps}`);
}
function animateConvergence() {
  if(!lastSolutionResult) return;
  const stepper=globalThis.createLaplaceStepper();
  const totalSweeps=lastSolutionResult.metrics.sweeps;
  const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  sorProgress.max=totalSweeps; sorProgress.value=0;
  drawConvergence(stepper,totalSweeps);
  playConvergenceButton.disabled=true;
  convergenceStatus.textContent=`Execução: 0 de ${totalSweeps} varreduras.`;

  function frame() {
    const progress=stepper.step(reducedMotion?Math.ceil(totalSweeps/6):2);
    sorProgress.value=progress.sweeps;
    drawConvergence(stepper,totalSweeps);
    if(progress.done) {
      playConvergenceButton.disabled=false;
      convergenceStatus.textContent=`Concluído: ${progress.sweeps} varreduras SOR.`;
      return;
    }
    if(reducedMotion || progress.sweeps%96===0 || progress.done) convergenceStatus.textContent=`Varredura ${progress.sweeps} de ${totalSweeps}.`;
    if(reducedMotion) setTimeout(()=>requestAnimationFrame(frame),400);
    else requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
playConvergenceButton.addEventListener("click",animateConvergence);

button.addEventListener("click", () => {
  button.disabled=true; statusLine.textContent="Calculando a solução…";
  requestAnimationFrame(() => setTimeout(() => {
    try {
      const calculationStart=performance.now();
      const result=solveLaplace();
      const calculationMs=performance.now()-calculationStart;
      lastSolutionResult=result;
      const listStart=performance.now();
      const printedRows=prepareFullList(result);
      const listPreparationMs=performance.now()-listStart;
      showMetrics(result,calculationMs,listPreparationMs); drawSurface(result); drawHeatmap(result);
      pointMapResult=result; selectedGridPoint=null; drawInteractiveMap(result);
      pointMapCanvas.setAttribute("aria-label","Planta interativa com 79 por 81 pontos. Clique em um quadrado ou use as setas do teclado para consultar as temperaturas.");
      pointInfo.textContent="Selecione um quadrado para consultar suas coordenadas e temperaturas; com o foco na planta, use as setas do teclado para percorrer os pontos.";
      const initialStepper=globalThis.createLaplaceStepper();
      sorProgress.max=result.metrics.sweeps; sorProgress.value=0;
      drawConvergence(initialStepper,result.metrics.sweeps);
      convergenceStatus.textContent=`Pronto: ${result.metrics.sweeps} varreduras SOR.`;
      resultPanel.hidden=false;
      statusLine.textContent=`Concluído: ${printedRows.toLocaleString("pt-BR")} temperaturas; cálculo em ${fmt(calculationMs,2)} ms.`;
    } catch (error) {
      statusLine.textContent=`O cálculo não foi concluído: ${error.message}`;
    } finally { button.disabled=false; }
  },40));
});

document.getElementById("downloadCsv").addEventListener("click", () => {
  const blob=new Blob(["\uFEFF"+csvContent],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob), link=document.createElement("a");
  link.href=url; link.download="temperaturas_internas_6083.csv"; link.click();
  URL.revokeObjectURL(url);
});
</script>
</body>
</html>
'''


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    logo_data = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")
    page = TEMPLATE.replace("{{SOLVER_SCRIPT}}", "<script>\n" + source + "\n</script>")
    page = page.replace("{{SOURCE_JSON}}", json.dumps(source, ensure_ascii=False))
    page = page.replace("{{LOGO_DATA_URI}}", logo_data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
