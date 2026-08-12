<!DOCTYPE html>
<html lang="en">
<head>
    <title>AI Shelf Life Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-success p-3">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">🥦 AI Shelf Life Predictor</a>
            <div>
                <a href="{{ url_for('login') }}" class="btn btn-outline-light me-2">Login</a>
                <a href="{{ url_for('register') }}" class="btn btn-light">Register</a>
            </div>
        </div>
    </nav>
    <div class="container text-center my-5 py-5">
        <h1 class="display-4 fw-bold text-success">AI Shelf Life Predictor</h1>
        <p class="lead text-muted">Smart Food Expiry Prediction & Notification System</p>
        <a href="{{ url_for('register') }}" class="btn btn-success btn-lg mt-3">Get Started</a>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>