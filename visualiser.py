import pygame
import random
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# config - Initialize pygame later to avoid tkinter conflict
import pygame

# Default dimensions (will be updated when pygame initializes)
WIDTH = 1600
HEIGHT = 1000
NUM_ITEMS = 50  # More items for larger screen
PADDING = 50
BAR_GAP = 2
SLEEP_MS = 60  # milliseconds pause between steps

# colours
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
BG = (18, 18, 20)
BAR_COLOR = (100, 200, 255)
ACTIVE_COLOR = (255, 120, 120)
TEXT_COLOR = (220, 220, 220)

# Global variables for pygame objects (initialized later)
screen = None
font = None
clock = None

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
            return gen_random_list(NUM_ITEMS)
        
        if not user_input.strip():
            # User wants random numbers
            root.destroy()
            return gen_random_list(NUM_ITEMS)
        
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

def render_text_antialiased(font, text, color):
    """Render text with anti-aliasing for better quality on Retina displays"""
    try:
        # Try to render with anti-aliasing (if supported)
        return font.render(text, True, color)
    except:
        # Fallback to regular rendering
        return font.render(text, True, color)

def get_time_complexity(algorithm):
    complexities = {
        "bubble": "O(n²) - Worst/Average, O(n) - Best",
        "insertion": "O(n²) - Worst/Average, O(n) - Best", 
        "selection": "O(n²) - All cases",
        "quick": "O(n log n) - Average, O(n²) - Worst",
        "merge": "O(n log n) - All cases",
        "heap": "O(n log n) - All cases"
    }
    return complexities.get(algorithm, "")

