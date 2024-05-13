<?php
    session_start();
    include ("../config/config.inc.php");

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch data for all months and years of 2567
$sql = "SELECT MONTH, COUNT(*) AS customer_count 
        FROM CustomerService 
        WHERE YEAR = ".$_SESSION['year'].
        " GROUP BY MONTH";

$result = $conn->query($sql);

$data = array();

if ($result->num_rows > 0) {
    // Output data of each row
    while ($row = $result->fetch_assoc()) {
        // Storing customer count in corresponding month
        $data[$row["MONTH"]] = $row["customer_count"];
    }
} else {
    echo "0 results";
}

$conn->close();

// Outputting data in JSON format
header('Content-Type: application/json');
echo json_encode($data);
?>
