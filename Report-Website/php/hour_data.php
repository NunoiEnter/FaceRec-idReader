<?php
// Establish database connection
$servername = "localhost";
$username = "auto";
$password = "password";
$dbname = "auto";

try {
    // Create connection
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Query to fetch data for all months and years
    $sql = "SELECT HOUR, COUNT(*) AS customer_count 
            FROM CustomerService 
            GROUP BY HOUR";

    $stmt = $conn->prepare($sql);
    $stmt->execute();

    $data = array();

    // Fetching data
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        // Storing customer count in corresponding month
        $data[$row["HOUR"]] = $row["customer_count"];
    }

    // Outputting data in JSON format
    header('Content-Type: application/json');
    echo json_encode($data);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>