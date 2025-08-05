import pandas as pd
import numpy as np
import statsmodels.api as sm

# ------------------------------------------------------------
# 1.  Read the source file
#     (placed in the same folder, change the name if needed)
# ------------------------------------------------------------
df = pd.read_excel("/Users/gaoxu/resources/人口普查数据/第七次全国人口普查.xlsx", usecols=["省份", "人口"]) \
       .rename(columns={"省份": "province",
                        "人口": "population"})

# ------------------------------------------------------------
# 2.  Rank provinces and take logarithms
# ------------------------------------------------------------
df = df.sort_values("population", ascending=False).copy()
df["rank"]    = np.arange(1, len(df) + 1)
df["ln_rank"] = np.log(
    df["rank"]-0.5)        # improved rank
df["ln_size"] = np.log(df["population"])

# ------------------------------------------------------------
# 3.  OLS regression: ln(rank) = α + β·ln(size)
#    and White-HC0 robust covariance
# ------------------------------------------------------------
X         = sm.add_constant(df["ln_size"])
ols_res   = sm.OLS(df["ln_rank"], X).fit()
rob_res   = ols_res.get_robustcov_results(cov_type="HC0")

pareto_coef = -ols_res.params["ln_size"]          # −β
output = pd.DataFrame([{
    "Pareto_Coefficient": pareto_coef,
    "SE_OLS":             ols_res.bse["ln_size"],
    "P_Value_OLS":        ols_res.pvalues["ln_size"],
    "SE_Robust":          rob_res.bse[1],          # index 1 = ln_size
    "P_Value_Robust":     rob_res.pvalues[1],
}])

# ------------------------------------------------------------
# 4.  Write result to Excel (no console print)
# ------------------------------------------------------------
output.to_excel("test.xlsx", index=False)
