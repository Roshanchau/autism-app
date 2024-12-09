
# Autism-app

## Overview
This repository contains a project developed during a hackathon, featuring a **Flask-based backend API** and a **React Native mobile application** built with Expo. The project leverages various technologies to provide functionalities like image fetching, word prediction, and Redis caching.

---

## Folder Structure
- **`hackthon_ktm/`**: Contains the backend code developed using Flask.
- **`mobile/autism-mobile/`**: Contains the React Native mobile application built with Expo.

---

## Features

### Backend (`hackthon_ktm`)
- Built with Flask.
- Implements API endpoints for:
  - **Image fetching**: Fetches images using the Pixabay API.
  - **Word prediction**: Utilizes GPT-2 to predict words based on user input.
  - **Caching**: Uses Redis to cache results for enhanced performance.
- External dependencies include:
  - Flask-Cors for enabling cross-origin requests.
  - HuggingFace Transformers for GPT-2 integration.
  - Redis for caching.
- **Requirement**: Users must configure their own **IP address** to access the API.

### Mobile App (`mobile/autism-mobile`)
- Developed using React Native and Expo.
- Interacts with the Flask backend for fetching images and word prediction.
- **Requirement**: Users must configure their own **IP address** to connect to the backend API.

---

## Getting Started

### Prerequisites
1. **Backend**
   - Python 3.7 or later.
   - Redis server.
   - A Pixabay API key.
2. **Mobile App**
   - Node.js and npm.
   - Expo CLI.

### Installation

#### Backend
1. Navigate to the `hackthon_ktm` folder.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Add your Pixabay API key to the `.env` file as `API_kEY`.
   - Add your Redis password to the `.env` file as `REDIS_PASSWORD`.
4. Start the Flask server:
   ```bash
   python flask_oldest.py
   ```

#### Mobile App
1. Navigate to the `mobile/autism-mobile` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure the IP address:
   - Update the backend API URL in the React Native app code to match your Flask server's IP address.
4. Start the Expo development server:
   ```bash
   npx expo start
   ```

---

## API Endpoints

### 1. **Fetch Images**
   **Endpoint**: `/api/images`  
   **Method**: `GET`  
   **Query Parameters**:
   - `query`: Search term for images.
   - `id`: Unique identifier for caching.
   **Response**: URL of the fetched image.

### 2. **Word Prediction**
   **Endpoint**: `/api/guu`  
   **Method**: `POST`  
   **Request Body**: 
   ```json
   {
       "item": "input_text"
   }
   ```
   **Response**: Predicted words.

### 3. **Display Words**
   **Endpoint**: `/api/display_words`  
   **Method**: `GET`  
   **Query Parameters**:
   - `count`: Pagination count.
   **Response**: List of words for display.

---

## Technologies Used

- **Backend**:
  - Flask
  - Redis
  - Transformers (GPT-2)
  - Python-Dotenv
  - Pixabay API

- **Frontend**:
  - React Native
  - Expo

---

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---


