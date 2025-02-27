# 🛡️ Password Protected Image Steganography 🔐  

**A secure and user-friendly Image Steganography tool with password protection!**
Supports **both CLI and GUI (Tkinter)** for encoding & decoding hidden messages inside images.

---

## ✨ Features  

✅ **User Authentication** (Login & Register)
✅ **Secure Password-Protected Encoding & Decoding**
✅ **Hide Messages Inside Images** (Steganography)
✅ **CLI and GUI Support** (Tkinter)
✅ **SQLite Database for User Management**

---

## 📌 How It Works  

### 🔑 1. **User Authentication**  
- Users must **register** before using the tool.
- **Login required** to encode/decode messages.

### 🖼️ 2. **Encoding a Secret Message**  
- Select an image 📷.
- Enter a **hidden message** ✍️.
- Set a **password for security** 🔐.
- The tool hides the message **inside the image**.

### 🔓 3. **Decoding the Hidden Message**  
- Select the **encoded image** 📂.
- Enter the **correct password** 🛡️
- Retrieve the **hidden message**! 

---

## 📥 Installation  

### 🔹 **1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo

🔹 2. Install Dependencies
pip install -r requirements.txt

🚀 Usage
🖥️ Run the GUI (Tkinter)

python main.py
A Graphical User Interface will open for encoding/decoding images.
📟 Run the CLI (Command Line Interface)

python cli.py
Use the CLI for quick encoding/decoding without the GUI.

📂 Project Structure

📂 Password-Protected-Image-Steganography
├── auth.py              # Handles user authentication (Login/Register)
├── cli.py               # Command-line interface for steganography
├── encoded_messages.db  # Database storing encoded messages
├── encoder_decoder.py   # Encoding/decoding logic
├── gui.py               # GUI implementation using Tkinter
├── main.py              # Entry point for GUI
├── users.db             # Database storing user credentials
├── sample_files/        # Contains sample images for testing
│   ├── dog&cat.jpg      # Sample image for encoding
│   ├── bear.jpg         # Another test image
│   ├── encoded_image.png # Encoded image with hidden message
│   └── README.md        # Instructions for sample files
├── requirements.txt     # Dependencies
├── README.md            # Project documentation

🔧 Dependencies
Make sure you have Python 3.x installed, then install the following:
Pillow
tk
cryptography
sqlite3
bcrypt
pwinput
customtkinter
pycryptodome

📝 Author
PAWAN KUMAR SAH
BSc (Hons) in Ethical Hacking and Cybersecurity
Coventry University

📜 License
This project is open-source and licensed under the MIT License.

⚠️ Copyright & Warning
© 2024 PAWAN KUMAR SAH. All rights reserved.

🔴 WARNING: Unauthorized reproduction, modification, or distribution of this software without explicit permission is prohibited.

🌟 Show Some Love!
⭐ Star this repository if you found it useful!
🐛 Found a bug? Open an issue!
💡 Have an idea? Contribute to this project!
