# AGENTS.md — CoupledFEMSimulations

Paper 3 codebase: FEM-based virtual temperature sensor for the
press-hardening tool, with ML surrogates (RF / MLP).

## Branching

* `main` is frozen at tag `v1.0-thesis-submission`.
* All v2 work lands on `v2-publication`.

## Known issues (priority order)

1. **P0 — Hardcoded ABAQUS node indices.** `extract_temps.py` lines
   7-35 hardcode node IDs per geometry (M1 / M2 / M3) with magic
   offsets like `5208 + 344`. Externalise into
   `configs/geometry/{M1,M2,M3}.yaml`:
   ```yaml
   name: M1
   node_groups:
     Stempel:  {origin: 5208, offsets: [5, 344]}
     Matrize:  {origin: 2672, offsets: [304, 327, 397]}
     Werkstueck: {origin: 0, offsets: [8, 9, 271, 238, 569]}
   ```
   `extract_temps.py` loads the YAML and emits the same CSV columns.

2. **P0 — Canonical notebook unclear.** Multiple notebooks exist;
   designate the one that produced the published RMSE
   (1.6 ± 0.5 K) and mark the others archive-only. Convert the
   canonical notebook into `src/coupled_fem/train.py`.

3. **P1 — No CI without ABAQUS.** Ship a small synthetic FEM-style
   CSV fixture under `tests/fixtures/` so the ML pipeline can be
   tested in CI on machines without ABAQUS.

4. **P1 — Modern baselines.** Add Physics-Informed NN (Raissi et al.
   2019) and Fourier Neural Operator (Li et al. 2021) baselines on the
   same dataset.

## Conventions for v2 code

* `src/coupled_fem/` library. `extract_temps.py` stays at the repo
  root (ABAQUS calls it directly) but reads its config from YAML.
* `configs/geometry/` holds one file per tool variant.
* `make_splits()` exposes deterministic k-fold + temporal splits; the
  v1 random split is preserved for reproducibility but flagged as
  *leakage-prone for time series*.

## Reuse

* `merged/*.csv` is the canonical dataset consumed by
  `PressHardeningKnowledgeGraph` to create `Simulation` nodes. Do not
  change its column schema without bumping a version in
  `merged/README.md`.

## Do not

* Do not regenerate FEM data — it took weeks to compute and is the
  shared asset across this PhD.
* Do not edit the ABAQUS `.inp` templates without a sanity-check FEM
  run on one geometry first.
