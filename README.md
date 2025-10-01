# 🎬 Watchlist Application (Microservices + Kubernetes)
This project is a **microservice-based movie watchlist application** built with **Python Flask** and **MongoDB**, fully deployed on **Kubernetes (Minikube)**.  

Users can **register, log in, and manage their personal movie watchlist**, with persistent storage for both user and movie data.


---
## 🚀 Features

- **User Authentication** – Register, Login, Logout (Auth-Service).  
- **Movie Management** – Add movies, view your watchlist, mark favorites (Movie-Service).  
- **Persistent Database** – MongoDB ensures data persistence.  
- **Kubernetes Deployment** – Each service runs in its own pod with service discovery, NodePort access, and scaling support.  
- **Frontend Integration** – `index.html` served by Auth-Service acts as the web interface.

---
## 🏗️ Architecture Overview

```text
+-----------------+      +-----------------+      +-----------------+
| Auth-Service    | ---> | Movie-Service   | ---> | MongoDB         |
| (Flask + UI)    |      | (Flask API)     |      | (Persistent DB) |
+-----------------+      +-----------------+      +-----------------+
       |                                         ^
       | NodePort Access                          |
       +-----------------------------------------+

```
---

## ⚙️ Setup & Deployment Instructions

### 1. Clone Repository
```bash
git clone https://github.com/vineethdhagey/Moviesapp.git
cd Moviesapp

```
### 2. Start Minikube
```bash
minikube start

```
### 3. Deploy Application
```bash
kubectl apply -f movie-app.yaml

```
### 4. Verify Pods & Services
```bash
kubectl get pods -n movies-app
kubectl get svc -n movies-app

```
### 5. Access Application
```bash
minikube service auth-service -n movies-app

```
This will open the browser with the frontend UI.

## 🌐 API Endpoints
 ### Auth-Service
  - **POST /api/register** → Register a new user

- **POST /api/login** → Login

- **POST /api/logout** → Logout

  ### Movie-Service
  - **POST /api/add_movie** → Add a movie for the logged-in user

- **GET /api/movies/{user_id}** → Fetch all movies for a specific user

- **DELETE /api/movies/{movie_id}** → Delete a movie by its ID


<img width="1888" height="919" alt="Screenshot 2025-10-01 230301" src="https://github.com/user-attachments/assets/f93a6cb6-6ee4-4003-9903-4da53e038747" />

<img width="1868" height="832" alt="Screenshot 2025-10-01 230328" src="https://github.com/user-attachments/assets/b1812e09-1972-491e-9738-f63fbe334818" />

<img width="1810" height="721" alt="Screenshot 2025-10-01 230519" src="https://github.com/user-attachments/assets/f4edbb4a-2657-4122-bdf0-a373134efb4f" />



