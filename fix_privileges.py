import psycopg2


def fix_privileges():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="responses_test_db",
            user="postgres",
            password="12345"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        privileges_commands = [
            "GRANT ALL PRIVILEGES ON SCHEMA public TO test_user;",
            "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO test_user;",
            "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO test_user;",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO test_user;",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO test_user;"
        ]

        for command in privileges_commands:
            cursor.execute(command)
            print(f"{command.split('TO')[0]}...")

        cursor.close()
        conn.close()
        print("Privileges granted successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    fix_privileges()