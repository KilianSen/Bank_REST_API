# BankSys RESTlike API
This page is served to explain the usage of the *BankSys* API.

## Account
An account instance represents a realworld bank account.
|Account|DataType|
|--|--|
|uuid		|str		|
|name		|str		|
|transaction_ids| list of str		|
|CREDIT_POSSIBLE| bool		|
|CREDIT_MAX| float		|
|balance| float		|

*the **balance** is calculated when called adding up all **transactions** from and to the account*


### Get
Sending a `get` request to `/account` using the parameter `uuid` containing an uuid **string** will yield a **json** object containing the account information including **current balance**.

#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/account?uuid=[PUT_UUID_HERE_WITHOUT_BRACKETS]
```

##### Python 3
```python
import requests
requests.get('{IP_ADDRESS}:{PORT}/account',  {'uuid':'[PUT_UUID_HERE_WITHOUT_BRACKETS]'})
```

### Create
Sending a `post` request to `/account` using the parameter `name` containing a **string** will create a new account and **return** the uuid cast in **json**.


#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/account?name=[PUT_NAME_HERE_WITHOUT_BRACKETS]
```

##### Python 3
```python
import requests
requests.post('{IP_ADDRESS}:{PORT}/account',  {'name':'[PUT_NAME_HERE_WITHOUT_BRACKETS]'})
```


### Accounts
To get all avaiable account uuid's you have to call get request to `/accounts` without any arguments.

#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/accounts
```

##### Python 3
```python
import requests
requests.get('{IP_ADDRESS}:{PORT}/accounts')
```


## Transaction
Represents a transaction between an origin account and a destination account.
|Transaction|DataType|
|--|--|
|uuid		|str		|
|origin|str		|
|destination| str		|
|value| float		|


### Get
Sending a `get` request to `/transaction` using the parameter `uuid` containing an uuid **string** will yield a **json** object containing the transaction information.

#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/transaction?uuid=[PUT_UUID_HERE_WITHOUT_BRACKETS]
```

##### Python 3
```python
import requests
requests.get('{IP_ADDRESS}:{PORT}/transaction',  {'uuid':'[PUT_UUID_HERE_WITHOUT_BRACKETS]'})
```

### Create
Sending a `post` request to `/transaction` using the parameter `name` containing a **string** will create a new account and **return** the uuid cast in **json**.


#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/transaction?origin=[origin]&destination=[destination]&value=[value]
```

##### Python 3
```python
import requests
requests.post('{IP_ADDRESS}:{PORT}/transaction',  {'origin':'[ORIGIN]', 'destination':'[DESTINATION]', 'value': [floatValue]})
```

### Transactions
To get all avaiable transaction uuid's you have to call `get` request to `/transactions` without any arguments.

#### Examples
##### URL
```batch
http://{IP_ADDRESS}:{PORT}/transactions
```

##### Python 3
```python
import requests
requests.get('{IP_ADDRESS}:{PORT}/transactions')
```

