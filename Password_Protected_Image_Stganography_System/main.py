import sys
from gui import start_gui
from cli import start_cli

def main():
    while True:
        choice = input("\n1️⃣ GUI Mode\n2️⃣ CLI Mode\n3️⃣ Exit\nChoose (1/2/3): ").strip()
        if choice == "1":
            try: start_gui()
            except Exception as e: print(f"❌ GUI Error: {e}")
        elif choice == "2":
            try: start_cli()
            except Exception as e: print(f"❌ CLI Error: {e}")
        elif choice == "3":
            print("👋 Exiting. Goodbye!"); sys.exit(0)
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
