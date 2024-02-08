# ContactBridge

ContactBridge is a web platform designed to seamlessly integrate with existing websites, enabling them to set up and receive messages from contact forms efficiently. Built with a focus on simplicity and functionality, ContactBridge offers a streamlined process for managing contact form submissions, including spam detection, storage, and notification functionalities.

## Technologies

ContactBridge leverages a robust stack of technologies to ensure a seamless, efficient, and scalable service:

- **Flask**: A lightweight WSGI web application framework in Python, enabling rapid development and server management.
- **RestXT (with OpenAPI UI)**: Provides a straightforward, standards-based way to define and expose RESTful APIs, complete with interactive documentation through OpenAPI UI.
- **MaterializeCSS**: A modern responsive front-end framework based on Material Design, ensuring an intuitive and responsive admin portal.
- **HTMX**: Offers dynamic interactions with the web pages, enhancing the user experience without requiring complex JavaScript frameworks.
- **SQLite**: Currently utilized for the lightweight and serverless database needs, ensuring quick setup and ease of message storage.
- **MySQL**: Planned migration for enhanced scalability and performance in handling larger datasets.

## Sequence Diagram

The following sequence diagram illustrates the workflow of ContactBridge from message submission to processing and notification.

![Sequence Diagram](/assets/sequenceDiagram.svg)

## Usage

### Integrating ContactBridge

To integrate ContactBridge into your website, follow these steps:

1. Include a reference to the ContactBridge script in your website's HTML.
2. Configure the contact form to point to the ContactBridge endpoint.
3. Customize the settings in the ContactBridge admin portal to match your website's needs.

### Admin Portal

The admin portal allows administrators to:

- View all received messages in a centralized dashboard.
- Configure email notification settings.
- Manage spam filters and review messages categorized as spam.

## Future Plans

- **Database Migration**: Transitioning from SQLite to MySQL for improved performance and scalability.
- **Enhanced Spam Detection**: Implementing more sophisticated algorithms for spam detection to reduce false positives and ensure important messages are promptly delivered.
