<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Table Data</title>
    <link rel="stylesheet" href="/css/styleg.css">
    <link rel="stylesheet" href="/css/styles.css">
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
                include '/var/www/html/Project/COM/php/yearindb.php';
                ?>
            </div>
            </li>
            <li><a href="#">About</a></li>
        </ul>
    </div>
</nav>
    <div class="container">
        <h2>สัดส่วนการใช้บริการทั้งหมด</h2>
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
        <div class="content" style="display: flex ;">
            <h2 style="display : flex ; margin-left: 35vh; margin-top: 5vh;">เปอร์เซนต์ผู้ใช่บริการ</h2>
            <h2 style="display : flex ; margin-right: 35vh; margin-top: 5vh;">สัดส่วนอายุผู้ใช้บริการ</h2>
        <div class="content">
            <div class="chart-container">
                <canvas id="genderChart"></canvas>
            </div>
                <div class="chart-container" style="position: relative;">

                    <canvas id="ageChart"></canvas>
                    <!-- 
                <div class="dropdown">
                <select id="ageRangeDropdown">
                    <option value="All">All</option>
                    <option value="Under 20">น้อยกว่า20</option>
                    <option value="21-40">21-40</option>
                    <option value="41-59">41-59</option>
                    <option value="60+">มากกว่า 60</option>
                </select>
            </div> -->
            </div>
            <div class="chart-container">
                <div class="graph-info">
                    <h2 style=" margin-top: 5vh;">สถิติเดือนที่ใช้บริการ</h2>
                    <canvas id="timeChart"></canvas>
                </div>
            </div>
            <div class="chart-container">
                <div class="graph-info">
                    <h2 style="margin-top: 5vh;">สถิติช่วงเวลาที่ใช้บริการ</h2>
                    <canvas id="MyChart"></canvas>
                </div>
            </div>
        </div>

    </div>
    <canvas id="ageChart2"></canvas>
    <script src="/JS/chart_script.js"></script>
    <script src="/JS/report_script.js"></script>
   
</body>

</html>