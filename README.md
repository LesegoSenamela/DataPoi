# DataPoi

A data poisoning detection, processing and visualization web application built with Flask, designed to handle data analysis tasks with an intuitive interface.

## Overview

DataPoi is a web-based data analysis tool that provides an interactive platform for processing, visualizing, and deriving insights from datasets. Built with Python Flask on the backend and modern HTML/CSS on the frontend, it offers a seamless experience for interpreting data poisoning results.

## Features

- **Data Upload & Processing**: Upload datasets for analysis
- **Interactive Visualizations**: Dynamic Results visualisation
- **Results Downloading**: Clean, user-friendly interface where you can download a pdf of the results.
- **Docker Support**: Easy deployment with containerization

## Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- Docker (optional, for containerized deployment)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LesegoSenamela/DataPoi.git
   cd DataPoi
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t datapoi .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 datapoi
   ```

## Project Structure

```
DataPoi/
├── app.py             # Main Flask application
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
├── models/            # Data models and processing logic
├── static/            # Static files (CSS, JS, images)
│   └── styles.css     # Stylesheet
└── templates/         # HTML templates
    └── index.html     # Main application page
```

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerization**: Docker
- **Data Processing**: Pandas, NumPy, Sickit-Learn

## Usage

1. **Upload Data**: Navigate to the upload section and select your dataset (CSV).
2. **Visualize**: Generate analysis results of the dataset. 
3. **Export**: Download process results.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This is a research project and will be changed as the research progresses.

## Contact

Lesego Senamela - [GitHub Profile](https://github.com/LesegoSenamela) • [LinkedIn](https://www.linkedin.com/in/lesegosenamela) • [Email](senamelalesego@gmail.com)



