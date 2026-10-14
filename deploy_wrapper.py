import subprocess
import platform

def deploy_software():
    current_os = platform.system()
    
    if current_os == "Windows":
        # Example using winget to silently install 7-Zip
        cmd = ["winget", "install", "--id", "IgorPavlov.7Zip", "--silent", "--accept-package-agreements", "--accept-source-agreements"]
    elif current_os == "Linux":
        # Example using apt to install htop and curl
        cmd = ["sudo", "apt", "install", "-y", "htop", "curl"]
    else:
        print(f"Unsupported OS: {current_os}")
        return

    print(f"Running deployment command on {current_os}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        print(f"Exit Code: {result.returncode}")
        print(f"Output:\n{result.stdout}")
        
        if result.returncode == 0:
            print("SUCCESS: Package deployed successfully.")
        else:
            print(f"WARNING: Deployment completed with non-zero exit code. Stderr: {result.stderr}")
            
    except FileNotFoundError:
        print("ERROR: Package manager utility (winget/apt) not found on path.")
    except Exception as e:
        print(f"ERROR: Unexpected exception occurred: {e}")

if __name__ == "__main__":
    deploy_software()
