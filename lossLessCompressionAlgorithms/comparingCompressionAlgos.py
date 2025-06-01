import bz2
import lzma
import gzip
import time
import os
import matplotlib.pyplot as plt

# --- 1. Extremely Simple Dummy Data (approx. 1MB) ---
original_data = (b"The quick brown fox jumps over the lazy dog. " * 1024 * 5) # Approx 0.2MB
original_data += os.urandom(1024 * 800) # Add some less compressible data to reach ~1MB
original_size = len(original_data)
print(f"Original data size: {original_size / (1024*1024):.2f} MB")

# --- 2. Test Configurations (High Compression Only) ---
# (algorithm_name, compress_func_with_high_level, decompress_func)
CONFIGS = [
    (
        "gzip (High)",
        lambda data: gzip.compress(data, compresslevel=9), # Level 9 for high
        gzip.decompress
    ),
    (
        "bz2 (High)",
        lambda data: bz2.compress(data, compresslevel=9), # Level 9 for high
        bz2.decompress
    ),
    (
        "lzma (High)",
        lambda data: lzma.compress(data, preset=9), # Preset 9 for high (ultra)
        lzma.decompress
    )
]

results = []

# --- 3. Run Compression/Decompression Tests ---
print(f"\n--- Testing High Compression Settings ---")
for name, compress_fn, decompress_fn in CONFIGS:
    # Compression
    start_comp = time.perf_counter()
    compressed_data = compress_fn(original_data)
    comp_time = time.perf_counter() - start_comp
    compressed_size = len(compressed_data)
    ratio = original_size / compressed_size if compressed_size > 0 else 0

    # Decompression
    start_decomp = time.perf_counter()
    decompressed_data = decompress_fn(compressed_data) # Verify integrity implicitly
    decomp_time = time.perf_counter() - start_decomp

    if decompressed_data != original_data: # Minimal check
        print(f"DECOMPRESSION MISMATCH for {name} - this shouldn't happen!")
        # In a truly minimal script as per request, one might even omit this check.
        # For now, keeping it as a crucial sanity check.

    print(f"{name}: Comp Time: {comp_time:.3f}s, Decomp Time: {decomp_time:.3f}s, Ratio: {ratio:.2f}x, Size: {compressed_size/1024:.1f}KB")
    results.append({
        "algo": name,
        "comp_time": comp_time,
        "decomp_time": decomp_time,
        "ratio": ratio
    })

# --- 4. Simplified Plotting ---
if not results:
    print("\nNo results to plot.")
else:
    comp_times = [r["comp_time"] for r in results]
    decomp_times = [r["decomp_time"] for r in results]
    ratios = [r["ratio"] for r in results]
    algo_names = [r["algo"] for r in results]

    # Plot 1: Compression Time vs Ratio
    plt.figure(figsize=(10, 6))
    scatter1 = plt.scatter(comp_times, ratios, c=range(len(algo_names)), cmap='viridis', s=100)
    plt.xlabel('Compression Time (seconds) - Lower is Faster')
    plt.ylabel('Compression Ratio - Higher is Better')
    plt.title(f'High Compression: Time vs. Ratio (Original: {original_size/(1024*1024):.2f}MB)')
    plt.grid(True, linestyle='--', alpha=0.6)
    # Add labels to points
    for i, name in enumerate(algo_names):
        plt.annotate(name.split(" ")[0], (comp_times[i], ratios[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.tight_layout()
    plt.savefig("ultra_simple_compression_plot.png")
    print("\nSaved ultra_simple_compression_plot.png")
    plt.show()

    # Plot 2: Decompression Time vs Ratio
    plt.figure(figsize=(10, 6))
    scatter2 = plt.scatter(decomp_times, ratios, c=range(len(algo_names)), cmap='plasma', s=100)
    plt.xlabel('Decompression Time (seconds) - Lower is Faster')
    plt.ylabel('Compression Ratio - Higher is Better')
    plt.title(f'High Compression: Decompression Time vs. Ratio (Original: {original_size/(1024*1024):.2f}MB)')
    plt.grid(True, linestyle='--', alpha=0.6)
    # Add labels to points
    for i, name in enumerate(algo_names):
        plt.annotate(name.split(" ")[0], (decomp_times[i], ratios[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.tight_layout()
    plt.savefig("ultra_simple_decompression_plot.png")
    print("Saved ultra_simple_decompression_plot.png")
    plt.show()
