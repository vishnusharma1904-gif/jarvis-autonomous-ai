"""
Calculator Tool for Mathematical Computations
"""

import math
import operator
from typing import Union

class Calculator:
    """Safe calculator for mathematical operations"""
    
    # Allowed operators
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '**': operator.pow,
        '%': operator.mod,
    }
    
    # Allowed functions
    functions = {
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil,
    }
    
    # Constants
    constants = {
        'pi': math.pi,
        'e': math.e,
    }
    
    @staticmethod
    def calculate(expression: str) -> str:
        """
        Safely evaluate mathematical expression
        
        Args:
            expression: Mathematical expression as string
        
        Returns:
            Result or error message
        """
        try:
            # Simple eval with restricted namespace for safety
            allowed_names = {
                **Calculator.functions,
                **Calculator.constants,
            }
            
            # Remove any potentially dangerous operations
            forbidden = ['import', '__', 'exec', 'eval', 'compile', 'open', 'file']
            for word in forbidden:
                if word in expression.lower():
                    return f"❌ Forbidden operation detected: {word}"
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"✅ Result: {result}"
        
        except ZeroDivisionError:
            return "❌ Error: Division by zero"
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    @staticmethod
    def solve_percentage(value: float, percentage: float) -> str:
        """Calculate percentage of a value"""
        result = (value * percentage) / 100
        return f"{percentage}% of {value} = {result}"
    
    @staticmethod
    def compound_interest(
        principal: float,
        rate: float,
        time: float,
        n: int = 1
    ) -> str:
        """
        Calculate compound interest
        
        Args:
            principal: Principal amount
            rate: Annual interest rate (percentage)
            time: Time in years
            n: Number of times interest applied per year
        
        Returns:
            Formatted result
        """
        amount = principal * (1 + (rate / 100) / n) ** (n * time)
        interest = amount - principal
        
        return f"""💰 Compound Interest Calculation:
Principal: ${principal:,.2f}
Rate: {rate}% per year
Time: {time} years
Compounding: {n} times/year

Final Amount: ${amount:,.2f}
Interest Earned: ${interest:,.2f}"""

def calculate(expression: str) -> str:
    """Wrapper function for calculator"""
    return Calculator.calculate(expression)
