# Data Structure Visualizer - Student Project

A learning project for visualizing data structures and algorithms with a Flask backend and web interface. Built for educational purposes to understand how different data structures and sorting algorithms work.

## Features

- **Landing Page**: Introduction to the visualizer with feature highlights
- **How-to Page**: Comprehensive instructions and keyboard controls
- **Interactive Visualizer**: Launch the Python pygame visualizer from the web
- **Custom Input**: Enter your own numbers or use random data
- **6 Sorting Algorithms**: Bubble, Insertion, Selection, Quick, Merge, and Heap Sort
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional design with smooth animations

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web App**:
   ```bash
   python app.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:9090`

## Project Structure

```
visualizer/
├── app.py                 # Flask application
├── visualiser.py         # Python pygame visualizer
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Landing page
│   ├── how_to.html     # Instructions page
│   └── visualizer.html # Visualizer page
└── static/             # Static assets
    ├── css/
    │   └── style.css   # Main stylesheet
    └── js/
        └── main.js     # JavaScript functionality
```

## Web App Pages

### 1. Landing Page (`/`)
- Hero section with app introduction
- Feature highlights with icons
- Algorithm overview with time complexities
- Call-to-action buttons

### 2. How-to Page (`/how-to`)
- Detailed keyboard controls
- Custom input instructions
- Step-by-step workflow
- Pro tips for best experience

### 3. Visualizer Page (`/visualizer`)
- Quick start options (random or custom numbers)
- Input validation for custom numbers
- Launch button for Python visualizer
- Algorithm and control reference

## API Endpoints

- `GET /api/random-numbers?count=25` - Generate random numbers
- `POST /api/validate-numbers` - Validate user input numbers
- `GET /run-visualizer` - Launch the Python visualizer

## Keyboard Controls (in Python Visualizer)

| Key | Action |
|-----|--------|
| B | Bubble Sort |
| I | Insertion Sort |
| S | Selection Sort |
| Q | Quick Sort |
| M | Merge Sort |
| H | Heap Sort |
| A | Ascending Order |
| D | Descending Order |
| SPACE | Start Sorting |
| R | Random Numbers |
| X | Instant Sort |
| ESC | Quit |

## Custom Number Input

- **Format**: Separate numbers with spaces or commas
- **Limit**: Maximum 25 numbers
- **Range**: Numbers between 1 and 1000
- **Examples**: `10 5 8 3 7` or `10,5,8,3,7`

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualizer**: Pygame (Python)
- **Styling**: Custom CSS with modern design
- **Fonts**: Inter (Google Fonts)

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Development

To run in development mode:

```bash
export FLASK_ENV=development
python app.py
```

## Deployment

For production deployment, consider using:
- Gunicorn as WSGI server
- Nginx as reverse proxy
- Environment variables for configuration

## License

This project is open source and available under the MIT License.
