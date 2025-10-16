# Idle Horde Slayer

This is an idle game where a hero automatically fights hordes of enemies, and the player focuses on upgrading skills and abilities to make the hero stronger. The project is being developed in Python using the Kivy framework.

## Getting Started on Windows

Follow these instructions to get a copy of the project up and running on your local Windows machine for development and testing.

### Prerequisites

*   **Python:** You need to have Python installed. If you don't have it, download it from [python.org](https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during installation.
*   **GitHub Desktop:** You will need [GitHub Desktop](https://desktop.github.com/) to easily clone and manage the project.

### Installation & Running the Game

1.  **Clone the Repository:**
    *   Open GitHub Desktop.
    *   Go to `File` > `Clone Repository`.
    *   Select the `Idle-Horde-Slayer` repository from the list.
    *   Choose a suitable folder on your computer (e.g., `C:\Users\YourUser\Documents\GitHub`).
    *   Click `Clone`.

2.  **Open a Command Prompt in the Project Folder:**
    *   After cloning, GitHub Desktop should show you the project. Click the `Show in Explorer` button.
    *   In the Explorer window that opens, click in the address bar at the top, type `cmd`, and press `Enter`. This will open a command prompt directly in the project folder.

3.  **Set Up a Virtual Environment:**
    *   In the command prompt you just opened, run the following commands one by one:
    ```bash
    # This creates a virtual environment folder named 'venv'
    python -m venv venv

    # This activates the virtual environment. You should see (venv) at the start of your prompt line.
    .\venv\Scripts\activate
    ```

4.  **Install Required Packages:**
    *   With the virtual environment still active, install all the necessary packages by running:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Game!**
    *   You're all set! To start the game, simply run:
    ```bash
    python main.py
    ```
    The game window should appear on your screen.

## Project Structure

*   `main.py`: The main entry point for the application.
*   `README.md`: This file.
*   `requirements.txt`: A list of Python dependencies for the project.
*   `assets/`: Contains all game assets like sprites and sounds (currently empty).
*   `src/`: Contains the core source code for the game logic and entities.