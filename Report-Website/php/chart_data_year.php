<?php   
    session_start();

include ("../config/config.inc.php");

// Function to retrieve gender data for a specific year
function getGenderData($year) {
    global $host, $username, $password, $dbname;
    
    try {
        // PDO connection
        $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
        // Set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Retrieve data from the "Gender" table for the specified year
        $sql = "SELECT GENDER, COUNT(*) AS count FROM CustomerService WHERE YEAR = :year GROUP BY GENDER";

        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':year', $year, PDO::PARAM_INT);
        $stmt->execute();

        $gender_data = array();
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            // Explicitly cast the count to integer
            $gender_data[$row['GENDER']] = (int)$row['count'];
        }

        return $gender_data;
    } catch(PDOException $e) {
        return array('error' => 'Connection failed: ' . $e->getMessage());
    }
}

// Usage: Retrieve year from query parameters
$gender_data = getGenderData($_SESSION['year']);

// Output the data as JSON
echo json_encode($gender_data);
?>
