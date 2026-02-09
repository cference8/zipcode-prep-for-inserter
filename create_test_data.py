import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'ZIP': ['12345', '12345-6789', '98765-4321', 12345],
    'Other': ['foo', 'bar', 'baz', 'qux']
}

df = pd.DataFrame(data)
df.to_excel('test_data.xlsx', index=False)
print("Created test_data.xlsx")
