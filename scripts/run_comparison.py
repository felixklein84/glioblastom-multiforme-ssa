#!/usr/bin/env python3
"""Run all four scenarios (no therapy / RT / TMZ / Stupp) and produce
comparison plots and a summary CSV.

Usage:
    python scripts/run_comparison.py
    python scripts/run_comparison.py --seed 7 --t-end 200 --out outputs/comparison_demo

All scenarios share the same seed so they share the *same pre-treatment
stochastic history*; they diverge at the first therapy event. Output is
reproducible.

NOTE: Therapy kill rates in the shipped configs are PLACEHOLDERS (ASM). The
comparison demonstrates *qualitative mechanics*, not clinical magnitudes.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from gbm_ctmc.io.results import save_trajectory_csv, trajectory_to_dataframe  # noqa: E402
from gbm_ctmc.parameters import ModelParams  # noqa: E402
from gbm_ctmc.plotting.comparison import plot_comparison  # noqa: E402
from gbm_ctmc.simulation import run_simulation  # noqa: E402

SCENARIOS = [
    ("no_therapy", ROOT / "configs" / "scenarios" / "no_therapy.yaml"),
    ("radiotherapy", ROOT / "configs" / "scenarios" / "radiotherapy.yaml"),
    ("tmz", ROOT / "configs" / "scenarios" / "tmz.yaml"),
    ("stupp", ROOT / "configs" / "scenarios" / "stupp.yaml"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the 4-scenario therapy comparison.")
    parser.add_argument("--seed", type=int, default=42,
                        help="Shared RNG seed across all scenarios (default 42).")
    parser.add_argument("--t-end", type=float, default=None,
                        help="Override the t_end (days) on every scenario.")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs" / "comparison",
                        help="Output directory (default outputs/comparison).")
    args = parser.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    trajectories: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict[str, object]] = []

    for name, cfg_path in SCENARIOS:
        params = ModelParams.from_yaml(cfg_path)
        params.run.seed = args.seed
        if args.t_end is not None:
            params.run.t_end = args.t_end

        print(f"\n[{name}] seed={params.run.seed} t_end={params.run.t_end} d  "
              f"therapy.type={params.therapy.type}")

        t0 = time.perf_counter()
        traj = run_simulation(params)
        elapsed = time.perf_counter() - t0

        df = trajectory_to_dataframe(traj)
        scenario_dir = out_dir / name
        save_trajectory_csv(traj, scenario_dir / "trajectory.csv")

        final = df.iloc[-1]
        nadir_idx = int(df["total"].idxmin())
        nadir = df.iloc[nadir_idx]

        print(f"  events: {len(df) - 1}   runtime: {elapsed:.2f} s")
        print(f"  final  t={final['time']:.1f}: S={int(final['S'])} P={int(final['P'])} "
              f"D={int(final['D'])} Q={int(final['Q'])} total={int(final['total'])}")
        print(f"  nadir  t={nadir['time']:.1f}: total={int(nadir['total'])}")

        trajectories[name] = df
        summary_rows.append({
            "scenario": name,
            "seed": params.run.seed,
            "t_end": params.run.t_end,
            "n_events": int(len(df) - 1),
            "runtime_s": round(elapsed, 3),
            "final_S": int(final["S"]),
            "final_P": int(final["P"]),
            "final_D": int(final["D"]),
            "final_Q": int(final["Q"]),
            "final_total": int(final["total"]),
            "nadir_total": int(nadir["total"]),
            "nadir_time": float(nadir["time"]),
            "extinct_at_end": bool(final["total"] == 0),
        })

    summary = pd.DataFrame(summary_rows)
    summary_path = out_dir / "summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"\n[summary] {summary_path}")
    print(summary.to_string(index=False))

    # Plots
    plot_comparison(
        trajectories, out_dir / "comparison_total.png",
        column="total", title="Total tumor burden across scenarios",
    )
    plot_comparison(
        trajectories, out_dir / "comparison_total_log.png",
        column="total", title="Total tumor burden (symlog y)",
        log_y=True,
    )
    for state in ("S", "P", "D", "Q"):
        plot_comparison(
            trajectories, out_dir / f"comparison_{state}.png",
            column=state, title=f"{state}-state count across scenarios",
        )
    print(f"[plots] {out_dir}/comparison_*.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
