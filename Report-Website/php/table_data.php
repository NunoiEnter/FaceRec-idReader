<?php
include ("./config/config.inc.php");

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Count total records
    $total_records_query = "SELECT COUNT(*) AS total FROM ID_CARD";
    $stmt = $conn->prepare($total_records_query);
    $stmt->execute();
    $total_records = $stmt->fetch(PDO::FETCH_ASSOC)['total'];

    // Query to fetch all data
    $query = "SELECT *, (YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543) AS AGE, CASE
        WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) < 20 THEN 'น้อยกว่า 20'
        WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) BETWEEN 21 AND 40 THEN '21-40'
        WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) BETWEEN 41 AND 59 THEN '41-59'
        ELSE 'มากกว่า 60'
        END AS AGE_GROUP FROM ID_CARD";
    $stmt = $conn->prepare($query);
    $stmt->execute();
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Grouping data by age and gender
    $ageGroups = array(
        'น้อยกว่า 20' => array('ชาย' => 0, 'หญิง' => 0, 'รวม' => 0),
        '21-40' => array('ชาย' => 0, 'หญิง' => 0, 'รวม' => 0),
        '41-59' => array('ชาย' => 0, 'หญิง' => 0, 'รวม' => 0),
        'มากกว่า 60' => array('ชาย' => 0, 'หญิง' => 0, 'รวม' => 0)
    );
    foreach ($result as $row) {
        $ageGroup = $row['AGE_GROUP'];
        $gender = $row['GENDER'] == "M" ? 'ชาย' : 'หญิง';
        $ageGroups[$ageGroup][$gender]++;
        $ageGroups[$ageGroup]['รวม']++;
    }

    // Display table
    echo '<table>';
    // Table header
    echo '<thead>';
    echo '<tr><th>ช่วงอายุ</th><th>ชาย</th><th>หญิง</th><th>รวม</th></tr>';
    echo '</thead>';
    // Table body
    echo '<tbody>';
    foreach ($ageGroups as $ageGroup => $genderCounts) {
        echo '<tr>';
        echo '<td>'.$ageGroup.'</td>';
        foreach ($genderCounts as $count) {
            echo '<td>'.$count.'</td>';
        }
        echo '</tr>';
    }
    echo '</tbody>';
    echo '</table>';

} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
$conn = null;
?>
