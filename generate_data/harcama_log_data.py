import random
import pandas as pd
from datetime import datetime, timedelta


def generate_data(start_date, num_days, num_records):
    data = {
        "Tarih": [],
        "İşlem Türü": [],
        "Tutar": [],
        "Harcama Kategorisi": [],
        "Açıklama": []
    }

    categories = {
        "Market": ["Migros", "Carrefour", "BIM"],
        "Fatura Ödemesi": ["Elektrik", "Su", "İnternet"],
        "ATM": ["ATM Çekimi"],
        "Restoran": ["Kebapçı", "Pizza", "Cafe"],
        "Ulaşım": ["Otobüs", "Taksi", "Tren"]
    }

    transaction_types = ["Alışveriş", "Fatura Ödemesi", "ATM Çekimi", "Restoran", "Ulaşım"]

    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, num_days - 1))
        transaction_type = random.choice(transaction_types)
        category = random.choice(list(categories.keys()))
        description = random.choice(categories[category])
        amount = round(random.uniform(10, 500), 2)
        
        data["Tarih"].append(date.strftime("%Y-%m-%d"))
        data["İşlem Türü"].append(transaction_type)
        data["Tutar"].append(amount)
        data["Harcama Kategorisi"].append(category)
        data["Açıklama"].append(description)
    
    return pd.DataFrame(data)

# Generating January 2024 data
start_date_2024 = datetime(2024, 1, 1)
df_2024 = generate_data(start_date_2024, 30, 500)

# Generating February 2024 data
start_date_feb_2024 = datetime(2024, 2, 1)
df_feb_2024 = generate_data(start_date_feb_2024, 28, 500)

# Merging the two dataframes
merged_df = pd.concat([df_2024, df_feb_2024])

# Saving the merged dataframe to CSV
merged_df.to_csv("harcama_gecmisi_ocak_subat.csv", index=False)

print("Done!!!")
