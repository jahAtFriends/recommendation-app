# Academic Recommendation App

This application processes student academic records in various math and science courses to give a recommendation for the course they should take next year. Academic data is imported via a CSV file listing classes taken (during which year) and grade earned by the student. The prerequisites and the possible next courses are defined in YAML files. The program outputs a CSV file showing the recommended course (or courses) for each student.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The application requires Python 3.6+ to run. The required Python packages are listed in the `requirements.txt` file. You can install them using pip:

```
pip install -r requirements.txt
```

### Running the Application

To run the application, navigate to the `src` directory and run the `main.py` file:

```
python main.py
```

The application will read the student academic records from the `data/students.csv` file, the course prerequisites from the `data/prerequisites.yaml` file, and the possible next courses from the `data/flow.yaml` file. It will then generate course recommendations for each student and write them to the `output/recommendations.csv` file.

## Project Structure

The project has the following structure:

- `src`: This directory contains the Python source code for the application.
  - `main.py`: This is the main file that runs the application.
  - `student.py`: This file exports a `Student` class.
  - `course.py`: This file exports a `Course` class.
  - `recommendation.py`: This file exports a `Recommendation` class.
  - `utils`: This directory contains utility functions for processing CSV and YAML files.
    - `csv_processor.py`: This file exports functions for processing CSV files.
    - `yaml_processor.py`: This file exports functions for processing YAML files.
- `data`: This directory contains the input CSV and YAML files.
  - `students.csv`: This file contains the academic records of the students.
  - `prerequisites.yaml`: This file defines the prerequisites for each course.
  - `flow.yaml`: This file defines the possible next courses for each course.
- `output`: This directory contains the output CSV file.
  - `recommendations.csv`: This file contains the course recommendations for each student.
- `requirements.txt`: This file lists the Python packages that the application depends on.
- `README.md`: This file contains the documentation for the application.