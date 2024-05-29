# HR Agent Project

## Overview
The HR Agent project is a Django-based web application designed to automate various human resource tasks, such as summarizing candidate notes, answering FAQs, and onboarding new employees. The project leverages AI agents for processing and generating responses to streamline HR operations.

## Features
1. **Homepage**: A simple welcome page.
2. **About Page**: Provides information about the project.
3. **Candidate Notes Summarization**: Summarizes notes on candidates from uploaded text files.
4. **FAQ Agent**: Answers frequently asked questions by searching a specified document.
5. **Onboarding Form**: Sends personalized onboarding emails to new employees with best practices and company policies.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/hr-agent-project.git
    cd hr-agent-project
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the project root directory and add the following variables:
    ```
    EMAIL_SENDER=your-email@gmail.com
    EMAIL_PASSWORD=your-email-password
    DOCX_FILE_PATH=/path/to/Employee-Code-of-Conduct.docx
    ```

5. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

### Homepage
- Access the homepage at `http://localhost:8000/` to see a welcome message.

### About Page
- Visit `http://localhost:8000/about` to learn more about the project.

### Candidate Notes Summarization
- Navigate to `http://localhost:8000/notes` to upload a text file containing candidate notes and get a summarized version.

### FAQ Agent
- Go to `http://localhost:8000/faq` to ask questions and receive answers based on the content of the uploaded document.

### Onboarding Form
- Visit `http://localhost:8000/onboarding` to fill out the onboarding form and send a personalized welcome email to new employees.

## Code Structure

- `views.py`: Contains the logic for handling requests and rendering templates.
- `urls.py`: Maps URLs to the corresponding view functions.
- `templates/`: Contains the HTML templates for rendering pages.
- `static/`: Contains static files (CSS, JavaScript, images).
- `.env`: Environment variables configuration file.

## Key Dependencies

- Django: The web framework used to build the application.
- smtplib and ssl: Used for sending emails securely.
- dotenv: For loading environment variables from a `.env` file.
- crewai: A custom AI tool for creating and managing agents and tasks.

## Contributing

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```
3. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature-name
    ```
5. **Create a new Pull Request**.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For questions or suggestions, please contact [Aneesh Bukya](mailto:aneeshbsri@gmail.com).
