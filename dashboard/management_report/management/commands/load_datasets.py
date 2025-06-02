from django.core.management.base import BaseCommand
import pandas as pd
import os
from django.conf import settings
from urllib.parse import quote_plus
from sqlalchemy import create_engine

class Command(BaseCommand):
    help = "Loads Excel datasets from /datasets/ into MySQL tables"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("⏳ Starting dataset import..."))

        # Define the folder where Excel files are stored
        data_folder = os.path.join(settings.BASE_DIR, 'datasets')

        # File 1: main budget dataset
        file1 = os.path.join(data_folder, 'ZEDW_BUDGET_DASH_V.xlsx')
        df1 = pd.read_excel(file1, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df1)} rows from {file1}"))
        self.stdout.write(str(df1.head()))

        # File 2: other budget dataset
        file2 = os.path.join(data_folder, 'ZEDW_BUDGET_DASH_OTHER_V.xlsx')
        df2 = pd.read_excel(file2, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df2)} rows from {file2}"))
        self.stdout.write(str(df2.head()))

        # File 3: pr release pending live dataset
        file3 = os.path.join(data_folder, 'PR_REL_PEND_LIVE.xlsx')
        df3 = pd.read_excel(file3, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df3)} rows from {file3}"))
        self.stdout.write(str(df3.head()))

        # File 4: pr enquiry status live dataset
        file4 = os.path.join(data_folder, 'PR_ENQ_STATUS_LIVE.xlsx')
        df4 = pd.read_excel(file4, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df4)} rows from {file4}"))
        self.stdout.write(str(df4.head()))

        # File 5: pr po status live dataset
        file5 = os.path.join(data_folder, 'PEND_PO_STATUS_LIVE.xlsx')
        df5 = pd.read_excel(file5, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df5)} rows from {file5}"))
        self.stdout.write(str(df5.head()))

        # File 6: inventory dataset
        file6 = os.path.join(data_folder, 'INVENTORY.xlsx')
        df6 = pd.read_excel(file6, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df6)} rows from {file6}"))
        self.stdout.write(str(df6.head()))

        # File 7: stock erp dataset
        file7 = os.path.join(data_folder, 'STOCK_ERP.xlsx')
        df7 = pd.read_excel(file7, engine='openpyxl')
        self.stdout.write(self.style.WARNING(f"Loaded {len(df7)} rows from {file7}"))
        self.stdout.write(str(df7.head()))

        self.stdout.write(self.style.SUCCESS("✅ All datasets loaded into DataFrames"))

        # Get MySQL DB connection info from Django settings
        db_settings = settings.DATABASES['default']
        user = db_settings['USER']
        password = quote_plus(db_settings['PASSWORD'])   # << wrap here
        host = db_settings['HOST'] or 'localhost'
        port = db_settings.get('PORT') or '3306'
        database = db_settings['NAME']

        # Build the SQLAlchemy connection string
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        # Create SQLAlchemy engine
        engine = create_engine(connection_string)

        # Write DataFrame to MySQL table (replace if exists)
        df1.to_sql(name='zedw_budget_dash_v', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'zedw_budget_dash_v' table updated"))

        df2.to_sql(name='zedw_budget_dash_other_v', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'zedw_budget_dash_other_v' table updated"))

        df3.to_sql(name='pr_rel_pend_live', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'pr_rel_pend_live' table updated"))

        df4.to_sql(name='pr_enq_status_live', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'pr_enq_status_live' table updated"))

        df5.to_sql(name='pend_po_status_live', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'pend_po_status_live' table updated"))

        df6.to_sql(name='inventory', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'inventory' table updated"))

        df7.to_sql(name='stock_erp', con=engine, if_exists='replace', index=False)
        self.stdout.write(self.style.SUCCESS("✅ 'stock_erp' table updated"))

        self.stdout.write(self.style.SUCCESS("🎉 All datasets loaded successfully!"))