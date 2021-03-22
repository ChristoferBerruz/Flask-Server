if (-not (Test-Path env:FLASK_APP)) { $env:FLASK_APP = "app" }
flask run