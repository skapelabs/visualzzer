#!/usr/bin/env python3
"""
Demo of the user input functionality for the sorting visualizer.
This shows how the input mechanism works before pygame is available.
"""

import random

def gen_random_list(n):
    return [random.randint(5, 100) for _ in range(n)]

def get_user_input():
    """Get user input for custom numbers"""
    print("\n" + "="*60)
    print("SORTING ALGORITHM VISUALIZER")
    print("="*60)
    print("Enter your own numbers to sort, or press Enter for random numbers.")
    print("• Separate numbers with spaces or commas")
    print("• Maximum 25 numbers allowed")
    print("• Numbers should be between 1 and 1000")
    print("="*60)
    
    while True:
        user_input = input("\nEnter numbers (or press Enter for random): ").strip()
        
        if not user_input:
            # User wants random numbers
            print("Generating random numbers...")
            return gen_random_list(25)
        
        # Parse input - handle both spaces and commas
        try:
            # Replace commas with spaces and split
            numbers_str = user_input.replace(',', ' ').split()
            
            if not numbers_str:
                print("Please enter at least one number.")
                continue
            
            # Convert to integers
            numbers = []
            for num_str in numbers_str:
                try:
                    num = int(num_str)
                    if num < 1 or num > 1000:
                        print(f"Number {num} is out of range (1-1000). Please try again.")
                        break
                    numbers.append(num)
                except ValueError:
                    print(f"'{num_str}' is not a valid number. Please try again.")
                    break
            else:
                # All numbers were valid
                if len(numbers) > 25:
                    print(f"Too many numbers ({len(numbers)}). Using first 25 numbers.")
                    numbers = numbers[:25]
                
                print(f"Using {len(numbers)} numbers: {numbers}")
                return numbers
                
        except Exception as e:
            print(f"Error parsing input: {e}. Please try again.")
            continue

def main():
    """Demo the input functionality"""
    print("This is a demo of the user input functionality.")
    print("In the full visualizer, this would be followed by the pygame window.")
    
    # Get user input
    numbers = get_user_input()
    
    print(f"\nDemo complete! The visualizer would now display {len(numbers)} numbers:")
    print(f"Numbers: {numbers}")
    print(f"Min: {min(numbers)}, Max: {max(numbers)}")
    print(f"Sum: {sum(numbers)}")
    
    print("\nThe pygame window would then open with these numbers ready to sort!")

if __name__ == "__main__":
    main()

