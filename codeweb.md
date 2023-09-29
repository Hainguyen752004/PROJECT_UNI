<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Z COFFEE ĐIỂM HẸN SINH VIÊN </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f2f2f2;
        }
        header {
            background-color: #003366;
            color: #fff;
            text-align: center;
            padding: 20px;
        }
        h1 {
            margin: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }
        .product {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 20px;
            margin: 10px;
            width: calc(33.33% - 20px);
        }
        .product img {
            max-width: 100%;
        }

        #menu ul{
	list-style-type:none;
	padding: 0;
	margin: 0;
}
#menu ul li{
	line-height: 2.9em;
	height: 2.9em;
}
#menu {
    background-color: black; 
    position: fixed;
    height: 100%; 
    width: 150px;
    left: 0;
}
#menu li a{
	display: block;
	color: white;
	padding: 0 1em;
	border-bottom: 1px;
}
#content{
	padding: 1em 8em;
}
    </style>
</head>
<body>
    <div id="contain">
        <div id="menu">
            <ul>
                    <li>
						<a href="#">Trang Chủ</a>
					</li>

                    <li>
						<a href="#">Dịch Vụ</a>
					</li>
                    <li>
						<a href="#"> Sản Phẩm</a>
					</li>
                    <li>
						<a href="#"> Tin Tức</a>
					</li>
                    <li>
						<a href="#"> Diễn Đàn</a>
					</li>
                    <li>
						<a href="#">Liên Hệ</a>
					
					</li>
            </ul>
    </div>
    <header>
        <h1>Z COFFEE ĐIỂM HẸN SINH VIÊN </h1>
    </header>
    <div class="container">
        <div class="product">
            <img src="https://inlysugiare.vn/wp-content/uploads/2020/05/ly-ca-phe-bac-xiu-da.jpg" alt="Sản phẩm 1">
            <h2>Bạc xỉu đá </h2>
            <p>Mô tả sản phẩm 1...</p>
            <p><strong>Giá:</strong> 1.000.000 VND</p>
            <a href="#">Mua ngay</a>
        </div>
        <div class="product">
            <img src="link_hinh_san_pham_2.jpg" alt="Sản phẩm 2">
            <h2>Sản phẩm 2</h2>
            <p>Mô tả sản phẩm 2...</p>
            <p><strong>Giá:</strong> 2.000.000 VND</p>
            <a href="#">Mua ngay</a>
        </div>
        <div class="product">
            <img src="link_hinh_san_pham_3.jpg" alt="Sản phẩm 3">
            <h2>Sản phẩm 3</h2>
            <p>Mô tả sản phẩm 3...</p>
            <p><strong>Giá:</strong> 3.000.000 VND</p>
            <a href="#">Mua ngay</a>
        </div>
    </div>
</body>
</html>
