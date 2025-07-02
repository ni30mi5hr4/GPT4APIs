<?php
// Get the prompt from the client-side
$prompt = $_POST['prompt'];

// Fetch the nonce from the GPT4Free chat page
$nonceUrl = 'https://gpt4free.io/chat';
$nonceResponse = file_get_contents($nonceUrl);

// Extract the nonce from the HTML response
preg_match('/data-system="([^"]+)"/', $nonceResponse, $matches);
$nonceData = json_decode(html_entity_decode($matches[1]), true);
$nonce = $nonceData['restNonce'];

// Set up the request to GPT-4 endpoint
$gptUrl = 'https://gpt4free.io/wp-json/mwai-ui/v1/chats/submit';
$gptParams = [
    'botId' => 'default',
    'customId' => null,
    'session' => 'N/A',
    'chatId' => generateRandomString(10),
    'contextId' => rand(0, 9999),
    'messages' => [[
        'content' => 'You are a helpful assistant.',
        'id' => generateRandomString(10),
        'role' => 'system'
    ]],
    'newMessage' => $prompt,
    'newFileId' => null,
    'stream' => true
];
$gptHeaders = [
    'Content-Type: application/json',
    'X-WP-Nonce: ' . $nonce
];

// Send the request to GPT-4 endpoint
$ch = curl_init($gptUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($gptParams));
curl_setopt($ch, CURLOPT_HTTPHEADER, $gptHeaders);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$gptResponse = curl_exec($ch);
curl_close($ch);

// Return the response to the client-side
echo $gptResponse;

// Helper function to generate random string
function generateRandomString($length = 10) {
    $characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
}
?>
