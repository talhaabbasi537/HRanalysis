import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Excel File Ka Absolute (Full) Path
file_path = r'C:\Users\pc\Desktop\hrtask\HR Data.xlsx'

# Verify file existence
if not os.path.exists(file_path):
    print(f"❌ Error: File nahi mili path par: {file_path}")
    print("Mera mashwara: Ensure karein ke 'HR Data.xlsx' 'hrtask' folder me mojood ho.")
else:
    df = pd.read_excel(file_path)

    # Clean column names
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]

    # 2. Database Connection (Apna Password Enter Karein)
    db_password = 'admin123'  # <-- Yahan PostgreSQL password likhein

    engine = create_engine(f'postgresql://postgres:{db_password}@localhost:5432/hr_db')

    # 3. Direct Table Creation & Data Upload
    df.to_sql('hr_data', engine, if_exists='replace', index=False)

    print("✅ HR Data successfully uploaded to PostgreSQL table 'hr_data'!")