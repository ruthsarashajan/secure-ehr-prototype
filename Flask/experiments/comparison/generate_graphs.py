import csv
from pathlib import Path
from statistics import mean, stdev

import matplotlib

# Create image files without opening chart windows.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------

script_folder = Path(__file__).resolve().parent

results_file = script_folder / "security_comparison_results.csv"

graphs_folder = script_folder / "graphs"
graphs_folder.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def convert_to_boolean(value):
    """Convert TRUE or FALSE text from the CSV into a Boolean value."""

    return value.strip().lower() == "true"


def calculate_standard_deviation(values):
    """Calculate standard deviation when there is more than one result."""

    if len(values) > 1:
        return stdev(values)

    return 0


def save_graph(figure, file_name, graph_name):
    """Save one graph and print its location."""

    graph_path = graphs_folder / file_name

    figure.savefig(
        graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(figure)

    print()
    print(graph_name + " saved in:")
    print(graph_path)


# ---------------------------------------------------------
# Read the experiment results
# ---------------------------------------------------------

rows = []

with results_file.open(
    mode="r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        # Ignore completely empty CSV rows.
        if not row.get("timestamp"):
            continue

        rows.append(
            {
                "timestamp": row["timestamp"],
                "number_of_tests": int(row["number_of_tests"]),
                "sha256_average_ms": float(
                    row["sha256_average_ms"]
                ),
                "sha256_digest_bytes": int(
                    row["sha256_digest_bytes"]
                ),
                "ml_dsa_keygen_average_ms": float(
                    row["ml_dsa_keygen_average_ms"]
                ),
                "ml_dsa_signing_average_ms": float(
                    row["ml_dsa_signing_average_ms"]
                ),
                "ml_dsa_verification_average_ms": float(
                    row["ml_dsa_verification_average_ms"]
                ),
                "ml_dsa_public_key_bytes": int(
                    row["ml_dsa_public_key_bytes"]
                ),
                "ml_dsa_secret_key_bytes": int(
                    row["ml_dsa_secret_key_bytes"]
                ),
                "ml_dsa_signature_bytes": int(
                    row["ml_dsa_signature_bytes"]
                ),
                "sha256_detected_change": convert_to_boolean(
                    row["sha256_detected_change"]
                ),
                "ml_dsa_detected_change": convert_to_boolean(
                    row["ml_dsa_detected_change"]
                )
            }
        )


if len(rows) == 0:
    raise ValueError(
        "No experiment results were found in the CSV file."
    )


# ---------------------------------------------------------
# Prepare the data
# ---------------------------------------------------------

runs = list(range(1, len(rows) + 1))

sha256_times_ms = [
    row["sha256_average_ms"]
    for row in rows
]

key_generation_times = [
    row["ml_dsa_keygen_average_ms"]
    for row in rows
]

signing_times = [
    row["ml_dsa_signing_average_ms"]
    for row in rows
]

verification_times = [
    row["ml_dsa_verification_average_ms"]
    for row in rows
]


# Convert SHA-256 milliseconds to microseconds.
sha256_times_microseconds = [
    time * 1000
    for time in sha256_times_ms
]


# Calculate averages.
sha256_average = mean(sha256_times_microseconds)

key_generation_average = mean(key_generation_times)

signing_average = mean(signing_times)

verification_average = mean(verification_times)


# Calculate standard deviations.
sha256_standard_deviation = calculate_standard_deviation(
    sha256_times_microseconds
)

key_generation_standard_deviation = calculate_standard_deviation(
    key_generation_times
)

signing_standard_deviation = calculate_standard_deviation(
    signing_times
)

verification_standard_deviation = calculate_standard_deviation(
    verification_times
)


# ---------------------------------------------------------
# Graph 1: Average operation times
# ---------------------------------------------------------

figure, axes = plt.subplots(
    1,
    2,
    figsize=(14, 7)
)

figure.suptitle(
    "Average Cryptographic Operation Times",
    fontsize=22
)


# SHA-256 side of the graph.
sha256_bar = axes[0].bar(
    ["SHA-256 hashing"],
    [sha256_average],
    yerr=[sha256_standard_deviation],
    capsize=6,
    color="#4f79bd",
    edgecolor="#34588f"
)

axes[0].set_title(
    "SHA-256",
    fontsize=17
)

axes[0].set_ylabel(
    "Average execution time (microseconds)"
)

axes[0].grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

axes[0].set_axisbelow(True)

axes[0].set_ylim(
    0,
    (
        sha256_average
        + sha256_standard_deviation
    ) * 1.35
)

sha256_label_height = (
    sha256_average
    + sha256_standard_deviation
    + (sha256_average * 0.05)
)

axes[0].text(
    sha256_bar[0].get_x()
    + sha256_bar[0].get_width() / 2,
    sha256_label_height,
    f"{sha256_average:.3f} microseconds",
    ha="center",
    fontsize=12
)


# ML-DSA side of the graph.
ml_dsa_names = [
    "Key generation",
    "Signing",
    "Verification"
]

ml_dsa_averages = [
    key_generation_average,
    signing_average,
    verification_average
]

ml_dsa_standard_deviations = [
    key_generation_standard_deviation,
    signing_standard_deviation,
    verification_standard_deviation
]

ml_dsa_colours = [
    "#5b9bd5",
    "#ed7d31",
    "#70ad47"
]

ml_dsa_bars = axes[1].bar(
    ml_dsa_names,
    ml_dsa_averages,
    yerr=ml_dsa_standard_deviations,
    capsize=6,
    color=ml_dsa_colours,
    edgecolor="#555555"
)

axes[1].set_title(
    "ML-DSA-44",
    fontsize=17
)

axes[1].set_ylabel(
    "Average execution time (milliseconds)"
)

axes[1].grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

axes[1].set_axisbelow(True)

highest_ml_dsa_result = max(
    average + deviation
    for average, deviation in zip(
        ml_dsa_averages,
        ml_dsa_standard_deviations
    )
)

axes[1].set_ylim(
    0,
    highest_ml_dsa_result * 1.30
)

for bar, average, deviation in zip(
    ml_dsa_bars,
    ml_dsa_averages,
    ml_dsa_standard_deviations
):
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        average + deviation + 2,
        f"{average:.2f} ms",
        ha="center",
        fontsize=12
    )


figure.text(
    0.5,
    0.02,
    (
        "SHA-256 is shown in microseconds and ML-DSA-44 "
        "is shown in milliseconds. Error bars show the "
        "sample standard deviation across the saved runs."
    ),
    ha="center",
    fontsize=11
)

figure.tight_layout(
    rect=[0, 0.07, 1, 0.93]
)

save_graph(
    figure,
    "average_operation_times.png",
    "Average operation times graph"
)


# ---------------------------------------------------------
# Graph 2: Combined bar and line chart
# ---------------------------------------------------------

figure, axis = plt.subplots(
    figsize=(14, 8)
)


# Signing is shown using bars.
axis.bar(
    runs,
    signing_times,
    width=0.65,
    color="#a9c77d",
    edgecolor="#6f9345",
    alpha=0.9,
    label="Signing time (bars)"
)


# Key generation is shown using a line.
axis.plot(
    runs,
    key_generation_times,
    color="#4472c4",
    marker="o",
    linewidth=2.5,
    markersize=7,
    label="Key generation time (line)"
)


# Verification is shown using a line.
axis.plot(
    runs,
    verification_times,
    color="#ed7d31",
    marker="s",
    linewidth=2.5,
    markersize=7,
    label="Verification time (line)"
)


axis.set_title(
    "ML-DSA-44 Performance Across 10 Runs",
    fontsize=21
)

axis.set_xlabel(
    "Experiment run",
    fontsize=13
)

axis.set_ylabel(
    "Average execution time (milliseconds)",
    fontsize=13
)

axis.set_xticks(runs)

axis.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

axis.set_axisbelow(True)

axis.legend(
    loc="upper left",
    fontsize=11
)

figure.tight_layout()

save_graph(
    figure,
    "ml_dsa_performance.png",
    "ML-DSA combined bar and line graph"
)


# ---------------------------------------------------------
# Graph 3: Storage requirements
# ---------------------------------------------------------

storage_names = [
    "SHA-256 digest",
    "ML-DSA public key",
    "ML-DSA secret key",
    "ML-DSA signature"
]

storage_values = [
    rows[0]["sha256_digest_bytes"],
    rows[0]["ml_dsa_public_key_bytes"],
    rows[0]["ml_dsa_secret_key_bytes"],
    rows[0]["ml_dsa_signature_bytes"]
]

storage_colours = [
    "#4f79bd",
    "#5b9bd5",
    "#ed7d31",
    "#a5a5a5"
]


figure, axis = plt.subplots(
    figsize=(13, 8)
)

storage_bars = axis.bar(
    storage_names,
    storage_values,
    color=storage_colours,
    edgecolor="#444444"
)

axis.set_title(
    "Cryptographic Storage Requirements",
    fontsize=21
)

axis.set_ylabel(
    "Size (bytes)",
    fontsize=13
)

axis.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

axis.set_axisbelow(True)

axis.set_ylim(
    0,
    max(storage_values) * 1.20
)

axis.tick_params(
    axis="x",
    rotation=15
)

for bar, value in zip(
    storage_bars,
    storage_values
):
    axis.text(
        bar.get_x() + bar.get_width() / 2,
        value + 45,
        f"{value:,} bytes",
        ha="center",
        fontsize=12
    )

figure.tight_layout()

save_graph(
    figure,
    "storage_comparison.png",
    "Storage comparison graph"
)


# ---------------------------------------------------------
# Graph 4: Tampering detection
# ---------------------------------------------------------

sha256_detection_count = sum(
    row["sha256_detected_change"]
    for row in rows
)

ml_dsa_detection_count = sum(
    row["ml_dsa_detected_change"]
    for row in rows
)

detection_names = [
    "SHA-256",
    "ML-DSA-44"
]

detection_values = [
    sha256_detection_count,
    ml_dsa_detection_count
]


figure, axis = plt.subplots(
    figsize=(10, 7)
)

detection_bars = axis.bar(
    detection_names,
    detection_values,
    color=["#4f79bd", "#70ad47"],
    edgecolor="#444444"
)

axis.set_title(
    "Tampering Detection Across Experiment Runs",
    fontsize=20
)

axis.set_ylabel(
    "Number of runs detecting changed data",
    fontsize=12
)

axis.set_ylim(
    0,
    len(rows) + 1
)

axis.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

axis.set_axisbelow(True)

for bar, value in zip(
    detection_bars,
    detection_values
):
    axis.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.2,
        f"{value}/{len(rows)} runs",
        ha="center",
        fontsize=13
    )

figure.tight_layout()

save_graph(
    figure,
    "tampering_detection.png",
    "Tampering detection graph"
)


# ---------------------------------------------------------
# Final terminal summary
# ---------------------------------------------------------

print()
print("All graphs were created successfully.")

print()
print("Number of experiment runs:")
print(len(rows))

print()
print("Average performance results:")
print(
    f"SHA-256 hashing: "
    f"{mean(sha256_times_ms):.6f} milliseconds"
)
print(
    f"ML-DSA key generation: "
    f"{key_generation_average:.2f} milliseconds"
)
print(
    f"ML-DSA signing: "
    f"{signing_average:.2f} milliseconds"
)
print(
    f"ML-DSA verification: "
    f"{verification_average:.2f} milliseconds"
)

print()
print("Tampering detection results:")
print(
    f"SHA-256: "
    f"{sha256_detection_count}/{len(rows)} runs"
)
print(
    f"ML-DSA-44: "
    f"{ml_dsa_detection_count}/{len(rows)} runs"
)

print()
print("All graphs saved in:")
print(graphs_folder)