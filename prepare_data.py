from pathlib import Path

import pandas as pd

Path("clean").mkdir(exist_ok=True)

GROUPS = {
    34: "2-4", 6: "5-9", 7: "10-14", 8: "15-19",
    9: "20-34", 10: "20-34", 11: "20-34",
    12: "35-59", 13: "35-59", 14: "35-59", 15: "35-59", 16: "35-59",
    17: "60+", 18: "60+", 19: "60+", 20: "60+", 21: "60+",
}
ORDER = ["2-4", "5-9", "10-14", "15-19", "20-34", "35-59", "60+"]
NAMES = {"TГјrkiye": "Türkiye", "CГґte d'Ivoire": "Côte d'Ivoire"}


def read_table(name):
    path = Path(f"data/{name}.xlsx")
    if path.exists():
        return pd.read_excel(path, sheet_name=0)
    return pd.read_csv(f"data/{name}.csv")


def fix_names(df):
    df["location_name"] = df["location_name"].replace(NAMES)
    return df


def age_table(df):
    number = df[df["metric_id"] == 1]
    rate = df[df["metric_id"] == 3]
    keys = ["location_name", "year", "age_id"]
    data = number[keys + ["val"]].merge(
        rate[keys + ["val"]], on=keys, suffixes=("_number", "_rate")
    )
    data["population"] = data["val_number"] / data["val_rate"] * 100_000
    data["group"] = data["age_id"].map(GROUPS)
    result = data.groupby(["location_name", "year", "group"], as_index=False)[
        ["val_number", "population"]
    ].sum()
    result["rate"] = result["val_number"] / result["population"] * 100_000
    result["group"] = pd.Categorical(result["group"], ORDER, ordered=True)
    return result.rename(columns={"val_number": "number"}).sort_values(
        ["location_name", "year", "group"]
    )


world = read_table("global_age")
world["location_name"] = "World"
countries = fix_names(read_table("countries_age"))
pd.concat([age_table(world), age_table(countries)]).to_csv(
    "clean/age_groups.csv", index=False
)

sex = read_table("global_sex")
sex = sex[sex["metric_id"] == 1].copy()
sex["group"] = sex["age_id"].map(GROUPS)
sex = sex.groupby(["year", "group", "sex_name"], as_index=False)["val"].sum()
sex["group"] = pd.Categorical(sex["group"], ORDER, ordered=True)
sex.rename(columns={"val": "number"}).sort_values(["year", "group"]).to_csv(
    "clean/world_sex.csv", index=False
)

standard = fix_names(read_table("countries_std"))
standard[["location_name", "sex_name", "year", "val", "lower", "upper"]].rename(
    columns={"val": "rate"}
).to_csv("clean/map.csv", index=False)

print("Готово: файлы в папке clean")