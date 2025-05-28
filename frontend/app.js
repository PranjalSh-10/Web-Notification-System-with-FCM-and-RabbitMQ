import { initializeApp } from "https://www.gstatic.com/firebasejs/10.3.1/firebase-app.js";
import { getMessaging, getToken } from "https://www.gstatic.com/firebasejs/10.3.1/firebase-messaging.js";

const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  messagingSenderId: "",
  appId: ""
};

const app = initializeApp(firebaseConfig);

window.subscribeToNotifications = subscribeToNotifications;

async function subscribeToNotifications() {
  const permission = await Notification.requestPermission();

  if (permission === "granted") {
    console.log("Notification permission granted.");

    try {
      const swReg = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
      console.log("Service Worker registered:", swReg);

      const messaging = getMessaging(app);

      const token = await getToken(messaging, {
        vapidKey: '',
        serviceWorkerRegistration: swReg
      });

      if (token) {
        console.log("FCM Token:", token);

        await fetch('http://localhost:8000/devices/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ fcm_token: token })
        });

        alert("Subscribed successfully!");
      } else {
        alert("No registration token available.");
      }

    } catch (error) {
      console.error("An error occurred while retrieving token. ", error);
      alert("Subscription failed: " + error.message);
    }

  } else if (permission === "denied") {
    alert("You denied notification permission.");
  } else {
    alert("You must grant permission to subscribe.");
  }
}


