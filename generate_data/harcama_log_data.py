import random
import pandas as pd
from datetime import datetime, timedelta

turkish_months = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}

def generate_data(start_date, num_days, num_records, categories, transaction_types, skew=False):
    data = {
        "Yıl": [],
        "Ay": [],
        "Gün": [],
        "Tarih": [],
        "İşlem Türü": [],
        "Tutar": [],
        "Harcama Kategorisi": [],
        "Açıklama": []
    }

    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, num_days - 1))
        transaction_type = random.choice(transaction_types)
        category = random.choice(list(categories.keys()))
        description = random.choice(categories[category])
        
        # Skew data for specified months
        if skew:
            amount = round(random.uniform(1000, 5000), 2) if random.random() < 0.2 else round(random.uniform(10, 500), 2)
            if random.random() < 0.1:
                description = "Unusual Expense"
        else:
            amount = round(random.uniform(10, 500), 2)
        
        data["Tarih"].append(date.strftime("%Y-%m-%d"))
        data["Yıl"].append(date.year)
        data["Ay"].append(turkish_months[date.month])  # Türkçe ay ismini ekliyoruz
        data["Gün"].append(date.day)
        data["İşlem Türü"].append(transaction_type)
        data["Tutar"].append(amount)
        data["Harcama Kategorisi"].append(category)
        data["Açıklama"].append(description)
    
    return pd.DataFrame(data)

# Define categories and transaction types for different months
categories_jan = {
    "Market": ["Migros", "Carrefour", "BIM"],
    "Fatura Ödemesi": ["Elektrik", "Su", "İnternet"],
    "ATM": ["ATM Çekimi"],
    "Restoran": ["Kebapçı", "Pizza", "Cafe"],
    "Ulaşım": ["Otobüs", "Taksi", "Tren"]
}
transaction_types_jan = ["Alışveriş", "Fatura Ödemesi", "ATM Çekimi", "Restoran", "Ulaşım"]

categories_feb = {
    "Market": ["A101", "Şok", "Metro"],
    "Eğlence": ["Sinema", "Tiyatro", "Konser"],
    "ATM": ["ATM Çekimi"],
    "Restoran": ["Burger", "Sushi", "Pasta"],
    "Sağlık": ["Doktor", "Eczane"]
}
transaction_types_feb = ["Alışveriş", "Eğlence", "ATM Çekimi", "Restoran", "Sağlık"]

categories_mar = {
    "Giyim": ["Zara", "H&M", "LC Waikiki"],
    "Fatura Ödemesi": ["Doğalgaz", "Su", "Elektrik"],
    "ATM": ["ATM Çekimi"],
    "Kafe": ["Starbucks", "Gloria Jeans", "Kahve Dünyası"],
    "Seyahat": ["Uçak", "Otobüs", "Tren"]
}
transaction_types_mar = ["Alışveriş", "Fatura Ödemesi", "ATM Çekimi", "Kafe", "Seyahat"]

categories_apr = {
    "Eğitim": ["Kurs", "Seminer", "Kitap"],
    "Fatura Ödemesi": ["Telefon", "İnternet", "Su"],
    "ATM": ["ATM Çekimi"],
    "Restoran": ["Fast Food", "Fine Dining", "Cafe"],
    "Spor": ["Spor Salonu", "Ekipman", "Üyelik"]
}
transaction_types_apr = ["Alışveriş", "Eğitim", "Fatura Ödemesi", "Restoran", "Spor"]

# Generating data for each month
start_date_jan = datetime(2024, 1, 1)
df_jan = generate_data(start_date_jan, 31, 500, categories_jan, transaction_types_jan)

start_date_feb = datetime(2024, 2, 1)
df_feb = generate_data(start_date_feb, 29, 300, categories_feb, transaction_types_feb, skew=True)

start_date_mar = datetime(2024, 3, 1)
df_mar = generate_data(start_date_mar, 31, 600, categories_mar, transaction_types_mar)

start_date_apr = datetime(2024, 4, 1)
df_apr = generate_data(start_date_apr, 30, 400, categories_apr, transaction_types_apr, skew=True)

# Merging the dataframes
merged_df = pd.concat([df_jan, df_feb, df_mar, df_apr])

# Saving the merged dataframe to CSV
merged_df.to_csv("harcama_gecmisi_ocak_subat_mart_nisan_final.csv", index=False)

print("Done!!!")
