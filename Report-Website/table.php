<?php
include ("config/config.inc.php");

?>


<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="/css/report_styles.css">
    <style>
        /* Pagination styles */
        .pagination {
            margin-top: 20px;
        }

        .pagination a {
            color: #007bff;
            text-decoration: none;
            padding: 5px 10px;
            border: 1px solid #007bff;
            border-radius: 5px;
            margin-right: 5px;
        }

        .pagination a:hover {
            background-color: #007bff;
            color: #fff;
        }

        .pagination a:active {
            background-color: #0056b3;
            color: #fff;
        }

        /* Search box styles */
        .search-container {
            margin-top: 20px;
        }

        .search-box {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 300px;
            margin-bottom: 10px;
        }

        .search-btn {
            padding: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>

<body>
<nav class="navbar">
        <button class="toggle-btn" onclick="toggleSidebar()">☰</button>
        <div class="navbar-links">
            <a href="#">WEB_REPORT</a>
        </div>
    </nav>
    <div class="sidebar" id="sidebar">
        <ul>
            <li><a href="table.php">Home</a></li>
            <li><a href="table.php">ตารางผู้ใช้บริการ</a></li>
            <li><a href="graph.php">ข้อมูลการใช้งานบริการ</a></li>
            <button class="dropdown-btn">สัดส่วนการใช้บริการ
                <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-container">
                <?php
                include '/var/www/html/Project/COM/php/yearindb.php';
                ?>
            </div>
            </li>
            <li><a href="#">About</a></li>
        </ul>
    </div>
</nav>
    <div class="container">
        <h2>ข้อมูลผู้ใช้บริการ</h2>
        <div id="genderLabel" class="gender-label">
            <h2>ยอดผู้ใช้</h2>
            <div class="gender-info">
                <?php
                include '/var/www/html/Project/COM/php/gender_data.php';
                ?>
                <div class="gender-item">
                    <h3>ผู้ชาย</h3>
                    <p><?php echo $maleCount; ?></p>
                </div>
                <div class="gender-item">
                    <h3>ผู้หญิง</h3>
                    <p><?php echo $femaleCount; ?></p>
                </div>
                <div class="gender-item">
                    <h3>รวม</h3>
                    <p><?php echo $maleCount + $femaleCount; ?></p>
                </div>
            </div>
        </div>
        <div id="table-container">
            <?php include 'php/table_data.php';?>
        </div>
        <!-- Pagination -->
        <!-- <div class="pagination">
            <?php 
            // Previous and Next buttons
            // if ($page > 1) {
            //     echo '<a href="?page=' . ($page - 1) . '">Previous</a>';
            // }
            // if ($page < $total_pages) {
            //     echo '<a href="?page=' . ($page + 1) . '">Next</a>';
            // }
            ?>
        </div> -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="/JS/report_script.js"></script>

</html>
