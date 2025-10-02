from ucimlrepo import fetch_ucirepo
from minio_utils import upload_to_minio 
from utils import prepare_path

output_path = prepare_path("data", "raw", "diabetes.csv")

# fetch dataset
diabetes_130_us_hospitals_for_years_1999_2008 = fetch_ucirepo(id=296)

# data (as pandas dataframes) 
X = diabetes_130_us_hospitals_for_years_1999_2008.data.features 
y = diabetes_130_us_hospitals_for_years_1999_2008.data.targets 
  
# Create dataset
data = X.copy()
data["readmitted"] = y["readmitted"]

# upload to minio
# data.to_csv(output_path, index=False)
upload_to_minio(str(output_path), "diabetes", "raw/diabetes.csv")