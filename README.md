# Activities2Notion
This Python project fetches your latest Strava activities and uploads them to a Notion database. It uses Strava's OAuth authentication to get the necessary tokens, fetches the latest activity data, and sends it to Notion, updating the database every time new data is available.

---
## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Setup](#setup)
4. [Run the Project](#run-the-project)
5. [Strava Authentication](#strava-authentication)
6. [Notion Integration](#notion-integration)
7. [Future Plans](#future-plans)
8. [Important Documentations](#important-documentation)
9. [License](#license)
---

## Overview
This project integrates with the Strava API to extract activity data and automatically upload it to a Notion database. The flow is as follows:

  1. **Authentication**: Use Strava's OAuth process to get the necessary tokens.

  2. **Fetch Activity**: Get the latest activity data from Strava.
   
  3. **Upload to Notion**: Automatically upload the data to a designated Notion database.

## Requirements


Before running the project, you need to have the following installed:

  - Python 3.9+
  - Pip (for installing dependencies)
  - Notion API Token (for Notion integration)
  - Strava API Credentials (for Strava integration)

## Setup
1. Clone the Repository
    ```
    git clone https://github.com/yourusername/strava2notion.git
    cd strava2notion
    ```
2. Install Dependencies
    Install the required Python libraries by running:
    ```
    pip install -r requirements.txt
    ````
3. Configure Environment Variables
    Create a `.env file in the root directory by copying the .env.example which is also in the root directory. Should look something like this:
    
    ```
    STRAVA_CLIENT_ID=your_strava_client_id
    STRAVA_CLIENT_SECRET=your_strava_client_secret
    STRAVA_REFRESH_TOKEN=your_strava_refresh_token
    STRAVA_ACCESS_TOKEN=your_strava_access_token
    STRAVA_TOKEN_EXPIRY=your_strava_token_expiry_timestamp
    NOTION_API_TOKEN=your_notion_api_token
    NOTION_DATABASE_ID=your_notion_database_id
    ```
To get these values, follow the steps below.

## Run the Project
1. Run the Script
Once your .env file is set up, simply run the main.py script:
```
python src/main.py
```

During the first run, the script will prompt you for authorization and automatically fetch the necessary tokens to connect to Strava and Notion.

## Strava Authentication

#### Obtain a Refresh Token and Access Token

To get the refresh token and access token, you need to go through the OAuth process. This will be handled automatically the first time you run main.py. Here's the process:

  1. Run the Script:
     - When running main.py for the first time, the script will prompt you to authorize the app and enter the authorization code.
  2. Authorize the App:
     - The script will print a URL for you to visit in your browser:
         ```
         Please authorize the app by visiting this URL:
         https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost/exchange_token&response_type=code&scope=read,activity:read,activity:write
          ```
     - Visit this URL, log in with your Strava account, and grant the app permission to access your activity data.
       
  3. Obtain the Authorization Code:

     - After granting permissions, you will be redirected to `https://localhost/exchange_token`, where you will see a URL containing a code parameter (e.g., `https://localhost/exchange_token?code=AUTHORIZATION_CODE`).
      - Copy this `AUTHORIZATION_CODE` from the URL.

  4. Enter the Authorization Code:
      - Paste the `AUTHORIZATION_CODE` into the terminal when prompted:

        ```
        Enter the code from the URL: [PASTE_AUTHORIZATION_CODE_HERE]
        ```

   5. Receive Your Tokens:
       - The script will exchange the authorization code for the access token and refresh token, and store them in your `.env` file.

> You can now use the access token and refresh token in the project to interact
> with Strava.

## Notion Integration
This project uses the Notion API to create a database entry for each activity you fetch from Strava. To integrate with Notion:

 1. Get Your Notion API Token:
     - Go to Notion Developers and create a new integration to obtain your API token.

  2. Get Your Notion Database ID:
     - Open your Notion database.
     - The URL should look something like     
`https://www.notion.so/yourusername/Database####Name####xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.
     - The string `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` is your database ID, which you will need to input in the `.env` file.

## Future Plans
The project is in its early stages, and there are several exciting features and enhancements planned for the future:

  1. Automatic Updates with Triggers:

      I plan to implement a trigger system that will automatically update the Notion database whenever new activity data is available from Strava. This would remove the need for manual intervention and ensure the Notion database is always up-to-date with the latest fitness data.

  3. Public Notion Integration:

      In the future, I aim to create a public Notion integration that allows users to easily connect their Strava account and upload their activity data to Notion without needing to clone the repository or run scripts. This will make the integration seamless and accessible to a wider audience directly within Notion.

  5. Integration with Other Fitness Platforms:

     I also plan to extend the integration beyond Strava by adding support for other fitness tracking applications. Some of the platforms I intend to integrate include:
        - Coros (I plan to work on this as I currently use a Coros)
        - Garmin
        - Suunto
        - Apple Watch
        
Any contributions from the community who are interested in helping integrate these or other platforms are welcomed. If you have experience with any of these systems and want to contribute, please feel free to reach out or submit pull requests!

I'd love for this project to be a team effort, not just an individual one!

## Important Documentation
  - [Strava API Docs](https://developers.strava.com/)
  - [Notion API Docs](https://developers.notion.com/docs/getting-started)
  - [Python Docs](https://docs.python.org/3.8/)
## License
This project is licensed under the MIT License #### see the [LICENSE](https://github.com/diion-berisha/activities2notion/blob/main/LICENSE) file for details.

---
