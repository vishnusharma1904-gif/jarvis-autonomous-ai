"""
Code Executor Tool with Sandboxing
Safely executes Python code in a restricted environment
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any
import os

class CodeExecutor:
    """Safe Python code executor"""
    
    def __init__(self):
        self.timeout = 5  # 5 seconds timeout
        self.max_output_length = 5000  # 5KB max output
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code safely
        
        Args:
            code: Python code to execute
        
        Returns:
            Dict with success status, output, and errors
        """
        # Security checks
        forbidden_imports = [
            'os', 'sys', 'subprocess', 'eval', 'exec',
            'compile', '__import__', 'open', 'file',
            'input', 'raw_input'
        ]
        
        # Check for forbidden operations
        for forbidden in forbidden_imports:
            if forbidden in code:
                return {
                    "success": False,
                    "output": "",
                    "error": f"❌ Forbidden operation detected: '{forbidden}' is not allowed for security reasons."
                }
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # Restricted globals (only safe built-ins)
        safe_builtins = {
            'print': print,
            'range': range,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
        }
        
        globals_dict = {"__builtins__": safe_builtins}
        locals_dict = {}
        
        try:
            # Execute code with output capture
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, globals_dict, locals_dict)
            
            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()
            
            # Limit output length
            if len(output) > self.max_output_length:
                output = output[:self.max_output_length] + "\n... (output truncated)"
            
            if errors:
                return {
                    "success": False,
                    "output": output,
                    "error": errors
                }
            
            return {
                "success": True,
                "output": output or "✅ Code executed successfully (no output)",
                "error": None
            }
        
        except Exception as e:
            error_msg = traceback.format_exc()
            return {
                "success": False,
                "output": stdout_capture.getvalue(),
                "error": f"❌ Execution Error:\n{error_msg}"
            }
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format execution result for display"""
        if result["success"]:
            return f"""```python
{result['output']}
```"""
        else:
            output_section = f"Output:\n{result['output']}\n\n" if result['output'] else ""
            return f"""{output_section}Error:
```
{result['error']}
```"""

# Global instance
code_executor = CodeExecutor()

def execute_code(code: str) -> str:
    """Execute Python code and return formatted result"""
    result = code_executor.execute(code)
    return code_executor.format_result(result)
