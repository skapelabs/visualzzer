#!/usr/bin/env python3
"""
Test script for the AI markdown display functionality
"""
import sys
import requests
from PyQt5.QtWidgets import QApplication
from ai_markdown_display import display_ai_response

def test_with_sample_markdown():
    """Test the markdown display with a sample markdown string"""
    sample_markdown = """# Sorting Algorithms Explained

## Quick Sort

Quick Sort is a divide-and-conquer algorithm that works by selecting a 'pivot' element and partitioning the array around the pivot.

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

Merge Sort is also a divide-and-conquer algorithm that divides the input array into two halves, recursively sorts them, and then merges the sorted halves.

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

## ASCII Diagram of Sorting Process

```
Initial array: [5, 2, 9, 1, 7, 6, 3]

Quick Sort partitioning:
[5, 2, 9, 1, 7, 6, 3]  (pivot = 5)
[2, 1, 3] + [5] + [9, 7, 6]
   /           \
[1] + [2] + [3]   [6] + [7] + [9]

Final sorted array: [1, 2, 3, 5, 6, 7, 9]
```

## Time Complexity Comparison

| Algorithm | Best Case | Average Case | Worst Case | Space Complexity |
|-----------|-----------|--------------|------------|------------------|
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |

This is a test of the markdown rendering capabilities to ensure proper formatting of code blocks, ASCII diagrams, tables, and regular text with appropriate spacing and alignment.
"""
    
    print("Displaying sample markdown...")
    display_ai_response(sample_markdown, "Markdown Rendering Test")

def test_with_api_request():
    """Test the markdown display with an actual API request"""
    try:
        print("Sending request to API...")
        response = requests.post(
            'http://localhost:9090/api/ask_ai',
            json={"question": "Explain the merge sort algorithm with code examples and diagrams", "display_in_pyqt": True},
            timeout=30
        )
        
        if response.status_code == 200:
            print("API request successful!")
            # The display should be handled by the API endpoint
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error making API request: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Choose which test to run
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        test_with_api_request()
    else:
        test_with_sample_markdown()
    
    sys.exit(app.exec_())