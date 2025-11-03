#!/usr/bin/env python3
"""
AI Response Viewer - PyQt5 application to display AI responses with proper markdown rendering
"""
import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import our markdown viewer
from markdown_viewer_pyqt import show_markdown

class AIResponseViewer(QMainWindow):
    """Main window for the AI Response Viewer application"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Response Viewer")
        self.setMinimumSize(600, 200)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("AI Response Viewer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Description
        description = QLabel("Enter your question about data structures and algorithms below:")
        description.setWordWrap(True)
        main_layout.addWidget(description)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your question here...")
        self.input_field.setMinimumHeight(40)
        self.input_field.returnPressed.connect(self.send_request)
        main_layout.addWidget(self.input_field)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Submit button
        self.submit_button = QPushButton("Ask AI")
        self.submit_button.setMinimumHeight(40)
        self.submit_button.clicked.connect(self.send_request)
        button_layout.addWidget(self.submit_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Set main widget
        self.setCentralWidget(main_widget)
    
    def send_request(self):
        """Send the question to the API and display the response"""
        question = self.input_field.text().strip()
        
        if not question:
            QMessageBox.warning(self, "Empty Question", "Please enter a question.")
            return
        
        try:
            # Disable input while waiting for response
            self.input_field.setEnabled(False)
            self.submit_button.setEnabled(False)
            self.submit_button.setText("Loading...")
            
            # Send request to API
            response = requests.post(
                'http://localhost:9090/api/ask_ai',
                json={"question": question},
                timeout=30
            )
            
            # Process response
            if response.status_code == 200:
                data = response.json()
                markdown_response = data.get('response', 'No response received')
                
                # Show the response in the markdown viewer
                show_markdown(markdown_response)
            else:
                error_message = f"Error: {response.status_code}\n{response.text}"
                QMessageBox.critical(self, "API Error", error_message)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable input
            self.input_field.setEnabled(True)
            self.submit_button.setEnabled(True)
            self.submit_button.setText("Ask AI")
            self.input_field.selectAll()
            self.input_field.setFocus()

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    viewer = AIResponseViewer()
    viewer.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()