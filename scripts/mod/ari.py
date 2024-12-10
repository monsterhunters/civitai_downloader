import os
import platform
import subprocess

def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def check_aria2_installed():
    try:
        subprocess.run(["aria2c", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_aria2():
    if is_colab():
        print("Installing aria2 in Google Colab...")
        try:
            subprocess.run(["apt-get", "install", "-y", "aria2"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing aria2 in Colab: {e}")
        return

    os_name = platform.system()
    if os_name == "Windows":
        print("Installing aria2 on Windows...")
        try:
            subprocess.run(["winget", "install", "--id", "aria2.aria2", "-e"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing aria2: {e}")
    elif os_name == "Linux":
        print("Installing aria2 on Linux...")
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", "aria2"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing aria2: {e}")
    elif os_name == "Darwin":  # macOS
        print("Installing aria2 on macOS...")
        try:
            subprocess.run(["brew", "install", "aria2"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing aria2: {e}")
    else:
        raise RuntimeError(f"Unsupported operating system: {os_name}")

if __name__ == "__main__":
    if not check_aria2_installed():
        install_aria2()
    else:
        print("aria2 is already installed.")
