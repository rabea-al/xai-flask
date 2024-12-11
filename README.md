<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>





<p align="center"><i>Xircuits Component Library for Flask! Simplify building and managing web applications with seamless integration.</i></p>

---
## Xircuits Component Library for Flask

A comprehensive suite of components designed for creating and managing web applications using Flask within the Xircuits environment.

## Table of Contents

- [Preview](#preview)
- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Try the Examples](#try-the-examples)
- [Installation](#installation)

## Preview

### InlineExample

<img src="https://github.com/user-attachments/assets/98329220-a990-4544-8474-acb615faf8d2" alt="InlineExample"/>

### InlineExample Result

<img src="https://github.com/user-attachments/assets/2740efd3-a361-4a10-a3a7-fca7391a9f33" alt="InlineExample_result"/>

### DeclarativeExample

<img src="https://github.com/user-attachments/assets/3331fb55-0142-42cf-9334-34627ba1e389" alt="DeclarativeExample" />

### DeclarativeExample Result

<img src="https://github.com/user-attachments/assets/47bd947c-c98f-4fc8-991f-5aa9f3eb29f4" alt="DeclarativeExample_result py" />

## Prerequisites

Before you begin, you will need the following:

1. Python3.9+.
2. Xircuits.

## Main Xircuits Components

### FlaskCreateApp Component:
Initializes a Flask application, allowing customization of public paths, static URL paths, and secret key settings for enhanced flexibility.

<img src="https://github.com/user-attachments/assets/eb1b078a-1059-4c21-bb1a-0c04767adc9f" alt="FlaskCreateApp" width="200" height="150" />

### FlaskStartServer Component:
Starts the Flask application server, with options to configure debug mode, host address, and port number.

<img src="https://github.com/user-attachments/assets/a336a86e-3c37-46fa-9b78-561e2bfac855" alt="FlaskStartServer" width="200" height="125" />

### FlaskDefineGetRoute Component:
Defines a GET route in the Flask application, linking it to specific actions or components to handle incoming requests.


### FlaskDefinePostRoute Component:
Defines a POST route in the Flask application, enabling execution of actions or components when POST requests are received.


### FlaskDefinePutRoute Component:
Defines a PUT route in the Flask application, linking it to specific actions or components for handling PUT requests.


### FlaskRenderTemplate Component:
Renders dynamic HTML templates with the ability to pass variables for personalized content delivery.


### FlaskReturnStringResponse Component:
Sends a plain text response to the client, ideal for returning simple messages or lightweight API data.


### FlaskReturnJSONResponse Component:
Returns structured JSON data, making it essential for APIs or applications requiring client-side data parsing.


### FlaskRedirect Component:
Redirects users to a different URL, enabling seamless navigation and flow control within the web application.


## Try the Examples

We have provided an example workflow to help you get started with the Flask component library. Give it a try and see how you can create custom Flask components for your applications.

### InlineExample

This example creates a Flask server using Xircuits, featuring two routes:  
1. **POST `/echo`**: Accepts JSON input, processes it, and returns the input as a plain text response.  
2. **GET `/greet`**: Returns a JSON response with a greeting message.  

It demonstrates inline route definitions and dynamic request handling.

### DeclarativeExample

This example sets up a Flask server with multiple routes:  
1. **GET `/hello/<name>`**: Displays the path parameter `<name>` in a structured response.  
2. **POST `/hello/<name>`**: Accepts JSON input and returns it as a JSON response.  
3. **GET `/stream`**: Streams a response to the client in chunks, demonstrating real-time data streaming.  
4. **PUT `/<some>/<path>/<parameters>`**: Processes path parameters and prints them for debugging.  
5. **Interval Job**: Prints a message every 5 seconds using a background job scheduler.  

It showcases both route definitions and advanced Flask features like streaming and scheduled tasks.

## Installation
To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the Flask library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install flask
```
You can also install it manually by cloning and installing it:
```
# base Xircuits directory  
git clone https://github.com/XpressAI/xai-flask xai_components/xai_flask  
pip install -r xai_components/xai_flask/requirements.txt  
```
