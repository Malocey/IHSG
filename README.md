# Idle Horde Slayer

This is an idle game where a hero automatically fights hordes of enemies, and the player focuses on upgrading skills and abilities to make the hero stronger. The project is being developed in Python using the Kivy framework.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your computer. You can download it from the official website:
[python.org](https://www.python.org/downloads/)

You will also need [Git](https://git-scm.com/downloads/) or [GitHub Desktop](https://desktop.github.com/).

### Installation

1.  **Clone the repository:**

    *   **Using GitHub Desktop:**
        1.  In GitHub Desktop, go to `File` > `Clone Repository`.
        2.  Select the repository for this project.
        3.  Choose a local path on your computer where you want to save the project.
        4.  Click `Clone`.

    *   **Using the command line:**
        ```bash
        git clone <repository_url>
        cd <repository_folder>
        ```

2.  **Set up a virtual environment (Recommended):**
    Open a terminal or command prompt in the project folder and run:
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    With your virtual environment active, install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Game

Once the installation is complete, you can start the game by running the `main.py` script:

```bash
python main.py
```

This will launch the game window on your desktop.

## Project Structure

*   `main.py`: The main entry point for the application.
*   `AGENTS.md`: Instructions for AI agents working on this repository.
*   `README.md`: This file.
*   `requirements.txt`: A list of Python dependencies for the project.
*   `assets/`: Contains all game assets like sprites and sounds.
*   `docs/`: Contains project design documents.
*   `src/`: Contains the core source code for the game logic and entities.