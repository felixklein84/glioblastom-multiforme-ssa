#!/usr/bin/env python3
"""Run a single no-therapy baseline simulation.

Usage:
    python scripts/run_baseline.py
    python scripts/run_baseline.py --config configs/default.yaml --out outputs/baseline
    python scripts/run_baseline.py --seed 7
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Make package importable when running the script directly from the repo.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from gbm_ctmc.io.results import save_trajectory_csv, trajectory_to_dataframe
from gbm_ctmc.parameters import ModelParams
from gbm_ctmc.plotting.trajectory import plot_trajectory
from gbm_ctmc.simulation import run_baseline


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a GBM CTMC baseline simulation.")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "default.yaml",
        help="Path to YAML config (default: configs/default.yaml).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "outputs" / "baseline",
        help="Output directory (default: outputs/baseline).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the RNG seed from the config.",
    )
    args = parser.parse_args()

    params = ModelParams.from_yaml(args.config)
    if args.seed is not None:
        params.run.seed = args.seed

    print(f"[gbm-ctmc] Loaded config: {args.config}")
    print(f"[gbm-ctmc] Seed: {params.run.seed}  t_end: {params.run.t_end} d  K: {params.K}")
    print(f"[gbm-ctmc] Initial: S={params.initial.S} P={params.initial.P} "
          f"D={params.initial.D} Q={params.initial.Q}")

    t0 = time.perf_counter()
    traj = run_baseline(params)
    elapsed = time.perf_counter() - t0

    df = trajectory_to_dataframe(traj)
    final = df.iloc[-1]
    print(f"[gbm-ctmc] Simulation done in {elapsed:.2f} s — {len(df)} events.")
    print(f"[gbm-ctmc] Final state at t={final['time']:.1f}: "
          f"S={int(final['S'])} P={int(final['P'])} D={int(final['D'])} "
          f"Q={int(final['Q'])}  total={int(final['total'])}")

    csv_path = save_trajectory_csv(traj, args.out / "trajectory.csv")
    plot_path = plot_trajectory(
        df,
        args.out / "trajectory.png",
        title=f"GBM CTMC baseline (seed={params.run.seed}, t_end={params.run.t_end:.0f} d)",
    )
    print(f"[gbm-ctmc] CSV:  {csv_path}")
    print(f"[gbm-ctmc] Plot: {plot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
