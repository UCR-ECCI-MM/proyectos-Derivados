from src.functions.general import min_max_normalize, safe_min, safe_max
from src.functions.geothermometers import compute_geothermometers
from src.heuristic import heuristic_weigths, \
  objective_function
from src.structures.Manifestation import Manifestation
from src.structures.NormalizationStats import NormalizationStats


def main():
  data = [
    Manifestation(
      mid="Manifestacion 1", x=100.0, y=200.0,
      temp=92.0, cond=1800.0,
      cl=650.0, si=230.0,
      na=480.0, k=32.0, ca=12.0
    ),
    Manifestation(
      mid="Manifestacion 2", x=110.0, y=210.0,
      temp=78.0, cond=1500.0,
      cl=450.0, si=180.0,
      na=350.0, k=28.0, ca=18.0
    ),
    Manifestation(
      mid="Manifestacion 3", x=95.0, y=205.0,
      temp=105.0, cond=2200.0,
      cl=900.0, si=280.0,
      na=600.0, k=40.0, ca=25.0
    )
  ]

  print("\n=== Test de Geotermométros Test ===\n")


  temps = [m.temp for m in data]
  conds = [m.cond for m in data]
  cls = [m.cl for m in data]

  # Compute the geothermometer on each manifestation
  t_avgs = []
  for m in data:
    t_si, t_nak, t_nakca = compute_geothermometers(
      m.si, m.na, m.k, m.ca
    )
    t_avgs.append((t_si + t_nak + t_nakca) / 3.0)

  # Calculate the stats
  stats = NormalizationStats(
    temp_min=safe_min(temps),
    temp_max=safe_max(temps),
    cond_min=safe_min(conds),
    cond_max=safe_max(conds),
    cl_min=safe_min(cls),
    cl_max=safe_max(cls),
    tavg_min=safe_min(t_avgs),
    tavg_max=safe_max(t_avgs)
  )

  weights = (0.4, 0.3, 0.3)

  for m in data:
    print(f"=== {m.mid} ===")

    # Compute geothermometer values
    t_si, t_nak, t_nakca = compute_geothermometers(m.si, m.na, m.k, m.ca)
    t_avg = (t_si + t_nak + t_nakca) / 3.0

    print(f"  T_Si      = {t_si:.2f} °C")
    print(f"  T_NaK     = {t_nak:.2f} °C")
    print(f"  T_NaKCa   = {t_nakca:.2f} °C")
    print(f"  T_avg     = {t_avg:.2f} °C\n")

    # Normalization per parameter
    n_temp = min_max_normalize(m.temp, stats.temp_min, stats.temp_max)
    n_cond = min_max_normalize(m.cond, stats.cond_min, stats.cond_max)
    n_cl = min_max_normalize(m.cl, stats.cl_min, stats.cl_max)
    n_tavg = min_max_normalize(t_avg, stats.tavg_min, stats.tavg_max)

    print("  Valores normalizados:")
    print(f"    temp_n  = {n_temp:.3f}")
    print(f"    cond_n  = {n_cond:.3f}")
    print(f"    cl_n    = {n_cl:.3f}")
    print(f"    tavg_n  = {n_tavg:.3f}\n")

    gs = objective_function(
      temp=m.temp,
      cond=m.cond,
      cl=m.cl,
      si=m.si,
      na=m.na,
      k=m.k,
      ca=m.ca,
      stats=stats,
      weights=weights
    )

  print(f"  >>> Geothermal Score Gs(i) = {gs:.4f}\n")

  print("Computing heuristic values...\n")
  beta_heuristic = 2.0
  idw_power = 2.0

  h_values = heuristic_weigths(
    data,
    stats,
    weights=weights,
    beta_heuristic=beta_heuristic,
    idw_power=idw_power
  )

  print("=== Results: Heuristic H(i) per manifestation ===\n")
  for m, h in zip(data, h_values):
    print(f"  {m.mid} -> H(i) = {h:.6f}")


if __name__ == "__main__":
  main()