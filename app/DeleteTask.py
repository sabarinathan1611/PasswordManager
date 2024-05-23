import sqlite3
import os

def delete_user_files_and_data():
  
        # Absolute path to the SQLite database file
        db_path = os.path.abspath('./instance/database.db')
        
        # Check if the database file exists
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}")
            return

        # Connect to the SQLite database
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA busy_timeout = 30000")  # Wait up to 30 seconds if the database is locked
            cursor = conn.cursor()

            try:
                # Print all table names and their structure
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    print(f"\nTable: {table_name}")
                    
                    # Get and print the table structure
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    print("Structure:")
                    for column in columns:
                        print(f"  {column[1]} ({column[2]})")
                    
                    # Get and print the table data
                    cursor.execute(f"SELECT * FROM {table_name};")
                    rows = cursor.fetchall()
                    print("Data:")
                    for row in rows:
                        print(f"  {row}")

                # Get the user IDs from delete_account where deleted is False
                cursor.execute("SELECT user_id FROM delete_account WHERE deleted = 0")
                users_to_delete = cursor.fetchall()
                
                # Extract user IDs from the query result
                user_ids = [user[0] for user in users_to_delete]
                print("WORK")
                
                for user_id in user_ids:
                    # Load user data from User table
                    cursor.execute("SELECT username, email FROM User WHERE id = ?", (user_id,))
                    user = cursor.fetchone()
                    
                    if user:
                        username, email = user
                        # Print user details
                        print(f"User: {username}, Email: {email}")

                        # Load and delete related files
                        cursor.execute("SELECT id, filepath, private_key_path, public_key_path FROM File WHERE user_id = ?", (user_id,))
                        files = cursor.fetchall()

                        for file in files:
                            file_id, filepath, private_key_path, public_key_path = file
                            try:
                                # Decrypt and print file details
                                decrypted_filepath = aes_cipher.decrypt_data(filepath)
                                decrypted_private_key_path = aes_cipher.decrypt_data(private_key_path)
                                decrypted_public_key_path = aes_cipher.decrypt_data(public_key_path)
                                print(f"Deleting file: {decrypted_filepath}")

                                if os.path.exists(decrypted_private_key_path):
                                    os.remove(decrypted_private_key_path)
                                else:
                                    print(f"File not found: {decrypted_private_key_path}")

                                if os.path.exists(decrypted_public_key_path):
                                    os.remove(decrypted_public_key_path)
                                else:
                                    print(f"File not found: {decrypted_public_key_path}")

                                if os.path.exists(decrypted_filepath):
                                    os.remove(decrypted_filepath)
                                else:
                                    print(f"File not found: {decrypted_filepath}")
                            except Exception as e:
                                print(f"Error deleting file {decrypted_filepath}: {e}")

                        # Load and delete related texts
                        cursor.execute("SELECT id, private_key_path, public_key_path FROM Text WHERE user_id = ?", (user_id,))
                        texts = cursor.fetchall()
                        for text in texts:
                            text_id, private_key_path, public_key_path = text
                            try:
                                # Decrypt and delete text keys
                                decrypted_private_key_path = aes_cipher.decrypt_data(private_key_path)
                                decrypted_public_key_path = aes_cipher.decrypt_data(public_key_path)

                                if os.path.exists(decrypted_private_key_path):
                                    os.remove(decrypted_private_key_path)
                                else:
                                    print(f"File not found: {decrypted_private_key_path}")

                                if os.path.exists(decrypted_public_key_path):
                                    os.remove(decrypted_public_key_path)
                                else:
                                    print(f"File not found: {decrypted_public_key_path}")
                            except Exception as e:
                                print(f"Error deleting text keys for text ID {text_id}: {e}")

                        # Delete the user and associated data from the database
                        cursor.execute("DELETE FROM File WHERE user_id = ?", (user_id,))
                        cursor.execute("DELETE FROM Text WHERE user_id = ?", (user_id,))
                        cursor.execute("DELETE FROM User WHERE id = ?", (user_id,))
                        conn.commit()

                    else:
                        print(f"User with ID {user_id} not found")

                # Update delete_account table to set deleted to True
                cursor.executemany("UPDATE delete_account SET deleted = 1 WHERE user_id = ?", [(user_id,) for user_id in user_ids])
                conn.commit()

                print("Processing completed.")

            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()

            finally:
                conn.close()

        except sqlite3.OperationalError as e:
            print(f"Database connection failed: {e}")
