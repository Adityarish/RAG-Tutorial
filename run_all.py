import subprocess
import os
import signal
import sys
import time

# Define paths
BACKEND_DIR = os.path.join(os.getcwd(), "backend")
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")

# Define commands
BACKEND_CMD = ["python", "app.py"]
FRONTEND_CMD = ["npm", "start"]

# Track processes
processes = []

def run_process(cmd, cwd):
    """Run a subprocess in the specified directory."""
    return subprocess.Popen(cmd, cwd=cwd)

def main():
    try:
        print("🚀 Starting Flask backend...")
        backend_proc = run_process(BACKEND_CMD, BACKEND_DIR)
        processes.append(backend_proc)

        # Wait a bit for backend to start before frontend
        time.sleep(3)

        print("🌐 Starting React frontend...")
        frontend_proc = run_process(FRONTEND_CMD, FRONTEND_DIR)
        processes.append(frontend_proc)

        print("\n✅ Both servers are running!")
        print("Backend: http://localhost:5001")
        print("Frontend: http://localhost:3000\n")

        # Keep script alive until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        for p in processes:
            p.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
