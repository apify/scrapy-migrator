# scrapy-migrator

A standalone POC script for wrapping Scrapy projects with Apify middleware.

## Usage

```bash
npm i

## This runs the migration on the example project (./tutorial)
node ./src/index.js

cd tutorial
## This runs the example project wrapped in Apify middleware
pip install -r requirements.txt -r requirements_apify.txt
python -m tutorial
```

