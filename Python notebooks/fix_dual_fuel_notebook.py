import json
from pathlib import Path


NOTEBOOK_PATH = Path(
    "/Users/dharathi/Library/CloudStorage/OneDrive-SwinburneUniversity/Documents/codex/research/Hyd-Diesel-Engine-Project/Python notebooks/Dual_Fuel_Engine_Combustion_Dataset.ipynb"
)


def replace_source(cell_source: str) -> str:
    updated = cell_source

    # Prevent target leakage in the single-output diesel model by removing
    # both complementary energy-share targets from the feature matrix.
    updated = updated.replace(
        "X = df_encoded.drop(columns=['Diesel_Energy_Share'])",
        "X = df_encoded.drop(columns=['Diesel_Energy_Share', 'Gasoline_Energy_Share'])",
    )

    # Prevent target leakage in the single-output gasoline model by removing
    # both complementary energy-share targets from the feature matrix.
    updated = updated.replace(
        "X1 = df_encoded.drop(columns=['Gasoline_Energy_Share'])",
        "X1 = df_encoded.drop(columns=['Diesel_Energy_Share', 'Gasoline_Energy_Share'])",
    )

    # Fix the multi-output Random Forest section so it uses the Random Forest
    # model's predictions rather than reusing the earlier Lasso predictions.
    updated = updated.replace(
        "y_rf_pred_multiple = model_multiple.predict(X_test_multiple)",
        "y_rf_pred_multiple = model_rf_multiple.predict(X_test_multiple)",
    )
    updated = updated.replace(
        'print("MSE:", mean_squared_error(y_test_multiple, y_pred_multiple))',
        'print("MSE:", mean_squared_error(y_test_multiple, y_rf_pred_multiple))',
    )
    updated = updated.replace(
        'print("R² Score:", r2_score(y_test_multiple, y_pred_multiple))',
        'print("R² Score:", r2_score(y_test_multiple, y_rf_pred_multiple))',
    )

    return updated


def main() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text())
    changed = 0

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        original = "".join(cell.get("source", []))
        updated = replace_source(original)
        if updated != original:
            cell["source"] = updated.splitlines(keepends=True)
            changed += 1

    if changed == 0:
        raise SystemExit("No matching notebook cells were updated.")

    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1))
    print(f"Updated {changed} code cell(s) in {NOTEBOOK_PATH.name}")


if __name__ == "__main__":
    main()
