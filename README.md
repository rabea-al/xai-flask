## Xircuits Flask Component Library

A comprehensive suite of components designed for creating and managing web applications using Flask within the [Xircuits](https://xircuits.io) environment. 


### Installation

To use this component library in Xircuits, simply run the Xircuits install command from your working directory.

```bash
xircuits install flask
```

Alternatively, you may also clone this repository into your `xai_components` directory and install it manually via
```
pip install -r requirements.txt
```

### Components
- **FlaskCreateApp**: Initializes a Flask application with customizable public path, static URL path, and secret key settings.
- **FlaskStartServer**: Launches the Flask application server, with options for setting debug mode, host address, and port number.
- **FlaskDefineGetRoute**: Defines a route for HTTP GET requests and associates it with a specific component or action to be executed when the route is accessed.
- **FlaskDefinePostRoute**: Similar to FlaskDefineGetRoute, but for HTTP POST requests, allowing the execution of components or actions upon receiving a POST request at the specified route.
- **FlaskDefinePutRoute**: Similar to FlaskDefineGetRoute, but for HTTP PUT requests, allowing the execution of components or actions upon receiving a PUT request at the specified route.
- **FlaskInlineDefineGetRoute**: Defines a route for HTTP GET requests in line with the main execution flow and associates it with a specific component or action to be executed when the route is accessed.
- **FlaskInlineDefinePostRoute**: Similar to FlaskInlineDefineGetRoute, but for HTTP POST requests, allowing the execution of components or actions upon receiving a POST request at the specified route.
- **FlaskInlineDefinePutRoute**: Similar to FlaskInlineDefineGetRoute, but for HTTP PUT requests, allowing the execution of components or actions upon receiving a PUT request at the specified route.
- **FlaskRenderTemplate**: Renders an HTML template, with the ability to pass variables to the template for dynamic content generation.
- **FlaskReturnStringResponse**: Sends a plain text response to the client, useful for simple messages or API endpoints returning textual data.
- **FlaskReturnJSONResponse**: Facilitates the return of JSON responses, ideal for API services where structured data needs to be communicated to the client.
- **FlaskReturnResponse**: Sends any supported flask response to the client, useful if you need to do something where the other response components are too limiting.
- **FlaskRedirect**: Redirects the client to a different URL, useful for navigation and flow control within a web application.
- **FlaskSessionPop**: Removes a specified key from the Flask session, useful for clearing session data.
- **FlaskSessionSet**: Sets a value in the Flask session under a specified key, enabling session-based data storage and retrieval.
- **FlaskSessionGet**: Retrieves a value from the Flask session, identified by a specific key, allowing for the use of session data across different components and routes.
- **FlaskSessionExists**: Checks for the existence of a specific key in the Flask session, useful for conditional logic based on session data.
- **FlaskGetFormValue**: Extracts a value from form data submitted via POST request, essential for processing user input in web forms.
- **FlaskGetRequestJson**: Retrieves JSON data from a request payload.
- **FlaskInitScheduler**: Initializes a scheduler for running background jobs. 
- **FlaskCreateIntervalJob**: Declaratively creates a scheduled interval job.
- **FlaskInlineCreateIntervalJob**: Creates a scheduled interval job in line with the main execution flow.

