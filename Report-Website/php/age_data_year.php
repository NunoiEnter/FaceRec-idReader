<?php
    session_start();
    include ("../config/config.inc.php");


    try {
        $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Query to fetch data
        $query = "SELECT *, (YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543) AS AGE, CASE
            WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) < 20 THEN 'น้อยกว่า 20'
            WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) BETWEEN 21 AND 40 THEN '21-40'
            WHEN ((YEAR(CURDATE()) - YEAR(STR_TO_DATE(DATE_OF_BIRTH, '%Y-%m-%d')) + 543)) BETWEEN 41 AND 59 THEN '41-59'
            ELSE 'มากกว่า 60'
            END AS AGE_GROUP, GENDER FROM CustomerService WHERE YEAR =".$_SESSION['year'];
        $stmt = $conn->prepare($query);
        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Initialize arrays for male and female age data
        $male_age_data = array(
            "น้อยกว่า 20" => 0,
            "21-40" => 0,
            "41-59" => 0,
            "มากกว่า 60" => 0
        );
        $female_age_data = array(
            "น้อยกว่า 20" => 0,
            "21-40" => 0,
            "41-59" => 0,
            "มากกว่า 60" => 0
        );

        // Count male and female age data
        foreach ($result as $row) {
            $ageGroup = $row['AGE_GROUP'];
            $gender = $row['GENDER'];
            if ($gender == "M") {
                $male_age_data[$ageGroup]++;
            } else {
                $female_age_data[$ageGroup]++;
            }
        }

        // Output data as JSON
        echo json_encode(array("male" => $male_age_data, "female" => $female_age_data));
    } catch(PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
    ?>
