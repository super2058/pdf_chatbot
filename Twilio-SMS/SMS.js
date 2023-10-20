const twilio = require("twilio");

// Your Twilio Account SID and Auth Token
const accountSid = "YOUR_ACCOUNT_SID";
const authToken = "YOUR_AUTH_TOKEN";

// Initialize Twilio client
const client = new twilio(accountSid, authToken);

// Function to send SMS
function sendOrderingLinkSMS(phoneNumber, orderingLink) {
  const messageBody = `Hello! You can place your order using this link: ${orderingLink}`;

  client.messages
    .create({
      body: messageBody,
      from: "YOUR_TWILIO_PHONE_NUMBER", // Replace with your Twilio phone number
      to: phoneNumber, // The recipient's phone number
    })
    .then((message) => console.log(`SMS sent with SID: ${message.sid}`))
    .catch((error) => console.error(error));
}

// Usage
const phoneNumber = "+1234567890"; // Replace with the recipient's phone number
const orderingLink = "https://yourwebsite.com/order"; // Replace with your ordering link

sendOrderingLinkSMS(phoneNumber, orderingLink);
