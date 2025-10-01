# -------------------- Step 2: File reading --------------------
import json
import csv
import yaml
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import time
from typing import TypedDict
from collections import namedtuple
from dataclasses import dataclass
from pydantic import BaseModel

print("==== STEP 2: Reading Files ====")

# JSON
with open("users.json", "r") as file:
    users_json = json.load(file)
print("JSON data:", users_json)

# CSV
with open("users.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    users_csv = [row for row in reader]
print("CSV data:", users_csv)

# YAML
with open("users.yaml", "r") as file:
    users_yaml = yaml.safe_load(file)
print("YAML data:", users_yaml)

# XML
tree = ET.parse("users.xml")
root = tree.getroot()
users_xml = []
for user in root.findall("user"):
    u = {
        "id": int(user.find("id").text),
        "name": user.find("name").text,
        "email": user.find("email").text,
        "age": int(user.find("age").text)
    }
    users_xml.append(u)
print("XML data:", users_xml)


# -------------------- Step 3: User structures --------------------
print("\n==== STEP 3: User Structures ====")

# TypedDict
class UserTypedDict(TypedDict):
    id: int
    name: str
    email: str
    age: int

# namedtuple
UserNamedTuple = namedtuple("UserNamedTuple", ["id", "name", "email", "age"])

# dataclass
@dataclass
class UserDataClass:
    id: int
    name: str
    email: str
    age: int

# Pydantic
class UserPydantic(BaseModel):
    id: int
    name: str
    email: str
    age: int

# Example
user1_td: UserTypedDict = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25}
user1_nt = UserNamedTuple(1, "Alice", "alice@example.com", 25)
user1_dc = UserDataClass(1, "Alice", "alice@example.com", 25)
user1_pd = UserPydantic(id=1, name="Alice", email="alice@example.com", age=25)

print("TypedDict:", user1_td)
print("NamedTuple:", user1_nt)
print("Dataclass:", user1_dc)
print("Pydantic:", user1_pd)


# -------------------- Step 4: Lists and arrays --------------------
print("\n==== STEP 4: Python List and NumPy Array ====")
numbers_list = [1, 2, 3, 4, 5]
numbers_array = np.array([1, 2, 3, 4, 5])
print("Python list:", numbers_list)
print("NumPy array:", numbers_array)


# -------------------- Step 5: Timer decorator --------------------
print("\n==== STEP 5: Timer Decorator ====")
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


# -------------------- Step 6: Scalar-vector multiplication --------------------
print("\n==== STEP 6: Scalar-Vector Multiplication ====")

@timer
def multiply_list(lst, scalar):
    return [x * scalar for x in lst]

@timer
def multiply_numpy(arr, scalar):
    return arr * scalar

multiply_list(numbers_list, 10)
multiply_numpy(numbers_array, 10)


# -------------------- Step 7: Load CSV into Pandas --------------------
print("\n==== STEP 7: Load CSV into Pandas ====")
df = pd.read_csv("users.csv")
print(df)