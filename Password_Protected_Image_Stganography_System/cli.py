from encoder_decoder import encode_message_cli, decode_message_cli
from auth import register_user, login_user

def start_cli():
    """Starts CLI mode for authentication and message encoding/decoding."""
    print("🔒 Welcome to the Password-Protected Image Steganography System!")

    while True:
        print("\n1️⃣ Register")
        print("2️⃣ Login")
        print("3️⃣ Encode a message")
        print("4️⃣ Decode a message")
        print("5️⃣ Exit")

        choice = input("Choose (1/2/3/4/5): ").strip()

        if choice == "1":
            username = input("Enter a username: ").strip()
            password = input("Enter a password (8+ characters, upper, lower, digit, special symbol): ").strip()
            if register_user(username, password):
                print("✅ Registration successful!")
            else:
                print("❌ Registration failed. Please try again.")
        
        elif choice == "2":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            if login_user(username, password):
                print("✅ Login successful!")
            else:
                print("❌ Invalid username or password.")
        
        elif choice == "3":
            encode_message_cli()
        
        elif choice == "4":
            decode_message_cli()
        
        elif choice == "5":
            print("👋 Exiting CLI mode. Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 5.")

