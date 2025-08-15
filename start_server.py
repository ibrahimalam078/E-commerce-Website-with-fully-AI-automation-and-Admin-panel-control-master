"""
Background Flask server launcher for API testing
This allows us to programmatically start/stop the server for testing
"""
import subprocess
import time
import requests
import threading
import os
import signal
from pathlib import Path

class FlaskServerManager:
    def __init__(self, port=5000):
        self.port = port
        self.process = None
        self.base_url = f"http://127.0.0.1:{port}"
        
    def start(self, timeout=30):
        """Start the Flask server"""
        print("🚀 Starting Flask server...")
        
        # Start the server process
        try:
            self.process = subprocess.Popen(
                ["python", "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            
            # Wait for server to be ready
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Flask server is running at {self.base_url}")
                        return True
                except requests.exceptions.RequestException:
                    time.sleep(1)
                    continue
            
            print("❌ Failed to start Flask server within timeout")
            self.stop()
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {str(e)}")
            return False
    
    def stop(self):
        """Stop the Flask server"""
        if self.process:
            print("🛑 Stopping Flask server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
            print("✅ Flask server stopped")
    
    def is_running(self):
        """Check if server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

def main():
    """Test the server manager"""
    server = FlaskServerManager()
    
    try:
        if server.start():
            print("\n🧪 Testing server functionality...")
            
            # Test health endpoint
            response = requests.get(f"{server.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                data = response.json()
                print(f"   Status: {data['status']}")
                print(f"   Services: {data['services']}")
            
            print("\n✅ Server is ready for API testing!")
            print(f"   Base URL: {server.base_url}")
            print("   Press Ctrl+C to stop the server")
            
            # Keep server running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Received interrupt signal")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        server.stop()

if __name__ == "__main__":
    main()
