#!/usr/bin/env python3
"""
Test the tkinter input dialog functionality
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import random

def gen_random_list(n):
    return [random.randint(5, 100) for _ in range(n)]

def get_user_input():
    """Get user input for custom numbers using tkinter dialog"""
    # Create a root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show welcome message
    messagebox.showinfo("Sorting Algorithm Visualizer", 
                       "Welcome to the Sorting Algorithm Visualizer!\n\n"
                       "You can enter your own numbers or use random numbers.\n"
                       "• Separate numbers with spaces or commas\n"
                       "• Maximum 25 numbers allowed\n"
                       "• Numbers should be between 1 and 1000")
    
    while True:
        # Get user input
        user_input = simpledialog.askstring("Enter Numbers", 
                                          "Enter your numbers (or leave empty for random):\n"
                                          "Examples: 10 5 8 3 7  or  10,5,8,3,7")
        
        if user_input is None:
            # User clicked Cancel - use random numbers
            root.destroy()
            return gen_random_list(25)
        
        if not user_input.strip():
            # User wants random numbers
            root.destroy()
            return gen_random_list(25)
        
        # Parse input - handle both spaces and commas
        try:
            # Replace commas with spaces and split
            numbers_str = user_input.replace(',', ' ').split()
            
            if not numbers_str:
                messagebox.showerror("Error", "Please enter at least one number.")
                continue
            
            # Convert to integers
            numbers = []
            invalid_numbers = []
            
            for num_str in numbers_str:
                try:
                    num = int(num_str)
                    if num < 1 or num > 1000:
                        invalid_numbers.append(f"{num} (out of range 1-1000)")
                    else:
                        numbers.append(num)
                except ValueError:
                    invalid_numbers.append(f"'{num_str}' (not a number)")
            
            if invalid_numbers:
                messagebox.showerror("Invalid Input", 
                                   f"Invalid numbers found:\n" + "\n".join(invalid_numbers) + 
                                   "\n\nPlease try again with valid numbers (1-1000).")
                continue
            
            # All numbers were valid
            if len(numbers) > 25:
                messagebox.showwarning("Too Many Numbers", 
                                     f"You entered {len(numbers)} numbers.\n"
                                     f"Using the first 25 numbers.")
                numbers = numbers[:25]
            
            # Show confirmation
            result = messagebox.askyesno("Confirm Numbers", 
                                       f"Using {len(numbers)} numbers:\n{numbers}\n\n"
                                       f"Proceed with these numbers?")
            
            if result:
                root.destroy()
                return numbers
            else:
                continue  # Let user try again
                
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing input: {e}\nPlease try again.")
            continue

def main():
    """Test the input functionality"""
    print("Testing tkinter input dialog...")
    print("A dialog window should appear now.")
    
    # Get user input
    numbers = get_user_input()
    
    print(f"\nTest complete! Got {len(numbers)} numbers:")
    print(f"Numbers: {numbers}")
    print(f"Min: {min(numbers)}, Max: {max(numbers)}")
    print(f"Sum: {sum(numbers)}")

if __name__ == "__main__":
    main()