def draw(items, active_indices=None, title="", time_complexity="", execution_time=""):
    screen.fill(BG)
    active_indices = active_indices or []
    n = len(items)
    if n == 0:
        pygame.display.flip()
        return

    # Reserve space for instructions at the top and bottom
    top_height = 200
    bottom_height = 100
    chart_area_height = HEIGHT - top_height - bottom_height - PADDING
    
    # compute bar size
    usable_width = WIDTH - 2 * PADDING
    bar_width = max(1, (usable_width - (n - 1) * BAR_GAP) // n)
    max_val = max(items)
    scale = chart_area_height / max_val

    # Draw bars in the middle area
    for i, val in enumerate(items):
        x = PADDING + i * (bar_width + BAR_GAP)
        bar_h = int(val * scale)
        y = HEIGHT - bottom_height - bar_h
        color = ACTIVE_COLOR if i in active_indices else BAR_COLOR
        rect = pygame.Rect(x, y, bar_width, bar_h)
        pygame.draw.rect(screen, color, rect)
        # small value label (only show for larger bars to avoid clutter)
        if bar_h > 30:
            txt = render_text_antialiased(font, str(val), TEXT_COLOR)
            txt_rect = txt.get_rect(center=(x + bar_width / 2, y - 10))
            screen.blit(txt, txt_rect)

    # Top section - Status and algorithm info
    top_lines = [
        f"Status: {title}",
        "",
        "SORTING ALGORITHMS:",
        "B - Bubble Sort    I - Insertion Sort    S - Selection Sort",
        "Q - Quick Sort     M - Merge Sort       H - Heap Sort"
    ]
    for idx, line in enumerate(top_lines):
        if line:  # Only draw non-empty lines
            txt = render_text_antialiased(font, line, TEXT_COLOR)
            screen.blit(txt, (PADDING, 20 + idx * 25))
    
    # Right side box for time complexity and execution time
    if time_complexity or execution_time:
        # Calculate box size based on screen width
        box_width = min(500, WIDTH // 3)  # Max 500px or 1/3 of screen width
        box_height = 140
        box_x = WIDTH - box_width - PADDING
        box_y = 20
        
        # Ensure box doesn't go off screen
        if box_x < PADDING:
            box_x = PADDING
            box_width = WIDTH - 2 * PADDING
        
        # Draw box background
        pygame.draw.rect(screen, (40, 40, 45), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (100, 100, 110), (box_x, box_y, box_width, box_height), 2)
        
        # Box title
        title_txt = render_text_antialiased(font, "ALGORITHM INFO", TEXT_COLOR)
        screen.blit(title_txt, (box_x + 15, box_y + 15))
        
        # Time complexity - wrap text if too long
        if time_complexity:
            complexity_text = f"Time Complexity: {time_complexity}"
            # Split long text into multiple lines if needed
            if len(complexity_text) > 50:
                parts = complexity_text.split(" - ")
                if len(parts) >= 2:
                    complexity_txt1 = render_text_antialiased(font, parts[0], TEXT_COLOR)
                    complexity_txt2 = render_text_antialiased(font, parts[1], TEXT_COLOR)
                    screen.blit(complexity_txt1, (box_x + 15, box_y + 45))
                    screen.blit(complexity_txt2, (box_x + 15, box_y + 65))
                else:
                    complexity_txt = render_text_antialiased(font, complexity_text[:45] + "...", TEXT_COLOR)
                    screen.blit(complexity_txt, (box_x + 15, box_y + 45))
            else:
                complexity_txt = render_text_antialiased(font, complexity_text, TEXT_COLOR)
                screen.blit(complexity_txt, (box_x + 15, box_y + 45))
        
        # Execution time
        if execution_time:
            time_text = f"Execution Time: {execution_time}"
            time_txt = render_text_antialiased(font, time_text, TEXT_COLOR)
            screen.blit(time_txt, (box_x + 15, box_y + 95))

    # Bottom section - Controls
    bottom_lines = [
        "CONTROLS:",
        "A - Ascending  |  D - Descending  |  SPACE - Start  |  R - Random",
        "X - Instant Sort  |  ESC - Quit"
    ]
    for idx, line in enumerate(bottom_lines):
        txt = render_text_antialiased(font, line, TEXT_COLOR)
        screen.blit(txt, (PADDING, HEIGHT - bottom_height + 20 + idx * 25))

    pygame.display.flip()

def bubble_sort_gen(arr, ascending=True):
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # highlight comparing pair
            yield a, (j, j + 1)
            if (a[j] > a[j + 1]) == ascending:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                yield a, (j, j + 1)
        if not swapped:
            break
    yield a, ()

def insertion_sort_gen(arr, ascending=True):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        yield a, (i,)
        while j >= 0 and (a[j] > key) == ascending:
            a[j + 1] = a[j]
            j -= 1
            yield a, (j + 1, j + 2)
        a[j + 1] = key
        yield a, (j + 1,)
    yield a, ()

def selection_sort_gen(arr, ascending=True):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        yield a, (i,)
        for j in range(i + 1, n):
            yield a, (i, j)
            if (a[j] < a[min_idx]) == ascending:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield a, (i, min_idx)
    yield a, ()

def quick_sort_gen(arr, ascending=True):
    def _quick_sort(a, low, high):
        if low < high:
            # Partition
            pivot_idx = low
            pivot = a[high]
            yield a, (high,)
            
            for i in range(low, high):
                yield a, (i, high)
                if (a[i] < pivot) == ascending:
                    a[pivot_idx], a[i] = a[i], a[pivot_idx]
                    yield a, (pivot_idx, i)
                    pivot_idx += 1
            
            a[pivot_idx], a[high] = a[high], a[pivot_idx]
            yield a, (pivot_idx, high)
            
            # Recursive calls
            for step in _quick_sort(a, low, pivot_idx - 1):
                yield step
            for step in _quick_sort(a, pivot_idx + 1, high):
                yield step
    
    a = arr[:]
    for step in _quick_sort(a, 0, len(a) - 1):
        yield step
    yield a, ()

def merge_sort_gen(arr, ascending=True):
    def _merge(a, left, mid, right):
        left_arr = a[left:mid + 1]
        right_arr = a[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            yield a, (left + i, mid + 1 + j)
            if (left_arr[i] <= right_arr[j]) == ascending:
                a[k] = left_arr[i]
                i += 1
            else:
                a[k] = right_arr[j]
                j += 1
            yield a, (k,)
            k += 1
        
        while i < len(left_arr):
            a[k] = left_arr[i]
            yield a, (k,)
            i += 1
            k += 1
        
        while j < len(right_arr):
            a[k] = right_arr[j]
            yield a, (k,)
            j += 1
            k += 1
    
    def _merge_sort(a, left, right):
        if left < right:
            mid = (left + right) // 2
            for step in _merge_sort(a, left, mid):
                yield step
            for step in _merge_sort(a, mid + 1, right):
                yield step
            for step in _merge(a, left, mid, right):
                yield step
    
    a = arr[:]
    for step in _merge_sort(a, 0, len(a) - 1):
        yield step
    yield a, ()

def heap_sort_gen(arr, ascending=True):
    def heapify(a, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            yield a, (i, left)
            if (a[left] > a[largest]) == ascending:
                largest = left
        
        if right < n:
            yield a, (i, right)
            if (a[right] > a[largest]) == ascending:
                largest = right
        
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            yield a, (i, largest)
            for step in heapify(a, n, largest):
                yield step
    
    a = arr[:]
    n = len(a)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        for step in heapify(a, n, i):
            yield step
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        yield a, (0, i)
        for step in heapify(a, i, 0):
            yield step
    
    yield a, ()

def handle_quit_events():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def handle_resize_event(event):
    """Handle window resize events for high-DPI displays"""
    global WIDTH, HEIGHT
    if event.type == pygame.VIDEORESIZE:
        WIDTH, HEIGHT = event.w, event.h
        # Recreate the display with new dimensions
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)

def main():
    # Get user input for numbers BEFORE initializing pygame
    items = get_user_input()
    
    # Now initialize pygame after tkinter is done
    global screen, font, clock, WIDTH, HEIGHT
    
    # Initialize pygame
    pygame.init()
    
    # Enable high-DPI rendering and multisampling for Retina displays
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
    
    # Get actual screen dimensions
    screen_info = pygame.display.Info()
    WIDTH = screen_info.current_w - 100  # Leave 50px margin on each side
    HEIGHT = screen_info.current_h - 100  # Leave 50px margin on top/bottom
    
    # Create high-DPI display with scaling and resizing
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Data Structure Visualiser")
    
    # Initialize font after pygame is ready
    try:
        font = pygame.font.SysFont("SF Mono", 24)
    except:
        try:
            font = pygame.font.SysFont("Menlo", 24)
        except:
            try:
                font = pygame.font.SysFont("Consolas", 24)
            except:
                font = pygame.font.SysFont("monospace", 24)
    
    clock = pygame.time.Clock()
    
    current_gen = None
    current_title = "Ready - Select algorithm"
    selected_algorithm = None
    ascending = True
    start_time = None
    execution_time = ""

    while True:
        # Handle events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.VIDEORESIZE:
                handle_resize_event(ev)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # Algorithm selection
                if ev.key == pygame.K_b:
                    selected_algorithm = "bubble"
                    current_title = "Bubble Sort selected - Press SPACE to start"
                elif ev.key == pygame.K_i:
                    selected_algorithm = "insertion"
                    current_title = "Insertion Sort selected - Press SPACE to start"
                elif ev.key == pygame.K_s and not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    selected_algorithm = "selection"
                    current_title = "Selection Sort selected - Press SPACE to start"
                elif ev.key == pygame.K_q:
                    selected_algorithm = "quick"
                    current_title = "Quick Sort selected - Press SPACE to start"
                elif ev.key == pygame.K_m:
                    selected_algorithm = "merge"
                    current_title = "Merge Sort selected - Press SPACE to start"
                elif ev.key == pygame.K_h:
                    selected_algorithm = "heap"
                    current_title = "Heap Sort selected - Press SPACE to start"
                
                # Direction selection
                elif ev.key == pygame.K_a:
                    ascending = True
                    if selected_algorithm:
                        current_title = f"{selected_algorithm.title()} Sort (Ascending) - Press SPACE to start"
                    else:
                        current_title = "Ascending selected - Choose algorithm"
                elif ev.key == pygame.K_d:
                    ascending = False
                    if selected_algorithm:
                        current_title = f"{selected_algorithm.title()} Sort (Descending) - Press SPACE to start"
                    else:
                        current_title = "Descending selected - Choose algorithm"
                
                # Start sorting
                elif ev.key == pygame.K_SPACE:
                    if selected_algorithm:
                        start_time = time.time()
                        execution_time = ""
                        if selected_algorithm == "bubble":
                            current_gen = bubble_sort_gen(items, ascending=ascending)
                            current_title = f"Bubble Sort ({'Ascending' if ascending else 'Descending'})"
                        elif selected_algorithm == "insertion":
                            current_gen = insertion_sort_gen(items, ascending=ascending)
                            current_title = f"Insertion Sort ({'Ascending' if ascending else 'Descending'})"
                        elif selected_algorithm == "selection":
                            current_gen = selection_sort_gen(items, ascending=ascending)
                            current_title = f"Selection Sort ({'Ascending' if ascending else 'Descending'})"
                        elif selected_algorithm == "quick":
                            current_gen = quick_sort_gen(items, ascending=ascending)
                            current_title = f"Quick Sort ({'Ascending' if ascending else 'Descending'})"
                        elif selected_algorithm == "merge":
                            current_gen = merge_sort_gen(items, ascending=ascending)
                            current_title = f"Merge Sort ({'Ascending' if ascending else 'Descending'})"
                        elif selected_algorithm == "heap":
                            current_gen = heap_sort_gen(items, ascending=ascending)
                            current_title = f"Heap Sort ({'Ascending' if ascending else 'Descending'})"
                
                # Reshuffle
                elif ev.key == pygame.K_r:
                    # Generate random numbers with the same length as current items
                    items = gen_random_list(len(items))
                    current_gen = None
                    selected_algorithm = None
                    current_title = "Random numbers generated - Select algorithm"
                    execution_time = ""
                
                # Instant sort
                elif ev.key == pygame.K_x:
                    start_time = time.time()
                    items = sorted(items, reverse=not ascending)
                    execution_time = f"{(time.time() - start_time):.4f} seconds"
                    current_gen = None
                    current_title = f"Instantly sorted ({'Ascending' if ascending else 'Descending'})"

        # if generator active, advance step by step
        if current_gen is not None:
            try:
                arr_state, active = next(current_gen)
                items = arr_state[:]
                time_complexity = get_time_complexity(selected_algorithm)
                draw(items, active_indices=active, title=current_title, 
                     time_complexity=time_complexity, execution_time=execution_time)
                # small wait but keep event loop alive
                pygame.time.wait(SLEEP_MS)
                # process events so window remains responsive
                pygame.event.pump()
            except StopIteration:
                if start_time:
                    execution_time = f"{(time.time() - start_time):.4f} seconds"
                current_gen = None
                current_title = "Sorting Complete!"
        else:
            time_complexity = get_time_complexity(selected_algorithm) if selected_algorithm else ""
            draw(items, title=current_title, time_complexity=time_complexity, execution_time=execution_time)
            clock.tick(30)

if __name__ == "__main__":
    main()
