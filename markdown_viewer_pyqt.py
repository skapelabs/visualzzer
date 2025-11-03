#!/usr/bin/env python3
"""
Markdown Viewer - PyQt5 application to display markdown content with proper formatting
"""
import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QScrollArea, 
                            QWidget, QTextEdit, QLabel, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor

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

class Separator(QFrame):
    """Simple horizontal separator line"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("margin: 10px 0;")

class MarkdownViewer(QMainWindow):
    """Main window for the Markdown Viewer application"""
    def __init__(self, markdown_text):
        super().__init__()
        self.init_ui()
        self.render_markdown(markdown_text)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Markdown Viewer")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(0)  # We'll add spacing with our widgets
        
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

def show_markdown(markdown_text):
    """Show markdown content in a new window"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    viewer = MarkdownViewer(markdown_text)
    viewer.show()
    
    if not QApplication.instance():
        sys.exit(app.exec_())
    
    return viewer

# For testing purposes
if __name__ == "__main__":
    sample_markdown = """# Markdown Rendering Test

This is a test of the markdown rendering capabilities. Let's see how it handles various elements.

## Code Blocks

Here's a Python code block:

```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
        
# Print the first 10 Fibonacci numbers
for i in range(10):
    print(fibonacci(i))
```

## ASCII Diagram

Here's an ASCII diagram that should not be wrapped:

```
+------------------+         +------------------+
|                  |         |                  |
|    Component A   |-------->|    Component B   |
|                  |         |                  |
+------------------+         +------------------+
        |                            |
        |                            |
        v                            v
+------------------+         +------------------+
|                  |         |                  |
|    Component C   |<--------|    Component D   |
|                  |         |                  |
+------------------+         +------------------+
```

## Regular Text

This is a paragraph with regular text that should be properly wrapped if it exceeds the width of the container. It should have proper line spacing and margins to make it readable.

## Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
| Cell 7   | Cell 8   | Cell 9   |

## End of Test

This is the end of the markdown rendering test.
"""
    
    show_markdown(sample_markdown)