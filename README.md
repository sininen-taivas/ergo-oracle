# Oracle Issue Script

## Usage

`python issue.py --api-key <API-KEY> --name <name> --description <description>`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--name` - Name of contract
- `--description` - Description of contract


# Price Script

## Usage

Basic usage: `python3 price.py --cmc-key <COINMARKETCAP APIKEY>`

## Coinmarketcap.com API key

You can specify CMC key either in --cmc-key option or in `var/config.json` file like:
```
{
    "coinmarketcap_api_key": "..."
}
```

# Common Update Script

## Usage

`python3 update.py --api-key <API-KEY> --mainnet --value <unsigned int63>`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--value` - price as an unsigned int63


# Update Script with USD/ERG price value 

## Usage

`python3 usd-erg-cmc-update.py --api-key <API-KEY> --cmc-key <COINMARKETCAP APIKEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--cmc-key` - coinmarketcap API key

# Update Script with EUR/ERG price value 

## Usage

`python3 eur-erg-cmc-update.py --api-key <API-KEY> --cmc-key <COINMARKETCAP APIKEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--cmc-key` - coinmarketcap API key

# Update Script with BTC/ERG price value (nanoErgo & milliBitcoin)

## Usage

`python3 btc-erg-cmc-update.py --api-key <API-KEY> --cmc-key <COINMARKETCAP APIKEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--cmc-key` - coinmarketcap API key

# Update Script with AUG/ERG price value 

## Usage

`python3 aug-erg-quandl-update.py --api-key <API-KEY> --cmc-key <COINMARKETCAP APIKEY> --quandl-key <QUANDL APIKEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--cmc-key` - coinmarketcap API key
- `--quandl-key` - quandl API key

# Update Script with AUG/USD price value 

## Usage

`python3 aug-usd-quandl-update.py --api-key <API-KEY> --quandl-key <QUANDL APIKEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--quandl-key` - quandl API key


# Clean Script

## Usage

`python3 clean.py --api-key <API-KEY> --mainnet`

## Command Line Options

- `-h`, `--help` - display available command line options
- `-s`, `--server` - use custom API server, default value is "localhost:9053"
- `-n`, `--network-log` - log network operations to console
- `-q`, `--quiet` - display result only, no debug output
- `--api-key` - API key to pass RPC node authentication
- `--stop` - Stop it!


## Automatic usage

Add to crontab
```cron
15 */4 * * * /path/usd-erg-cmc-update.py --api-key <API-KEY> --cmc-key <COINMARKETCAP APIKEY> --mainnet
*/30 * * * * /path/clean.py --api-key <API-KEY> --mainnet
10 */4 * * * /path/clean.py --api-key <API-KEY> --stop --mainnet --stop
```
