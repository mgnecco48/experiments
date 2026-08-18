import pandas as pd

excel = pd.ExcelFile("COGS Mendels 2.0.xlsx")

print(excel.sheet_names)

sheets = excel.sheet_names


def findProductCost(df):
    coords = []
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            val = df.iat[row, col]

            if isinstance(val, str) and "product cost" in val.lower():
                coords.append((row, col))

    return coords


def extractData(df, row, col):
    name = df.iat[row - 3, col]
    food_cost = df.iat[row - 2, col + 1]
    staff_cost = df.iat[row - 1, col + 1]
    product_cost = df.iat[row, col + 1]

    return {
        "Product": name,
        "Food Cost": food_cost,
        "Staff Cost": staff_cost,
        "Total Cost": product_cost,
    }


# def addColumns(df):
#     df = df.copy()
#
#     df["Added 15%"] = df["Total Cost"] * 0.15
#     df["Sale price to shop"] = df["Total Cost"] + df["Added 15%"]
#     df["(In Store) Sale price in shop (incl VAT)"] = 100
#     df["(In Store) Sale price in shop (excl VAT)"] = (
#         df["(In Store) Sale price in shop (incl VAT)"] / 1.25
#     )
#     df["(In Store) Food cost %"] = (
#         df["Sale price to shop"] / df["(In Store) Sale price in shop (excl VAT)"]
#     )
#     df["(In Store) Gross Margin %"] = 1 - df["(In Store) Food cost %"]
#     df["(In Store) Contribution"] = (
#         df["(In Store) Sale price in shop (excl VAT)"] - df["Sale price to shop"]
#     )
#     df["(Take Away) Sale price in shop (incl VAT)"] = 0
#     df["(Take Away) Sale price in shop (excl VAT)"] = (
#         df["(Take Away) Sale price in shop (incl VAT)"] / 1.25
#     )
#     df["(Take Away) Food cost %"] = (
#         df["Sale price to shop"] / df["(Take Away) Sale price in shop (excl VAT)"]
#     )
#     df["(Take Away) Gross Margin %"] = 1 - df["(Take Away) Food cost %"]
#     df["(Take Away) Contribution"] = (
#         df["(Take Away) Sale price in shop (excl VAT)"] - df["Sale price to shop"]
#     )
#
#     return df


products = []
for sheet in sheets:
    print(f"\nCategory: {sheet}\n")
    df = pd.read_excel(excel, sheet_name=sheet, header=None)
    coords = findProductCost(df)

    for row, col in coords:
        data = extractData(df, row, col)
        products.append(data)

compact_df = pd.DataFrame(products)
print(compact_df)

compact_df.to_excel("summary.xlsx", sheet_name="Summary", index=False)
