#!/usr/bin/env python3
"""
PyQt5 version of the user input functionality for the sorting visualizer.
This shows how the input mechanism would work with PyQt5.
"""

import sys
import random
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def gen_random_list(n):
    return [random.randint(5, 100) for _ in range(n)]

class NumberInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.numbers = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Sorting Algorithm Visualizer - Number Input")
        self.setFixedSize(500, 400)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Enter Your Numbers")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Enter numbers to sort, or leave empty for random numbers.\n"
            "• Separate numbers with spaces or commas\n"
            "• Maximum 25 numbers allowed\n"
            "• Numbers should be between 1 and 1000\n\n"
            "Examples: 10 5 8 3 7  or  10,5,8,3,7"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(instructions)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter numbers here...")
        self.input_field.setFont(QFont("Monaco", 12))
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.random_button = QPushButton("Use Random Numbers")
        self.random_button.clicked.connect(self.use_random)
        button_layout.addWidget(self.random_button)
        
        self.ok_button = QPushButton("Use These Numbers")
        self.ok_button.clicked.connect(self.validate_and_accept)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Preview area
        self.preview = QTextEdit()
        self.preview.setMaximumHeight(100)
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Preview of entered numbers will appear here...")
        layout.addWidget(self.preview)
        
        # Connect input field to preview
        self.input_field.textChanged.connect(self.update_preview)
        
        self.setLayout(layout)
        
        # Set focus to input field
        self.input_field.setFocus()
    
    def update_preview(self):
        """Update the preview area as user types"""
        text = self.input_field.text().strip()
        if not text:
            self.preview.clear()
            return
        
        try:
            # Parse input
            numbers_str = text.replace(',', ' ').split()
            numbers = []
            errors = []
            
            for num_str in numbers_str:
                try:
                    num = int(num_str)
                    if num < 1 or num > 1000:
                        errors.append(f"{num} (out of range)")
                    else:
                        numbers.append(num)
                except ValueError:
                    errors.append(f"'{num_str}' (not a number)")
            
            # Update preview
            if errors:
                preview_text = f"Errors found:\n" + "\n".join(errors)
                self.preview.setStyleSheet("color: red;")
            else:
                if len(numbers) > 25:
                    preview_text = f"Too many numbers ({len(numbers)}). Will use first 25:\n{numbers[:25]}"
                    self.preview.setStyleSheet("color: orange;")
                else:
                    preview_text = f"Valid numbers ({len(numbers)}):\n{numbers}"
                    self.preview.setStyleSheet("color: green;")
            
            self.preview.setText(preview_text)
            
        except Exception:
            self.preview.setText("Error parsing input")
            self.preview.setStyleSheet("color: red;")
    
    def use_random(self):
        """Use random numbers"""
        self.numbers = gen_random_list(25)
        self.accept()
    
    def validate_and_accept(self):
        """Validate input and accept if valid"""
        text = self.input_field.text().strip()
        
        if not text:
            # Empty input - use random
            self.use_random()
            return
        
        try:
            # Parse input
            numbers_str = text.replace(',', ' ').split()
            
            if not numbers_str:
                QMessageBox.warning(self, "Error", "Please enter at least one number.")
                return
            
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
                QMessageBox.critical(self, "Invalid Input", 
                                   f"Invalid numbers found:\n" + "\n".join(invalid_numbers) + 
                                   "\n\nPlease try again with valid numbers (1-1000).")
                return
            
            # All numbers were valid
            if len(numbers) > 25:
                reply = QMessageBox.question(self, "Too Many Numbers", 
                                           f"You entered {len(numbers)} numbers.\n"
                                           f"Use the first 25 numbers?",
                                           QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    numbers = numbers[:25]
                else:
                    return
            
            # Show confirmation
            reply = QMessageBox.question(self, "Confirm Numbers", 
                                       f"Use these {len(numbers)} numbers?\n\n{numbers}",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.numbers = numbers
                self.accept()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error parsing input: {e}\nPlease try again.")

def get_user_input_pyqt5():
    """Get user input using PyQt5 dialog"""
    app = QApplication(sys.argv)
    
    dialog = NumberInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.numbers
    else:
        return gen_random_list(25)  # Default to random if cancelled

def main():
    """Demo the PyQt5 input functionality"""
    print("This is a demo of the PyQt5 input functionality.")
    print("In the full visualizer, this would be followed by the pygame window.")
    
    # Get user input
    numbers = get_user_input_pyqt5()
    
    print(f"\nDemo complete! The visualizer would now display {len(numbers)} numbers:")
    print(f"Numbers: {numbers}")
    print(f"Min: {min(numbers)}, Max: {max(numbers)}")
    print(f"Sum: {sum(numbers)}")
    
    print("\nThe pygame window would then open with these numbers ready to sort!")

if __name__ == "__main__":
    main()

