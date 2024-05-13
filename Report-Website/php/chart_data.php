<?php
// Database connection
include ("../config/config.inc.php");


try {
    // PDO connection
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Retrieve data from the "Gender" table
    $sql = "SELECT GENDER, COUNT(*) as count FROM ID_CARD GROUP BY GENDER";
    $stmt = $conn->prepare($sql);
    $stmt->execute();

    $gender_data = array();
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        // Explicitly cast the count to integer
        $gender_data[$row['GENDER']] = (int)$row['count'];
    }

    // Output the data as JSON
    echo json_encode($gender_data);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
