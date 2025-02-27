from encoder_decoder import encode_message_cli, decode_message_cli

def start_cli():
    """Starts CLI mode for encoding/decoding."""
    while True:
        choice = input("\n1️⃣ Encode a message\n2️⃣ Decode a message\n3️⃣ Exit\nChoose (1/2/3): ").strip()
        if choice == "1":
            encode_message_cli()
        elif choice == "2":
            decode_message_cli()
        elif choice == "3":
            print("👋 Exiting CLI mode. Goodbye!"); break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")
