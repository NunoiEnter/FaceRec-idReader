<?php

    session_start();
    include ("config/config.inc.php");

$_SESSION['year'] = isset($_GET['year']) ? $_GET['year'] : date('Y')+543; 


?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Table Data</title>
    <link rel="stylesheet" href="/css/styleg.css">
    <link rel="stylesheet" href="/css/report_styles.css">
    <script src="path/to/chartjs/dist/chart.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
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
                include 'php/yearindb.php';
                ?>
            </div>
            </li>
            <li><a href="#">About</a></li>
        </ul>
    </div>
</nav>
    <div class="container">
        <h2>สัดส่วนการใช้บริการปี <?php echo $_SESSION['year']; ?></h2>
        <div class="content" style="display: flex ;">
            <h2 style="display : flex ; margin-left: 35vh;">เปอร์เซนต์ผู้ใช่บริการ</h2>
            <h2 style="display : flex ; margin-right: 35vh;">สัดส่วนอายุผู้ใช้บริการ</h2>
        <div class="content">
            <div class="chart-container">
                <canvas id="genderChart"></canvas>
            </div>
                <div class="chart-container" style="position: relative;">

                    <canvas id="ageChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="graph-info">
                    <h2>สถิติเดือนที่ใช้บริการ</h2>
                    <canvas id="timeChart"></canvas>
                </div>
            </div>
            <div class="chart-container">
                <div class="graph-info">
                    <h2>สถิติช่วงเวลาที่ใช้บริการ</h2>
                    <canvas id="MyChart"></canvas>
                </div>
            </div>
        </div>

    </div>
    <canvas id="ageChart2"></canvas>
    <script src="/JS/chart.js"></script>
    <script src="/JS/report_script.js"></script>
</body>
</html>