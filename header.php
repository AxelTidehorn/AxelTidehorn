<!DOCTYPE html>
<html>
  <head>
        <title>Axel Tidehorn | Portfolio</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <script src="https://kit.fontawesome.com/8f51a7ee18.js"></script>
        <link rel="stylesheet" href=<?php bloginfo('stylesheet_url'); ?>>
        <script src="https://unpkg.com/masonry-layout@4/dist/masonry.pkgd.min.js"></script>
        <script src="https://unpkg.com/imagesloaded@4/imagesloaded.pkgd.js"></script>
    </head>



    <body>
        <header>
            <div class="header-wrapper">
                <div class="logo-wrapper">
                    <a href="http://localhost/AxelTidehorn2/wordpress/">
                        <svg width="100%" height="100%" viewBox="0 0 1400 1200" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
                            <g>
                                <path d="M150.405,563.074c-31.048,-72.444 -10.35,-139.138 62.094,-200.083c25.298,-20.698 50.883,-36.509 76.756,-47.433c25.873,-10.925 49.733,-18.686 71.581,-23.286c25.298,-4.6 49.446,-6.899 72.444,-6.899c-12.649,11.499 -22.423,25.297 -29.322,41.396c-5.75,13.799 -9.2,30.76 -10.35,50.883c-1.149,20.123 4.6,43.409 17.249,69.857c8.049,17.248 12.361,35.359 12.936,54.332c0.575,18.974 -2.587,37.085 -9.486,54.333c-6.9,17.249 -16.674,32.772 -29.323,46.571c-12.649,13.799 -28.172,24.723 -46.571,32.772c-17.248,8.05 -35.359,12.074 -54.333,12.074c-18.973,0 -37.084,-3.162 -54.332,-9.486c-17.249,-6.325 -32.773,-15.812 -46.571,-28.46c-13.799,-12.649 -24.723,-28.173 -32.772,-46.571Zm224.23,631.595l132.814,0c-47.146,-16.099 -85.668,-44.846 -115.565,-86.242c-29.898,-41.397 -44.847,-88.543 -44.847,-141.438c0,-52.896 14.949,-100.042 44.847,-141.438c29.897,-41.396 68.419,-70.144 115.565,-86.242l-151.787,0c-58.645,0 -107.803,7.474 -147.475,22.423c-39.672,14.948 -71.006,33.634 -94.004,56.057c-22.998,22.423 -39.384,46.859 -49.159,73.306c-9.774,26.448 -14.661,51.746 -14.661,75.894c0,25.298 4.312,51.17 12.937,77.618c8.624,26.448 24.435,50.883 47.433,73.306c22.998,22.423 54.333,40.822 94.004,55.195c39.672,14.374 89.98,21.561 150.925,21.561l18.973,0Z" style="fill:#fff;fill-rule:nonzero;transition:ease .25s;"/>
                                <path d="M1309.9,284.029l0,345.381l-6.367,0c-7.427,-10.611 -19.364,-28.384 -35.811,-53.319c-16.447,-24.936 -38.199,-53.319 -65.257,-85.152c-27.057,-31.832 -59.951,-65.256 -98.68,-100.272c-38.729,-35.016 -84.091,-67.909 -136.084,-98.68l0,-7.958l342.199,0Zm-689.229,1.427c40.321,-21.222 81.703,-45.626 124.146,-73.214c36.077,-24.405 75.867,-53.85 119.372,-88.335c43.504,-34.485 86.478,-74.011 128.921,-118.576l0,791.035c0,37.138 5.04,70.827 15.12,101.068c10.081,30.241 23.609,57.829 40.587,82.764c16.977,24.936 36.076,46.953 57.298,66.052c21.222,19.1 42.974,35.547 65.256,49.341c51.993,33.954 111.414,59.951 178.262,77.989c-42.443,7.428 -84.887,13.264 -127.33,17.508c-37.138,3.183 -77.193,4.244 -120.167,3.183c-42.974,-1.061 -83.56,-6.366 -121.759,-15.916c-37.138,-9.55 -71.888,-27.058 -104.251,-52.524c-32.363,-25.465 -60.482,-56.502 -84.356,-93.109c-23.874,-36.608 -42.709,-77.194 -56.503,-121.759c-13.794,-44.566 -20.691,-90.192 -20.691,-136.88l0,-253.067c0,-54.115 -5.04,-96.558 -15.12,-127.33c-10.08,-30.771 -20.956,-54.115 -32.628,-70.031c-13.794,-19.099 -29.18,-31.832 -46.157,-38.199Z" style="fill:#fff;fill-rule:nonzero;transition:ease .25s;"/>
                            </g>
                        </svg>
                    </a>
                </div>
                <button id="hamburger" class="hamburger-btn" onClick="toggleMenu()">
                    <span class="line"></span>
                    <span class="line"></span>
                    <span class="line"></span>
                </button>
                <nav class="desktop-menu">
                    <?php wp_nav_menu(array('theme_location => header-menu')) ?>
                </nav>
            </div>
        </header>
        <nav class="mobile-menu">
            <?php wp_nav_menu(array('theme_location => header-menu')) ?>
        </nav>

        <script>

            function toggleMenu(){
                const menu = document.querySelector(".mobile-menu");
                const hamburger = document.getElementById("hamburger");
                menu.classList.toggle("reveal-menu");
                hamburger.classList.toggle("clicked");
            }

        </script>
