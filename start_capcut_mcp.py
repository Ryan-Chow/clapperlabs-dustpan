#!/usr/bin/env python3
"""
Startup script to ensure capcut-mcp server is running
This handles the integration between our CLI and the original capcut-mcp
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path
from typing import Dict, List, Any

class CapCutMCPManager:
    def __init__(self, capcut_mcp_path: str = "capcut-mcp", port: int = 9000):
        self.capcut_mcp_path = Path(capcut_mcp_path)
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self.server_process = None
    
    def is_server_running(self) -> bool:
        """Check if the capcut-mcp server is already running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def start_server(self) -> bool:
        """Start the capcut-mcp server"""
        
        if self.is_server_running():
            print("✅ CapCut MCP server already running")
            return True
        
        if not self.capcut_mcp_path.exists():
            print(f"❌ capcut-mcp not found at {self.capcut_mcp_path}")
            print("Please run: git clone https://github.com/fancyboi999/capcut-mcp.git capcut-mcp")
            return False
        
        # Check if capcut-mcp has required files
        main_py = self.capcut_mcp_path / "main.py"
        if not main_py.exists():
            print(f"❌ main.py not found in {self.capcut_mcp_path}")
            return False
        
        print("🚀 Starting CapCut MCP server...")
        
        try:
            # Start the server in the capcut-mcp directory
            self.server_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=self.capcut_mcp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=dict(os.environ, PORT=str(self.port))  # Set port if needed
            )
            
            # Wait for server to be ready
            for attempt in range(15):  # Wait up to 15 seconds
                time.sleep(1)
                if self.is_server_running():
                    print("✅ CapCut MCP server started successfully")
                    return True
                
                # Check if process crashed
                if self.server_process.poll() is not None:
                    stdout, stderr = self.server_process.communicate()
                    print(f"❌ Server process crashed:")
                    print(f"STDOUT: {stdout.decode()}")
                    print(f"STDERR: {stderr.decode()}")
                    return False
            
            print("❌ Server failed to start within 15 seconds")
            self.stop_server()
            return False
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the capcut-mcp server"""
        
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("🛑 CapCut MCP server stopped")
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                print("🛑 CapCut MCP server force killed")
            except Exception as e:
                print(f"⚠️ Error stopping server: {e}")
    
    def restart_server(self) -> bool:
        """Restart the capcut-mcp server"""
        self.stop_server()
        time.sleep(2)
        return self.start_server()
    
    def test_api_endpoints(self) -> Dict[str, bool]:
        """Test that all required API endpoints are working"""
        
        if not self.is_server_running():
            return {"server_running": False}
        
        endpoints_to_test = [
            "/add_video",
            "/add_audio", 
            "/add_image",
            "/add_text",
            "/add_subtitle",
            "/add_effect",
            "/add_sticker",
            "/save_draft"
        ]
        
        results = {"server_running": True}
        
        for endpoint in endpoints_to_test:
            try:
                # Test with a minimal POST request (won't actually work but should return valid HTTP response)
                response = requests.post(f"{self.base_url}{endpoint}", json={}, timeout=5)
                # Even if it returns an error, it means the endpoint exists
                results[endpoint] = response.status_code in [200, 400, 422]  # Valid HTTP responses
            except requests.exceptions.RequestException:
                results[endpoint] = False
        
        return results
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get detailed server status information"""
        
        status = {
            "running": self.is_server_running(),
            "process_id": self.server_process.pid if self.server_process else None,
            "url": self.base_url,
            "capcut_mcp_path": str(self.capcut_mcp_path),
            "endpoints_status": {}
        }
        
        if status["running"]:
            status["endpoints_status"] = self.test_api_endpoints()
        
        return status

def main():
    """Main function for testing the server manager"""
    
    manager = CapCutMCPManager()
    
    print("🔧 CapCut MCP Server Manager")
    print("=" * 40)
    
    # Test server startup
    if manager.start_server():
        print("\n🧪 Testing API endpoints...")
        endpoint_status = manager.test_api_endpoints()
        
        print("\n📊 Endpoint Status:")
        for endpoint, working in endpoint_status.items():
            status_icon = "✅" if working else "❌"
            print(f"  {status_icon} {endpoint}")
        
        print(f"\n🌐 Server running at: {manager.base_url}")
        print("Press Ctrl+C to stop the server...")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            manager.stop_server()
    else:
        print("❌ Failed to start CapCut MCP server")
        sys.exit(1)

if __name__ == "__main__":
    main()