import pandas as pd
from app.repositories.status_store_repository import set_status
import os

def extract_xls(file_path: str) -> str:
    documents = []
    filename = os.path.basename(file_path)

    try:
        # set current status
        set_status(filename, "processing")
        
        # Select engine based on file extension
        if file_path.endswith(".xls"):
            sheets = pd.read_excel(file_path, sheet_name=None, engine="xlrd")
        else:
            sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

        for sheet_name, df in sheets.items():
            sheet_text = df.astype(str).fillna("").values.flatten()
            sheet_text = [cell.strip() for cell in sheet_text if cell.strip()]

            if sheet_text:
                documents.append({
                    "text": " ".join(sheet_text),
                    "metadata": {
                        "file_name": filename,
                        "file_type": "xls",
                        "page": sheet_name
                    }
                })

        set_status(filename, "processed")
        
    except Exception as e:
        set_status(filename, "failed", str(e))
        print(f"{filename} → failed ❌ ({e})")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        raise Exception(f"Excel processing failed: {str(e)}")

    return documents