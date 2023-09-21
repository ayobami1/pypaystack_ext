# PyPaystack Extension

This Python script provides a seamless integration with the Paystack API using the PyPaystack library. It allows you to perform various actions related to creating and managing Paystack transactions, customers, and subscription plans.

## Prerequisites

Before using this script, make sure you have the following:

- Python installed on your system.
- The `pypaystack` library installed. You can install it using pip:

pip install pypaystack


- A Paystack API key. You can obtain this key by signing up for a Paystack account and creating an API key in your Paystack dashboard.

- An SMS gateway service configured (if you plan to send SMS OTPs).

## Getting Started

1. Clone or download this repository to your local machine.

2. Set your Paystack API key as an environment variable. You can do this by exporting it in your terminal:


## Features

### 1. Create and Manage Plans

You can create and manage subscription plans using the `create_plans` function. It allows you to define various parameters for your plans, such as name, amount, interval, currency, and more.

### 2. Manage Customer Profiles

The `manage_customers_profile` function enables you to create, fetch, and update customer profiles. It's essential for creating customers before making payments and managing their details.

### 3. Make Transactions

The `make_transaction` function facilitates payment transactions. It generates a unique reference for each transaction, handles customer authentication, and provides the option to store authentication codes for future charges.

### 4. Validate Account Numbers

The `validate_account_number` function helps you validate bank account numbers before processing transactions. It fetches a list of banks and their codes, allowing you to verify account details.

## Usage

1. Set up your environment variables with your Paystack API key.

2. Customize the script according to your needs, including customer details, transaction amounts, and other parameters.

3. Run the script to perform various Paystack-related actions.

## Contributing

Contributions and improvements to this code are welcome. Feel free to open issues or pull requests to suggest changes or report problems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
