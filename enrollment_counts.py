import os
import pandas as pd

districts = {
    "0973783": "black_oak_mine_unified",
    "0961838": "buckeye_unified",
    "0961846": "camino_unified",
    "0910090": "el_dorado_county_office_of_education",
    "0961853": "el_dorado_union_high",
    "0961879": "gold_oak_union_elementary",
    "0961887": "gold_trail_union_elementary",
    "0961895": "indian_diggings_elementary",
    "0961903": "lake_tahoe_unified",
    "0961911": "latrobe",
    "0961929": "mother_lode_union_elementary",
    "0961945": "pioneer_union_elementary",
    "0961952": "placerville_union_elementary",
    "0961960": "pollock_pines_elementary",
    "0961978": "rescue_union_elementary",
    "0961986": "silver_fork_elementary",
}

current_data = []

for d_code, d_name in districts.items():
    file = f"Enrollment_2024-2025_{d_code}.csv"
    df = pd.read_csv(os.path.join("enrollData", file)).assign(District=d_name)
    current_data.append(df)

df = pd.concat(current_data)
str_list = [str(a).zfill(2) for a in range(1, 13)]
grade_mapping = {
    **dict(zip(str_list + list(range(1, 13)), str_list * 2)),
    **{"PS": "PS", "TK": "TK", "KN": "KN", "US": "US"},
}
enroll = (
    df.assign(GroupByValue=df.GroupByValue.map(grade_mapping))
    .groupby(["District", "SchoolNameValue", "GroupByValue"])
    .agg({"Group2TotalDetail": "sum"})
    .unstack()
    .droplevel(0, axis=1)
    .assign(
        Total_Elem=lambda df_: df_.loc[
            :, ["TK", "KN", "01", "02", "03", "04", "05", "06", "07", "08"]
        ].sum(1),
        Total_HS=lambda df_: df_.loc[:, ["09", "10", "11", "12"]].sum(1),
        School_Total=lambda df_: df_.Total_Elem + df_.Total_HS,
    )
    .fillna(0)
    .astype("int")
    .loc[
        :,
        [
            "PS",
            "TK",
            "KN",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "US",
            "Total_Elem",
            "09",
            "10",
            "11",
            "12",
            "Total_HS",
            "School_Total",
        ],
    ]
)
district_totals = pd.concat(
    {"TOTAL": enroll.groupby(level=0).sum()}, names=["SchoolNameValue"]
).swaplevel()
final = pd.concat([enroll, district_totals]).sort_index()
final.to_excel("final_enrollment.xlsx")
