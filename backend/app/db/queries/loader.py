from pathlib import Path

QUERIES_DIR = Path(__file__).parent


def load_queries() -> dict[str, dict[str, str]]:
    """
    Load all .sql files in the queries folder.
    Returns a nested dict: {filename_without_ext: {query_name: sql_string}}
    """
    all_queries = {}

    for file_path in QUERIES_DIR.glob("*.sql"):
        file_name = file_path.stem  # e.g., 'users', 'items'
        queries = {}
        current_name = None
        current_sql_lines = []

        with file_path.open("r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("-- name:"):
                    # Save previous query
                    if current_name and current_sql_lines:
                        queries[current_name] = "\n".join(current_sql_lines).strip()
                    # Start new query
                    current_name = line.replace("-- name:", "").strip()
                    current_sql_lines = []
                elif line.startswith("--") and current_name:
                    continue
                elif current_name:
                    current_sql_lines.append(line)

            # Save last query in file
            if current_name and current_sql_lines:
                queries[current_name] = "\n".join(current_sql_lines).strip()

        all_queries[file_name] = queries

    return all_queries


# Example usage
if __name__ == "__main__":
    queries = load_queries()
    for file, file_queries in queries.items():
        print(f"File: {file}")
        for name, sql in file_queries.items():
            print(f"  {name}: {sql[:60]}...")  # print first 60 chars
