Smart Diet Assistant 🥗🤖
Welcome to the Smart Diet Assistant, a web application designed to provide personalized nutritional guidance powered by AI. Users can create a personal profile, receive daily calorie and meal recommendations, and use their camera to upload images of food for automatic recognition and nutritional analysis.
Live Demo: https://smartdiet-xzoc.onrender.com
✨ Features
Personalized Profile Creation: Users can input their name, age, weight, height, gender, activity level, and dietary preferences to create a unique profile.
Daily Calorie Calculation: Automatically calculates the user's daily caloric needs based on their profile using the Mifflin-St Jeor equation.
AI-Powered Food Recognition: Upload an image of a meal, and the application will use a pre-trained TensorFlow model (MobileNetV2) to identify the food item.
Nutritional Information: Get estimated calories, protein, carbs, and fat for recognized food items based on a comprehensive nutrition table.
Custom Meal Recommendations: Receive a sample daily meal plan tailored to your caloric needs and dietary preferences.
Food Logging: Keep a log of all uploaded and recognized meals to track your intake.
🛠️ Technology Stack
This is a full-stack application built with a modern technology stack:
Frontend:
React: A JavaScript library for building user interfaces.
JavaScript (ES6+): For application logic.
CSS: For styling and layout.
Backend:
FastAPI: A modern, high-performance Python web framework for building APIs.
Python 3: For all server-side logic.
Uvicorn: An ASGI server to run the FastAPI application.
Machine Learning:
TensorFlow: An end-to-end open-source platform for machine learning.
MobileNetV2: A pre-trained model used for efficient image classification.
Deployment:
Render: The application is deployed as a single web service, with the FastAPI backend serving the built React frontend.
🏗️ How It Works
The application is a unified full-stack project where the backend serves both the API and the user interface.
The user visits the main URL, and the FastAPI server serves the index.html file from the built React application.
The React UI loads in the user's browser.
When the user interacts with the UI (e.g., creates a profile or uploads an image), the React frontend makes an API request to the backend (e.g., POST /api/profile).
The FastAPI backend receives the request, processes it, performs calculations, or runs the TensorFlow model for image recognition.
The backend then sends a JSON response back to the frontend.
The React application receives this data and updates the UI to display the results to the user.
🚀 Setup and Installation
To run this project locally, you will need to run the backend and frontend separately.
Prerequisites
Python 3.8+
Node.js and npm
Backend Setup
Clone the repository:
git clone [https://github.com/ishumaitreyee/SmartDiet.git](https://github.com/ishumaitreyee/SmartDiet.git)
cd SmartDiet


Create a Python virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install Python dependencies:
pip install -r requirements.txt


Run the backend server:
uvicorn main:app --reload

The backend API will be running at http://127.0.0.1:8000.
Frontend Setup
Navigate to the frontend directory:
# From the project root
cd frontend/smart-diet-frontend


Install Node.js dependencies:
npm install


Start the frontend development server:
npm start

The frontend UI will open in your browser at http://localhost:3000.
📝 API Endpoints
The backend provides the following API endpoints:
POST /api/profile: Create a new user profile.
POST /api/recommend: Get a meal recommendation for a given user_id.
POST /api/upload_food: Upload a food image for recognition for a given user_id.
GET /api/logs: Retrieve the food logs for a given user_id.
You can view interactive API documentation by running the backend locally and visiting http://127.0.0.1:8000/docs.
