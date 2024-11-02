import os
import shutil


def main():
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("Copied .env.example to .env. Please fill in your credentials.")

    print("Installing required packages...")
    os.system("pip install -r requirements.txt")

    print("Setup complete! Update your .env file with the required keys.")


if __name__ == "__main__":
    main()
