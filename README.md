## Motivation
This prototype was inspired by a human-centric approach to software development, focusing on designing intuitive and meaningful digital experiences. The goal was to simplify the healthcare booking process by making it more accessible, efficient, and user-friendly.

# 🏥 Healthcare Appointment Booking System

This is a prototype web-based application that allows patients to view available healthcare appointment slots, book an appointment, and manage existing bookings — including cancellations — through a modern, user-friendly interface.

---

## 📌 Use Case

Healthcare providers often rely on outdated systems or manual processes to manage patient appointments. This application demonstrates how cloud-native technologies can be used to build a responsive and scalable appointment system for patients and healthcare administrators.

**Key Features:**
- View available slots
- Book appointments
- Cancel appointments with confirmation
- Light/dark mode toggle
- Responsive, mobile-friendly UI

---

## 🏗️ Architecture

The application follows a serverless, event-driven architecture:

```
[Frontend (Next.js)] → [API Gateway] → [AWS Lambda Functions] → [DynamoDB]
```

- **Frontend:** Next.js with modern CSS styling
- **API Gateway:** Handles RESTful HTTP endpoints
- **Lambda Functions:** Stateless compute functions for slot querying, booking, and cancellation
- **DynamoDB:** Serverless NoSQL database for slots and appointments

![Healthcare Appointment System Diagram drawio](https://github.com/user-attachments/assets/d0bcda47-ad34-4404-bc03-8b6a2459434b)

---

## 🧰 Technologies Used

### Frontend
- React (via Next.js)
- CSS Modules (modern, scoped styling)
- Dark/Light theme toggle
- TypeScript

### Backend
- AWS Lambda (Python 3.11)
- Amazon API Gateway
- Amazon DynamoDB (with GSI on `patient_id`)
- AWS SAM (Serverless Application Model)

---

## ⚙️ Prototype Design Highlights

- Simple, clean UI with clear call-to-actions
- Slot booking via URL param prefill
- Modal confirmations for success/failure
- CORS-enabled endpoints for smooth frontend-backend integration
- Patient ID hardcoded for demonstration purposes

---

## 🔗 Demo

> 🌐 **Live Demo (API only)**:  
> [https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod](https://7x307khvxf.execute-api.eu-west-2.amazonaws.com/Prod)

> 🖥️ **Frontend App (local)**:  
> Run `npm run dev` in the `/frontend` directory and access via `http://localhost:3000`.

---

## 📝 Setup Instructions

1. Clone the repository
2. Deploy backend with AWS SAM:
   ```
   sam build && sam deploy --guided
   ```
3. Run frontend locally:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. Visit `http://localhost:3000` to interact with the application

---

## 📌 Notes

- This prototype assumes no login or user authentication.
- To make it production-ready, consider integrating Amazon Cognito, better slot conflict resolution, and input sanitization.
- The patient ID is hardcoded for testing.
