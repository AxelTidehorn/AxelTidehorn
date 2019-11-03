<?php

    require('includes/reg_menus.php');
  //  require('includes/reg_post_types.php');

    add_image_size('grid_thumbnail', 300, 300, true);
    add_image_size('single_large', 660, 660, false);


    add_theme_support('post-thumbnails');


?>
