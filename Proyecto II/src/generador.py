# synthetic_dataset_generator.py
# ---------------------------------------------------------------
# Expands a real geothermal dataset to sizes:
#   - 100
#   - 150
#   - 300
#
# Uses spatial jitter + chemical perturbation with physical limits.
# ---------------------------------------------------------------

import csv
import random
import math


def load_real_manifestations(path: str):
  data = []
  with open(path, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      row2 = {
        "id": row["id"],
        "x": float(row["coord_x"]),
        "y": float(row["coord_y"]),
        "temp": float(row["temp"]),
        "cond": float(row["cond"]),
        "Cl": float(row["Cl"]),
        "Ca": float(row["Ca"]),
        "Si": float(row["Si"]),
        "Na": float(row["Na"]),
        "K": float(row["K"]),
        "Mg": float(row["Mg"]),
      }
      data.append(row2)
  return data


def generate_synthetic_item(base):
  """Create a synthetic sample from a base manifestation."""

  # Spatial jitter (≈300 m)
  x_new = base["x"] + random.gauss(0, 0.003)
  y_new = base["y"] + random.gauss(0, 0.003)

  def perturb(value):
    """Small 5%–7% Gaussian variation."""
    return max(0.0001, value * random.gauss(1.0, 0.05))

  new_item = {
    "id": base["id"] + "_synt_" + str(random.randint(100000, 999999)),
    "x": x_new,
    "y": y_new,
    "temp": max(20, min(120, perturb(base["temp"]))),
    "cond": perturb(base["cond"]),
    "Cl": perturb(base["Cl"]),
    "Ca": perturb(base["Ca"]),
    "Si": perturb(base["Si"]),
    "Na": perturb(base["Na"]),
    "K": perturb(base["K"]),
    "Mg": perturb(base["Mg"]),
  }

  return new_item


def expand_dataset(real_data, target_size):
  """Expand dataset using resampling + perturbation."""

  if len(real_data) >= target_size:
    return real_data[:target_size]

  new_data = list(real_data)

  while len(new_data) < target_size:
    base = random.choice(real_data)
    new_data.append(generate_synthetic_item(base))

  return new_data


def save_dataset(path, data):
  """Save dataset to CSV."""
  fieldnames = ["id", "coord_x", "coord_y", "temp", "cond",
                "Cl", "Ca", "Si", "Na", "K", "Mg"]

  with open(path, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for d in data:
      writer.writerow({
        "id": d["id"],
        "coord_x": d["x"],
        "coord_y": d["y"],
        "temp": d["temp"],
        "cond": d["cond"],
        "Cl": d["Cl"],
        "Ca": d["Ca"],
        "Si": d["Si"],
        "Na": d["Na"],
        "K": d["K"],
        "Mg": d["Mg"],
      })


def main():
  real_data = load_real_manifestations("../dataset/manifestations_30.csv")

  # Expand datasets
  d100 = expand_dataset(real_data, 100)
  d150 = expand_dataset(real_data, 150)
  d300 = expand_dataset(real_data, 300)

  # Save them
  save_dataset("../dataset/dataset_100.csv", d100)
  save_dataset("../dataset/dataset_150.csv", d150)
  save_dataset("../dataset/dataset_300.csv", d300)

  print("Datasets generated successfully:")
  print(" - dataset_100.csv")
  print(" - dataset_150.csv")
  print(" - dataset_300.csv")


if __name__ == "__main__":
  main()
