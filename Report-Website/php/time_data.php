<?php
// Establish database connection
include ("../config/config.inc.php");

try {
    // Create connection
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // Set the PDO error mode to exception
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Query to fetch data for all months and years
    $sql = "SELECT MONTH, COUNT(*) AS customer_count 
            FROM CustomerService 
            GROUP BY MONTH";

    $stmt = $pdo->query($sql);
    
    $data = array();

    if ($stmt->rowCount() > 0) {
        // Output data of each row
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            // Storing customer count in corresponding month
            $data[$row["MONTH"]] = $row["customer_count"];
        }
    } else {
        echo "0 results";
    }
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}

// Outputting data in JSON format
header('Content-Type: application/json');
echo json_encode($data);
?>
