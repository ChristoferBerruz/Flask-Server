if (-not (Test-Path env:FLASK_APP)) { $env:FLASK_APP = "app" }
if (-not (Test-Path env:FLASK_ENV)) { $env:FLASK_ENV = "development" }
flask run