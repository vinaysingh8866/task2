
# Stock Trading Backend

Stock Trading Backend made with Python Flask 


## API Reference

#### Authentication

```http
  POST /api/login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. Your email  |
| `password` | `string` | **Required**. Your password  |


```http
  POST /api/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. Your email  |
| `password` | `string` | **Required**. Your password  |
| `uname` | `string` | **Required**. Your user name  |

Log Out
```http
  POST /api/logout
```


Test Auth Token
```http
  POST /api/token_test
```

pass bearer token for testing token


Get new Auth token
```http
  POST /api/new_token
```
#### Stocks

Add new asset 
```http
  GET /api/add_stock
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. name of asset |
| `balance` | `string` | **Required**. balance of asset  |


Get user portfolio
```http
  GET /api/get_stock
```


Sell Stock
```http
  GET /api/sell_stock
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `aid` | `string` | **Required**. asset Id |
| `amount` | `string` | **Required**. amount to sell  |

Sell Stock
```http
  GET /api/buy_stock
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `aid` | `string` | **Required**. asset Id |
| `amount` | `string` | **Required**. amount to buy  |

## Installation

Install requirements

```bash
  pip3 install -r requirements.txt
```
    
## Running Tests

To run tests, run the following command

```bash
  python3 test.py
```


## Deployment

To deploy this project run

```bash
  npm run deploy
```


## Run Locally

Start the server

```bash
  python3 app.py
```

