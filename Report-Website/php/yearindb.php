<?php
include ("./config/config.inc.php");

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Count total records
    $total_records_query = "SELECT DISTINCT(YEAR) AS YEAR FROM auto.CustomerService ORDER by YEAR DESC;";
    // $total_records_query = "SELECT * FROM auto.CustomerService;";
    
    $stmt = $conn->prepare($total_records_query);
    $stmt->execute();

    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($result as $row) {

        echo '<li><a href="/yeargraph.php?year='.$row['YEAR'].'">'.$row['YEAR'].'</a>
             </li>';
            }

} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
$conn = null;
?>