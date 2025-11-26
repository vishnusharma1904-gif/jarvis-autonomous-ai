"""
File Manager Tool
Safe file system operations for the agent
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

class FileManager:
    """Safe file manager with sandboxing"""
    
    def __init__(self, sandbox_dir: str = "backend/data/sandbox"):
        """Initialize with sandbox directory"""
        self.sandbox_dir = Path(sandbox_dir).resolve()
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
    
    def _is_safe_path(self, path: str) -> bool:
        """Check if path is within sandbox"""
        try:
            full_path = (self.sandbox_dir / path).resolve()
            return full_path.is_relative_to(self.sandbox_dir)
        except:
            return False
    
    def list_files(self, directory: str = ".") -> str:
        """List files in directory (within sandbox)"""
        if not self._is_safe_path(directory):
            return "❌ Access denied: Path outside sandbox"
        
        try:
            target_dir = self.sandbox_dir / directory
            if not target_dir.exists():
                return f"❌ Directory not found: {directory}"
            
            if not target_dir.is_dir():
                return f"❌ Not a directory: {directory}"
            
            items = []
            for item in sorted(target_dir.iterdir()):
                item_type = "📁" if item.is_dir() else "📄"
                size = f"({item.stat().st_size} bytes)" if item.is_file() else ""
                items.append(f"{item_type} {item.name} {size}")
            
            return "\n".join(items) if items else "Empty directory"
        
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"
    
    def read_file(self, filepath: str) -> str:
        """Read file contents (within sandbox)"""
        if not self._is_safe_path(filepath):
            return "❌ Access denied: Path outside sandbox"
        
        try:
            full_path = self.sandbox_dir / filepath
            if not full_path.exists():
                return f"❌ File not found: {filepath}"
            
            if not full_path.is_file():
                return f"❌ Not a file: {filepath}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit file size
            max_size = 10000  # 10KB
            if len(content) > max_size:
                content = content[:max_size] + "\n... (file truncated)"
            
            return f"📄 Contents of {filepath}:\n\n{content}"
        
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    def write_file(self, filepath: str, content: str) -> str:
        """Write content to file (within sandbox)"""
        if not self._is_safe_path(filepath):
            return "❌ Access denied: Path outside sandbox"
        
        try:
            full_path = self.sandbox_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✅ File written successfully: {filepath}"
        
        except Exception as e:
            return f"❌ Error writing file: {str(e)}"
    
    def delete_file(self, filepath: str) -> str:
        """Delete file (within sandbox)"""
        if not self._is_safe_path(filepath):
            return "❌ Access denied: Path outside sandbox"
        
        try:
            full_path = self.sandbox_dir / filepath
            if not full_path.exists():
                return f"❌ File not found: {filepath}"
            
            if full_path.is_file():
                full_path.unlink()
                return f"✅ File deleted: {filepath}"
            else:
                return f"❌ Not a file: {filepath}"
        
        except Exception as e:
            return f"❌ Error deleting file: {str(e)}"
    
    def create_directory(self, directory: str) -> str:
        """Create directory (within sandbox)"""
        if not self._is_safe_path(directory):
            return "❌ Access denied: Path outside sandbox"
        
        try:
            full_path = self.sandbox_dir / directory
            full_path.mkdir(parents=True, exist_ok=True)
            return f"✅ Directory created: {directory}"
        
        except Exception as e:
            return f"❌ Error creating directory: {str(e)}"

# Global instance
file_manager = FileManager()
