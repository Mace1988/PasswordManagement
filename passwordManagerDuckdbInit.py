import duckdb
duckdb_file="/Users/masonfrance/Projects/PasswordManagement/passwordManager.duckdb"
json_file="/Users/masonfrance/Projects/PasswordManagement/test.json"

conn = duckdb.connect(duckdb_file)

def create_table():
    conn.execute("DROP TABLE IF EXISTS enc_pw;")
    conn.execute("CREATE TABLE enc_pw (user_name VARCHAR, encrypted_password VARCHAR);")


# res = duckdb.execute("""
#     SELECT
#         $my_param,
#         $other_param,
#         $also_param
#     """,
#     {
#         "my_param": 5,
#         "other_param": "DuckDB",
#         "also_param": [42]
#     }
# )

conn.execute("INSERT INTO enc_pw VALUES ('test', 'data');")
conn.execute("SELECT * FROM enc_pw")
print(conn.fetchall())
print(duckdb.read_json(json_file))
# duckdb.execute("INSERT INTO enc_pw SELECT * FROM 'test.json';")

# create_table()

