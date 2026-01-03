"""Test script to run all modes and save outputs in separate directories."""

import os
import subprocess
import sys


def main():
    from core.modes import get_available_modes
    
    input_dir = "data/input"
    base_output = "data/output"
    
    modes = get_available_modes()
    
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input directory not found: {input_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print(f"Testing all anonymization modes ({len(modes)} modes)")
    print("=" * 60)
    print()
    
    for idx, mode in enumerate(modes, start=1):
        output_dir = os.path.join(base_output, f"out{idx}")
        
        print(f"[{idx}/{len(modes)}] Testing mode: {mode}")
        print(f"  Input: {input_dir}")
        print(f"  Output: {output_dir}")
        
        cmd = [
            sys.executable,
            "cli.py",
            "--input", input_dir,
            "--output", output_dir,
            "--mode", mode
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
            print(f"  [OK] Success: {mode}")
            if result.stdout:
                print(f"  Output: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"  [ERROR] Failed: {mode}")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            sys.exit(1)
        
        print()
    
    print("=" * 60)
    print("[OK] All modes tested successfully!")
    print("=" * 60)
    print(f"\nOutput directories:")
    for idx, mode in enumerate(modes, start=1):
        output_dir = os.path.join(base_output, f"out{idx}")
        print(f"  - {output_dir} ({mode})")


if __name__ == "__main__":
    main()

