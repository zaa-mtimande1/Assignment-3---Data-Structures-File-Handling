from db import SessionLocal, engine, Base
from crud import get_all_users, get_user_by_username, create_user, update_user_email

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Start database session
db = SessionLocal()


def print_users(users):
    if not users:
        print("No users found.")
        return
    print(f"{'ID':<3} {'Username':<10} {'Email':<25} {'Created At'}")
    print("-" * 50)
    for user in users:
        created = user.created_at.strftime(
            "%Y-%m-%d %H:%M:%S") if user.created_at else "N/A"
        print(f"{user.id:<3} {user.username:<10} {user.email:<25} {created}")


# 1️⃣ Retrieve all users
print("\nAll users in the database:")
all_users = get_all_users(db)
print_users(all_users)

# 2️⃣ Find a user by username
username_to_find = "zaa"
found_user = get_user_by_username(db, username_to_find)
print(f"\nSearch for username '{username_to_find}':")
if found_user:
    print(
        f"Found: ID={found_user.id}, Username={found_user.username}, Email={found_user.email}")
else:
    print("User not found.")

# 3️⃣ Create a new user
new_username = "emma"
new_email = "emma@example.com"
created_user = create_user(db, new_username, new_email)
print(f"\nCreating new user '{new_username}':")
if created_user:
    print(
        f"Created: ID={created_user.id}, Username={created_user.username}, Email={created_user.email}")
else:
    print("Failed to create user.")

# 4️⃣ Update user email
updated_email = "emma_new@example.com"
updated_user = update_user_email(db, new_username, updated_email)
print(f"\nUpdating '{new_username}' email to '{updated_email}':")
if updated_user:
    print(
        f"Updated: ID={updated_user.id}, Username={updated_user.username}, Email={updated_user.email}")
else:
    print("Failed to update user.")

# Close session
db.close()
