# Get DoorDash Orders History 

A Python script to retrieve your DoorDash order history from Gmail and export it to a CSV file as doordash doesn't have an api endpoint for customers to fetch the orders history. 

## Description

This tool fetches all DoorDash order confirmation emails in your Gmail account using the Gmail API. It extracts the date of the order and the total amount spent and saves this information into a CSV file.

## Use Cases

- **Order Tracking**: Keep a track of your DoorDash orders, including the date and total expenditure.
- **Expense Management**: Useful for personal finance management, to include your food delivery expenses in budgeting.
- **Data Analysis**: Analyze your ordering habits over time or compute total spend.

## Getting Started

### Dependencies

- Python 3.x
- `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

### Installing

- Clone the repository or download the script to your local machine.
- Install the dependencies using `pip`:

  ```sh
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Ensure you have a credentials.json file for the Gmail API. This can be obtained from the Google Cloud Console by creating a project, enabling the Gmail API, and creating credentials.
Executing program

Follow the OAuth flow in the browser to authenticate.



License
This project is licensed under the MIT License.

Acknowledgments
This script was created for personal use to track DoorDash orders.
Thanks to the contributors who may help in improving this project.

Run the script with the required flags:
```sh
python get_my_doordash_orders.py --credentials "path/to/credentials.json" --output "path/to/output.csv"


