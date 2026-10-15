# Park-Here – Car Parking Management System

Park-Here is a Flask-based web application that helps users find and book parking spots easily. It also allows administrators to manage parking lots, monitor parking availability, and view parking records.

## Features

- User registration and login
- Search and book available parking spots
- Admin dashboard for managing parking lots and spots
- Monitor occupied and available parking spots
- Track parking history and parking costs
- Responsive user interface
- Visual reports and charts

## Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Authentication:** Flask-Login
- **Visualization:** Matplotlib

## Project Structure

```text
park-here/
├── controllers/
├── instance/
├── static/
├── templates/
├── app.py
├── requirements.txt
└── README.md
```

## How to Run the Application

### Prerequisites

- Python installed on your system
- Git installed on your system

### Steps

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Navigate to the project directory**

```bash
cd park-here
```

**3. Install the required dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

**5. Open the application**

Follow the local URL displayed in the terminal and open it in your web browser.

## How to Use

### For Users

1. Register for an account.
2. Log in to the application.
3. Browse available parking spots.
4. Select and book an available spot.
5. View parking details and history.

### For Administrators

1. Log in using an administrator account.
2. Access the admin dashboard.
3. Add, view, or delete parking lots and manage spots.
4. Monitor parking availability and occupied spots.

## Database

The application uses SQLite to store user information, parking lots, parking spots, and parking history.

## Project Documentation

Refer to the project documentation for detailed information about the database schema, architecture, and implementation.


## Author

**Jeevan Jyoti**  


---

*Park-Here – Making parking easier and more convenient.*
