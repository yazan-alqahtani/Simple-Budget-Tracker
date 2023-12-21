# Simple Budget Tracker

Simple Budget Tracker is a simple and intuitive web application built with Flask, designed to help users manage their expenses and budgets effortlessly. The application allows users to log in, add their expenses with descriptions and categories, set budgets for different expense categories, and visualize their spending patterns through interactive charts.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Features

- User Authentication: Secure user authentication system for personalized experiences.
- Expense Tracking: Add, view, and categorize expenses to gain insights into spending habits.
- Budget Management: Set and manage budgets for various expense categories to stay on track.
- Interactive Charts: Visualize expense distribution through dynamic pie charts.
User-Friendly Interface: Simple and elegant design for an intuitive user experience.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yazan-alqahtani/Simple-Budget-Tracker.git
   cd Simple-Budget-Tracker
   ```
1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up the database:

    ```bash
    python app.py
    ```

# Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to http://localhost:5000.

3. Explore the application.

# Dependencies

Flask==2.0.1

Flask-WTF==0.15.1

Flask-SQLAlchemy==2.5.1

Flask-Login==0.5.0

matplotlib==3.4.3

Werkzeug==2.1.5