#!/usr/bin/env python3
"""
AI Markdown Display - PyQt5 window to display AI responses with proper markdown formatting
"""
import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QScrollArea, 
                            QWidget, QTextEdit, QLabel, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CodeBlock(QTextEdit):
    """Widget for displaying code blocks with proper formatting"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 10))
        self.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
            }
        """)
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Set fixed height based on content with some padding
        doc_height = self.document().size().height()
        self.setMinimumHeight(min(int(doc_height + 30), 300))
        
        # Disable text wrapping for code blocks to preserve formatting
        self.setLineWrapMode(QTextEdit.NoWrap)

class TextBlock(QTextEdit):
    """Widget for displaying regular text with proper formatting"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Arial", 11))
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                line-height: 1.4;
                margin: 5px 0;
            }
        """)
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Enable text wrapping for regular text
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Set fixed height based on content
        doc_height = self.document().size().height()
        self.setMinimumHeight(int(doc_height + 20))
        
        # Set document margins
        document = self.document()
        document.setDocumentMargin(10)

class AIMarkdownViewer(QMainWindow):
    """Main window for displaying AI responses with markdown formatting"""
    def __init__(self, markdown_text, title="AI Response"):
        super().__init__()
        self.title = title
        self.init_ui()
        self.render_markdown(markdown_text)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(self.title)
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(0)
        
        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget and layout
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)  # Space between blocks
        
        # Set content widget in scroll area
        self.scroll_area.setWidget(self.content_widget)
        
        # Add scroll area to main layout
        self.main_layout.addWidget(self.scroll_area)
        
        # Set main widget
        self.setCentralWidget(self.main_widget)
    
    def render_markdown(self, markdown_text):
        """Parse and render markdown content"""
        # Split the markdown by code blocks
        parts = re.split(r'(```[\s\S]*?```)', markdown_text)
        
        for part in parts:
            if part.strip():
                if part.startswith('```') and part.endswith('```'):
                    # Code block
                    # Remove the code fence markers and language identifier if present
                    code_content = re.sub(r'^```\w*\n', '', part)
                    code_content = re.sub(r'```$', '', code_content)
                    
                    # Add vertical padding before code block
                    self.content_layout.addSpacing(10)
                    
                    # Add code block
                    code_block = CodeBlock(code_content)
                    self.content_layout.addWidget(code_block)
                    
                    # Add vertical padding after code block
                    self.content_layout.addSpacing(10)
                else:
                    # Regular text
                    text_block = TextBlock(part)
                    self.content_layout.addWidget(text_block)
        
        # Add stretch to push content to the top
        self.content_layout.addStretch()

def display_ai_response(response_text, title="AI Response"):
    """Display AI response with proper markdown formatting"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    viewer = AIMarkdownViewer(response_text, title)
    viewer.show()
    
    if not QApplication.instance():
        sys.exit(app.exec_())
    
    return viewer

# For testing purposes
if __name__ == "__main__":
    sample_response = """# Sorting Algorithms

Here's a quick overview of common sorting algorithms:

## Quick Sort

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

## Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Time Complexity Comparison

| Algorithm | Best Case | Average Case | Worst Case | Space Complexity |
|-----------|-----------|--------------|------------|------------------|
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |

## Visualization

```
Bubble Sort:
[5,3,8,4,2] → [3,5,8,4,2] → [3,5,4,8,2] → [3,5,4,2,8] → 
[3,5,4,2,8] → [3,4,5,2,8] → [3,4,2,5,8] → 
[3,4,2,5,8] → [3,2,4,5,8] → 
[2,3,4,5,8]
```
"""
    
    display_ai_response(sample_response, "Sorting Algorithms")