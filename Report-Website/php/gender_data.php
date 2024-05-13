<?php
// Establish database connection


try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Fetch gender data from database
    $sql = "SELECT GENDER FROM ID_CARD";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    
    // Initialize variables
    $maleCount = 0;
    $femaleCount = 0;
    
    // Count genders
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        if ($row["GENDER"] == "M") {
            $maleCount++;
        } elseif ($row["GENDER"] == "F") {
            $femaleCount++;
        }
    }
    
    // Return gender counts
    $genderData = array(
        "maleCount" => $maleCount,
        "femaleCount" => $femaleCount
    );
    $jsonGenderData = json_encode($genderData);
    
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
