import { Capacitor } from '@capacitor/core'

export function listen() {
  Pushy.listen();
}

// Register the user for push notifications
export function register() {
  Pushy.register(function (err, deviceToken) {
      // Handle registration errors
      if (err) {
        return alert(err);
      }

      // Display an alert with device token
      alert('Pushy device token: ' + deviceToken);

      // Send the token to your backend server via an HTTP GET request
      //await fetch('https://your.api.hostname/register/device?token=' + deviceToken);

      // Succeeded, optionally do something to alert the user
  })
}

// Enable in-app notification banners (iOS 10+)
export function toggleInAppBanner(value) {
  Pushy.toggleInAppBanner(value);
}

// Listen for push notifications
export function setNotificationListener() {
  Pushy.setNotificationListener(function (data) {
      // Print notification payload data
      console.log('Received notification: ' + JSON.stringify(data));

      // Display an alert with the "message" payload value
      alert('Received notification: ' + data.message);
      
      // Clear iOS app badge number
      Pushy.clearBadge();
  })
}

export function initialize() {
  if (Capacitor.getPlatform() === 'web') {
    // maybe do browser notifications here
    console.log('running in browser - skipping notification setup')
    return
  }
  listen()
  register()
  toggleInAppBanner(true)
  setNotificationListener()
}