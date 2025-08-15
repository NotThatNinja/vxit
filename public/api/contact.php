<?php
// CORS (for development)
// header('Access-Control-Allow-Origin: http://localhost:4321');
// header('Access-Control-Allow-Methods: POST, OPTIONS');
// header('Access-Control-Allow-Headers: Content-Type');

// if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
//     http_response_code(200);
//     exit;
// }

header('Content-Type: application/json');

if (isset($_GET['action']) && $_GET['action'] === 'submit') {
    // Retrieve form data
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    $name = trim($data['name']);
    $email = filter_var(trim($data['email']), FILTER_SANITIZE_EMAIL);
    $phone = !empty(trim($data['phone'])) ? trim($data['phone']) : 'N/A';
    $subject = trim($data['subject']);
    $message = trim($data['message']);
    $privacy = filter_var($data['privacy'], FILTER_VALIDATE_BOOLEAN);

    // Validation
    $errors = [];

    if (empty($name)) {
        $errors[] = 'Name is required.';
    }

    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Valid email is required.';
    }

    if (empty($subject)) {
        $errors[] = 'Subject is required.';
    }

    if (empty($message)) {
        $errors[] = 'Message is required.';
    }

    if (!$privacy) {
        $errors[] = 'You must accept the privacy policy.';
    }

    if (strlen($name) > 100) {
        $errors[] = 'Name must be less than 100 characters.';
    }

    if (strlen($email) > 100) {
        $errors[] = 'Email must be less than 100 characters.';
    }

    if (strlen($phone) > 100) {
        $errors[] = 'Phone must be less than 100 characters.';
    }

    if (strlen($subject) > 100) {
        $errors[] = 'Subject must be less than 100 characters.';
    }

    if (strlen($message) > 5000) {
        $errors[] = 'Message must be less than 5000 characters.';
    }

    if (!empty($errors)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'errors' => $errors]);
        exit;
    }

    // Submit form (remove newlines from name to prevent header injection)
    $safe_name = str_replace(["\r", "\n"], '', $name);

    $to = 'contactus@vxit.io';
    $headers = "From: $safe_name <$email>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    $email_subject = "Contact Form: $subject";
    $email_body = "Name: $name\nEmail: $email\nPhone: $phone\nSubject: $subject\nMessage:\n$message";

    $mail_sent = mail($to, $email_subject, $email_body, $headers);

    if ($mail_sent) {
        http_response_code(200);
        echo json_encode(['success' => true, 'message' => 'Your message has been sent! We will get back to you shortly.']);
    } else {
        http_response_code(500);
        echo json_encode(['success' => false, 'errors' => ['Failed to send email.']]);
    }
}
?>
