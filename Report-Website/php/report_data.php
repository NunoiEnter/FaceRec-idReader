<?php
include ("../config/config.inc.php");

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Query to fetch age distribution data
    $query = "SELECT AGE_GROUP, GENDER, COUNT(*) AS count FROM ID_CARD GROUP BY AGE_GROUP, GENDER";
    $stmt = $conn->prepare($query);
    $stmt->execute();
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Initialize arrays for age distribution data
    $male_age_data = array();
    $female_age_data = array();

    // Populate arrays with age distribution data
    foreach ($result as $row) {
        $ageGroup = $row['AGE_GROUP'];
        $gender = $row['GENDER'] == "M" ? 'ชาย' : 'หญิง';
        $count = $row['count'];

        // Populate male or female age data based on gender
        if ($gender == 'ชาย') {
            $male_age_data[$ageGroup] = $count;
        } else {
            $female_age_data[$ageGroup] = $count;
        }
    }

    // Output data as JSON
    echo json_encode(array("male" => $male_age_data, "female" => $female_age_data));

} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
$conn = null;
?>
