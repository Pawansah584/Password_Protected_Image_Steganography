from encoder_decoder import encode_message_cli, decode_message_cli
from auth import register_user, login_user, reset_password, is_valid_password

def start_cli():
    """Starts CLI mode for authentication and message encoding/decoding."""
    print("🔒 Welcome to the Password-Protected Image Steganography System!")

    while True:
        print("\n1️⃣ Register")
        print("2️⃣ Login")
        print("3️⃣ Reset Password")
        print("4️⃣ Encode a message")
        print("5️⃣ Decode a message")
        print("6️⃣ Exit")

        choice = input("Choose (1/2/3/4/5/6): ").strip()

        if choice == "1":
            username = input("Enter a username: ").strip()
            password = input("Enter a password (8+ characters, upper, lower, digit, special symbol): ").strip()
            confirm_password = input("Confirm your password: ").strip()

            if password != confirm_password:
                print("❌ Passwords do not match. Please try again.")
                continue

            is_valid, msg = is_valid_password(password)
            if not is_valid:
                print(f"❌ {msg}")
                continue

            success, msg = register_user(username, password, confirm_password)
            print(f"✅ {msg}" if success else f"❌ {msg}")

        elif choice == "2":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            success, msg = login_user(username, password)
            print(f"✅ {msg}" if success else f"❌ {msg}")

        elif choice == "3":
            username = input("Enter your username: ").strip()
            new_password = input("Enter a new password (8+ characters, upper, lower, digit, special symbol): ").strip()
            confirm_password = input("Confirm your new password: ").strip()

            if new_password != confirm_password:
                print("❌ Passwords do not match. Please try again.")
                continue

            is_valid, msg = is_valid_password(new_password)
            if not is_valid:
                print(f"❌ {msg}")
                continue

            success, msg = reset_password(username, new_password, confirm_password)
            print(f"✅ {msg}" if success else f"❌ {msg}")

        elif choice == "4":
            encode_message_cli()

        elif choice == "5":
            decode_message_cli()

        elif choice == "6":
            print("👋 Exiting CLI mode. Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    start_cli()
