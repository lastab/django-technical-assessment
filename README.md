# Django Technical Assessment 

This project is a web application that combines a Django backend with a React frontend. 
The Django backend handles API requests, data processing, and storage, while the React frontend provides a dynamic and responsive user interface.
The project implements JWT to user authentication.
Registered users can login and access their uploaded csv or xml files and can upload new ones.
The uploaded file gets loaded into panda's dataframe and tries to accurately identify
the most approprate data type for each column.
The uploaded file's data with headers and data_types can be viewed. The application also allows to change the data_type.


## Prerequisites 

- Python 3.x 
- Node.js 
- npm or yarn

## Backend Setup (Django) 

1. Navigate to the backend directory: 
    ```sh 
    cd backend
    ```
2. Create a virtual environment:
    ```sh 
    python -m venv venv 
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3. Install backend dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Apply database migrations:
    ```sh
    python manage.py migrate
    ```
5. Start the Django development server:
    ```sh
    python manage.py runserver
    ```

## Frontend Setup (React)

1. Navigate to the frontend directory: 
    ```sh 
    cd frontend
    ```
2. Install frontend dependencies:
    ```sh 
    npm install
    # or
    yarn install
    ```
3. Create a `.env` file in the frontend directory and add the backend API URL:
    ```sh
    VITE_API_URL="http://localhost:8000"
    ```
4. Start the React development server:
    ```sh
    npm run dev
    # or
    yarn run dev
    ```

## Running the Application

Backend: The Django server will run on http://localhost:8000

Frontend: The React server will run on http://localhost:5173

Access the application by navigating to the frontend URL in your browser.


## Additional Information

Make sure the backend server is running when you start the frontend development server.
Register new user through: http://localhost:5173/register
Login the user through: http://localhost:5173/login

